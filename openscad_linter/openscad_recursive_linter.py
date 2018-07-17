import os


class OpenscadRecursiveLinter(object):
    def __init__(self, linter):
        self.linter = linter

    def lint_files(self, base):
        if os.path.isfile(base):
            self.linter.lint_file(base)
        elif os.path.isdir(base):
            for root, dirs, files in os.walk(base):
                for omitted in ['fixtures', 'test-results']:
                    if omitted in dirs:
                        dirs.remove(omitted)
                for file_name in files:
                    if file_name.endswith('.scad'):
                        self.linter.lint_file(os.path.join(root, file_name))
        else:
            raise RuntimeError("'%s' is neither file nor directory" % (base))
