import os

from openscad_linter import OpenscadLinter


class LinterTestCase(object):
    def _get_fixture_file_name(self, fixture_name):
        path = [os.path.dirname(os.path.abspath(__file__))]
        path += ['fixtures', fixture_name + '.scad']
        return os.path.join(*path)

    def _lint_file(self, file_name, code):
        nags = {'list': []}  # nested in a dict, as Python 2 lacks 'nonlocal'

        def nag(code, msg, file_name, line='', col=''):
            nags['list'] += [code]

        OpenscadLinter(nag).lint_file(file_name)

        if code is None:
            assert not nags['list']
        else:
            assert code in nags['list']

    def assert_failing_fixture(self, fixture_name, code):
        file_name = self._get_fixture_file_name(fixture_name)
        self._lint_file(file_name, code)

    def assert_ok_fixture(self, fixture_name):
        self.assert_failing_fixture(fixture_name, code=None)
