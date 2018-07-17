from tests.linter_test_case import LinterTestCase


class TestSpacing(LinterTestCase):
    def test_spacing_plain(self):
        self.assert_ok_fixture('spacing_plain')

    def test_U005_param_no_space_after_1st_comma(self):
        self.assert_failing_fixture('spacing_comma_missing_after_1', 'U005')

    def test_U005_param_no_space_after_2nd_comma(self):
        self.assert_failing_fixture('spacing_comma_missing_after_2', 'U005')

    def test_U006_trailing_whitespace_space(self):
        self.assert_failing_fixture('spacing_trailing_whitespace_space',
                                    'U006')

    def test_U006_trailing_whitespace_tab(self):
        self.assert_failing_fixture('spacing_trailing_whitespace_tab', 'U006')
