from tests.linter_test_case import LinterTestCase
from subprocess import Popen, PIPE


class LinterIntegrationTestCase(LinterTestCase):
    def __run_linter(self, file_name):
        proc = Popen(["./lint", "--only-file", file_name],
                     stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = proc.communicate()
        return (proc.returncode, stdout, stderr)

    def _lint_file(self, file_name, code):
        (result, stdout, stderr) = self.__run_linter(file_name)
        assert not stdout
        if code is None:
            assert not stderr
            assert result == 0
        else:
            assert code in stderr
            assert result != 0
