import argparse
import functools
import itertools
import re
import sys


from pkg_resources import parse_version, Requirement


import backends


def _starts_with_digit(s):
    return re.compile("\d").match(s[0])


def _pid(name, version):
    """ builds a package identifier based on name and version as:
    name{-version}, version is optional if blank
    """
    return "{name}{sep}{ver}".format(
        name=name,
        sep="-" if version else "",
        ver=version if version else ""
    )


def parse(pkg):
    def _strip_ext(name):
        # as per http://docs.python.org/2/distutils/sourcedist.html
        SDIST_EXT=(".tar.gz", ".zip", ".tar.bz2", "tar.z", ".tar")
        for ext in SDIST_EXT:
            if name.endswith(ext):
                return name.split(ext)[0]
        return name
    name = ""
    pkg_name = _strip_ext(pkg)
    for part in pkg_name.split("-"):
        if not _starts_with_digit(part):
            name = "{0}{1}{2}".format(name, "-" if name else "", part)
        else:
            return (name, pkg_name.split("{0}-".format(name)).pop())
    return (name, pkg_name.split("{0}-".format(name)).pop())


class RepoHandler(object):
    def __init__(self, backend):
        self.backend = backend
        self._cache = {}
        self._init_cache()

    def _init_cache(self,):
        for p in self.backend.gen_pksg():
            name, version = parse(p)
            self._cache.setdefault(name, []).append(version)

    def _iter_pkgs(self,):
        return itertools.chain(*[[(k,v) for v in vs]
                                 for k, vs in self._cache.items()])

    def has_package(self, pkg):
        try:
            name, ver = parse(pkg)
        except:
            print "Error pkg {0}".format(pkg)
        return ver in self._cache.get(name, [])

    def get_latest(self, pkg_spec):
        """
        Returns the name of the latest package file on the repository
        pkg_spec: is a setuptools formated package specifier"""
        req_name = Requirement.parse(pkg_spec).key
        req_specs = Requirement.parse(pkg_spec).specs
        specs = req_specs[0] if req_specs else ("", "")
        op, version = specs
        pkgs = map(lambda p: parse(p)[1], self.get_by_name(req_name))
        pkgs = filter(lambda p:
                      eval("{v1}{op}{v2}".format(v1=parse_version(p), op=op,
                                                 v2=parse_version(version) if
                                                 version else "")),
                      pkgs)
        asc_vers = sorted(pkgs, key=parse_version)
        if asc_vers:
            last_ver = asc_vers.pop()
            return "{pkg_name}-{ver}".format(pkg_name=req_name, ver=last_ver)
        raise LookupError(
            "Pkg {pkg} doesn't exists in the repository".format(pkg=req_name))

    def get_by_name(self, pkg_name):
        return map(lambda v: _pid(pkg_name, v),
                   self._cache.get(pkg_name, []))

    def match(self, regex):
        patt = re.compile(regex)
        return [_pid(*i) for i in self._iter_pkgs() if patt.search(_pid(*i))]


def get_handler(backend):
    return RepoHandler(backend)


def _parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["latest", "exists", "list", "match"])
    parser.add_argument("arg", help="package name (latest, exists, list) or regexp (match)")
    parser.add_argument("-b", "--bucket", help="Used for s3 backend")
    return parser.parse_args()


def _pretty_print(o):
    if isinstance(o, list):
        for el in o:
            print el
    else:
        print o
    if not o:
        sys.exit(1)


def _handle_cli(args):
    h = get_handler(backends.S3Backend(args.bucket))
    dispatcher = {
        "latest": functools.partial(h.get_latest),
        "match": functools.partial(h.match),
        "exists": functools.partial(h.has_package),
        "list": functools.partial(h.get_by_name),}
    _pretty_print(dispatcher.get(args.cmd)(args.arg))


def main():
    _handle_cli(_parse_cli())


if __name__ == '__main__':
    main()
