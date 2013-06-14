import unittest
from .backends import MemoryBackend
from .handlers import get_handler, parse


class TestS3Repository(unittest.TestCase):
    def setUp(self, ):
        self.pkgs = [
            "test-pkg-1.0.0.tar.gz",
            "test-pkg-1.1.0.tar.gz",
            "test-pkg-1.2.0.dev.20130601.0900-1.1.0-1-gaaa001.tar.gz",
            "test-pkg-1.2.0.dev.20130601.1000-1.1.0-3-gaaa003.tar.gz",
            "test-pkg-1.2.0.rc.20130601.1030-1.1.0-3-gaaa003.tar.gz",
            "test-pkg-1.2.0.dev.20130601.1200-1.1.0-5-gaaa005.tar.gz",
            "test-pkg-1.2.0.dev.20130601.1230-1.1.0-6-gaaa006.tar.gz",
            "test-pkg-1.2.0.rc.20130601.1330-1.1.0-6-gaaa006.tar.gz",
            "test-one-two2-1.0.0.tar.gz",
            "test-one-two2-1.2.0.dev.20130601.0900-1.1.0-1-gaaa001.tar.gz",
            "test-one-two2-1.2.0.dev.20130601.1000-1.1.0-3-gaaa003.tar.gz",
            "test-one-two2-1.2.0.rc.20130601.1030-1.1.0-3-gaaa003.tar.gz",
        ]
        self._init_repo()

    def _init_repo(self,):
        self.repo = get_handler(MemoryBackend(self.pkgs))

    def test_parse(self,):
        final = ("test-pkg", "1.0.0")
        self.assertEqual(final, parse("{0}-{1}".format(*final)))
        dev = ("test-one-two2", "1.2.0.dev.20130601.0900-1.1.0-1-gaaa001")
        self.assertEqual(dev, parse("{0}-{1}".format(*dev)))
        with_ext = ("test-pkg", "1.0.0")
        self.assertEqual(with_ext, parse("{0}-{1}.tar.gz".format(*with_ext)))


    def test_has_package(self,):
        valid = self.pkgs[0]
        self.assertTrue(self.repo.has_package(valid))
        invalid = "does-not-exists"
        self.assertFalse(self.repo.has_package(invalid))
        version_invalid = valid.replace("1.0.0", "999.999.999")
        self.assertFalse(self.repo.has_package(version_invalid))
        name_invalid = valid.replace("test-pkg", "xxx_xxx")
        self.assertFalse(self.repo.has_package(name_invalid))

    def test_get_by_name(self,):
        self._init_repo()
        def expect(search):
            return map(lambda s: s.rstrip(".tar.gz"),
                       filter(
                           lambda s: s.startswith(search), self.pkgs))
        search = "test-pkgs"
        self.assertEqual(expect(search), self.repo.get_by_name(search))
        search = "test-one-two2"
        self.assertEqual(expect(search), self.repo.get_by_name(search))
        search = "does-not-exists"
        self.assertEqual(expect(search), self.repo.get_by_name(search))

    def test_get_latest(self,):
        def _assertExists(expect, pkg_name=None):
            pkg_name = expect[0] if not pkg_name else pkg_name
            self.assertEqual("{0}-{1}".format(*expect),
                             self.repo.get_latest(pkg_name))
        expect = ("test-pkg","1.2.0.rc.20130601.1330-1.1.0-6-gaaa006")
        print self.repo._cache
        _assertExists(expect)
        expect = ("test-pkg","1.3.0")
        self.pkgs.append("{0}-{1}".format(*expect))
        self._init_repo()
        _assertExists(expect)
        with self.assertRaises(LookupError):
            self.repo.get_latest("does-not-exists")
        expect = ("test-pkg","1.2.0.rc.20130601.1330-1.1.0-6-gaaa006")
        _assertExists(expect, "test-pkg < 1.3.0")

    def test_match(self,):
         regex = "test-pkg.*gaaa006"
         expect = [
            "test-pkg-1.2.0.dev.20130601.1230-1.1.0-6-gaaa006",
            "test-pkg-1.2.0.rc.20130601.1330-1.1.0-6-gaaa006",
         ]
         self.assertEqual(expect, self.repo.match(regex))
         self.assertEqual([], self.repo.match("does-not-exist"))