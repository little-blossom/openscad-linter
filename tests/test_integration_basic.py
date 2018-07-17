from tests.linter_integration_test_case import LinterIntegrationTestCase


class TestModule(LinterIntegrationTestCase):
    def test_module_plain(self):
        self.assert_ok_fixture('module_plain')

    def test_orphan_test(self):
        self.assert_ok_fixture('module_orphan_test')

    def test_U005_param_no_space_after_1st_comma(self):
        self.assert_failing_fixture('spacing_comma_missing_after_1', 'U005')
