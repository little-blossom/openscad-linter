from tests.linter_test_case import LinterTestCase


class TestModule(LinterTestCase):
    def test_module_plain(self):
        self.assert_ok_fixture('module_plain')

    def test_no_expected_module(self):
        self.assert_ok_fixture('module_no_expected_module')

    def test_orphan_test(self):
        self.assert_ok_fixture('module_orphan_test')

    def test_U001_paren_missing2(self):
        self.assert_failing_fixture('module_paren_on_different_line', 'U001')

    def test_U003_no_tests(self):
        self.assert_failing_fixture('module_no_tests', 'U003')

    def test_U004_unexpected_module_name(self):
        self.assert_failing_fixture('module_neither_expected_nor_test', 'U004')

    def test_U007_module_defined_twice(self):
        self.assert_failing_fixture('module_twice_defined', 'U007')
