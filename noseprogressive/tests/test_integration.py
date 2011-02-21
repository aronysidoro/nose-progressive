from unittest import TestCase, TestSuite

from nose import SkipTest
from nose.plugins import PluginTester
from nose.plugins.skip import Skip
from nose.tools import eq_

from noseprogressive import ProgressivePlugin


class IntegrationTestCase(PluginTester, TestCase):
    activate = '--with-progressive'
    plugins = [ProgressivePlugin(), Skip()]


class HookTests(IntegrationTestCase):
    """Tests that ensure our code is getting run when expected"""

    def makeSuite(self):
        class Failure(TestCase):
            def runTest(self):
                assert False

        class Skip(TestCase):
            def runTest(self):
                raise SkipTest

        class Success(TestCase):
            def runTest(self):
                pass

        class Error(TestCase):
            def runTest(self):
                raise NotImplementedError

        return TestSuite([Failure(), Skip(), Success(), Error()])

    def _count_eq(self, text, count):
        """Assert `text` appears `count` times in the captured output."""
        eq_(str(self.output).count(text), count)

    def test_fail(self):
        """Make sure failed tests print a line."""
        # Grrr, we seem to get stdout here, not stderr.
        self._count_eq('FAIL: ', 1)

    def test_skip(self):
        """Make sure skipped tests print a line."""
        self._count_eq('SKIP: ', 1)

    def test_error(self):
        """Make sure uncaught errors print a line."""
        self._count_eq('ERROR: ', 1)

    # Proper handling of test successes is tested by the sum of the above, in
    # that no more than one failure, skip, and error is shown.

    def test_summary(self):
        """Make sure summary prints.

        Also incidentally test that addError() counts correctly.

        """
        assert '4 tests, 1 failure, 1 error, 1 skip in ' in self.output


# def test_slowly():
#     def failer(y):
#         print "booga"
#         if y == 1:
#             assert False
#     for x in range(10):
#         from time import sleep
#         sleep(0.1)
#         yield failer, x


# def test_syntax_error():
#     x = 1
#     :bad
