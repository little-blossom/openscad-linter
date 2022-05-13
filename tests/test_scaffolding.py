from tests.linter_test_case import LinterTestCase
from openscad_linter import OpenscadRecursiveLinter
from mock import Mock
import os
import os.path
import pytest


class TestScaffolding(LinterTestCase):
    def touch(self, tmpdir, file_parts):
        file_abs = os.path.join(tmpdir, *file_parts)
        dir_abs = os.path.dirname(file_abs)
        if not os.path.exists(dir_abs):
            os.makedirs(dir_abs)

        open(file_abs, 'a').close()

        return file_abs

    def assert_linted_files(self, linter, expected):
        print(linter)
        print(linter.lint_file)
        calls = linter.lint_file.call_args_list
        actual = sorted([c[0][0] for c in calls])

        expected = sorted(expected)

        assert actual == expected

    def test_lint_files_single_file(self):
        file_name = self._get_fixture_file_name('module_plain')
        linter = Mock()

        OpenscadRecursiveLinter(linter).lint_files(file_name)

        self.assert_linted_files(linter, [file_name])

    def test_lint_files_directory_plain(self, tmpdir):
        tmpdir = str(tmpdir)

        expected = []
        for file_name in [
                ['foo.scad'],
                ['bar.scad'],
                ]:
            abs_file_name = self.touch(tmpdir, file_name)
            expected += [abs_file_name]
        expected.sort()
        linter = Mock()

        OpenscadRecursiveLinter(linter).lint_files(tmpdir)

        self.assert_linted_files(linter, expected)

    def test_lint_files_directory_ignore_non_scad(self, tmpdir):
        tmpdir = str(tmpdir)

        expected = []
        for file_name in [
                ['foo.scad'],
                ['bar.txt'],
                ['baz.scad'],
                ]:
            abs_file_name = self.touch(tmpdir, file_name)
            if file_name != ['bar.txt']:
                expected += [abs_file_name]
        print(expected)
        expected.sort()
        linter = Mock()

        OpenscadRecursiveLinter(linter).lint_files(tmpdir)

        self.assert_linted_files(linter, expected)

    def test_lint_files_directory_descending(self, tmpdir):
        tmpdir = str(tmpdir)

        expected = []
        for file_name in [
                ['foo.scad'],
                ['bar.txt'],
                ['foo', 'foo.scad'],
                ['foo', 'bar.txt'],
                ]:
            abs_file_name = self.touch(tmpdir, file_name)
            if file_name[-1] != 'bar.txt':
                expected += [abs_file_name]

        expected.sort()
        linter = Mock()

        OpenscadRecursiveLinter(linter).lint_files(tmpdir)

        self.assert_linted_files(linter, expected)

    def test_lint_files_directory_ignore_fixtures(self, tmpdir):
        tmpdir = str(tmpdir)

        expected = []
        for file_name in [
                ['foo.scad'],
                ['bar.txt'],
                ['fixtures', 'foo.scad'],
                ['fixtures', 'bar.txt'],
                ]:
            abs_file_name = self.touch(tmpdir, file_name)
            if file_name[0] != 'fixtures' and file_name[-1] != 'bar.txt':
                expected += [abs_file_name]

        expected.sort()
        linter = Mock()

        OpenscadRecursiveLinter(linter).lint_files(tmpdir)

        self.assert_linted_files(linter, expected)

    def test_lint_files_directory_ignore_test_results(self, tmpdir):
        tmpdir = str(tmpdir)

        expected = []
        for file_name in [
                ['foo.scad'],
                ['bar.txt'],
                ['test-results', 'foo.scad'],
                ['test-results', 'bar.txt'],
                ]:
            abs_file_name = self.touch(tmpdir, file_name)
            if file_name[0] != 'test-results' and file_name[-1] != 'bar.txt':
                expected += [abs_file_name]

        expected.sort()
        linter = Mock()

        OpenscadRecursiveLinter(linter).lint_files(tmpdir)

        self.assert_linted_files(linter, expected)

    def test_lint_files_neither_file_nor_directory(self, tmpdir):
        base = os.path.join(str(tmpdir), 'foo')

        linter = Mock()

        with pytest.raises(RuntimeError) as e_info:
            OpenscadRecursiveLinter(linter).lint_files(base)

        assert base in str(e_info.value)
