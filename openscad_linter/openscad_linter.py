import logging
import os
import re


class OpenscadLinter(object):
    def __init__(self, nag):
        self.nag = nag

    def get_expected_module_name(self, file_name):
        ret = os.path.basename(file_name)
        if ret.endswith('.scad'):
            ret = ret[:-5]
        ret = re.sub('_([a-z])', lambda p: p.group(1).upper(), ret)
        return ret

    def lint_file(self, file_name):
        nag = self.nag

        logging.debug('Linting file %s' % (file_name))

        expected_module_name = self.get_expected_module_name(file_name)
        has_expected_module = False
        has_tests = False

        with open(file_name, 'r') as f:
            line_number = 0
            for line in f:
                if line.endswith('\n'):
                    line = line[:-1]
                logging.debug('Linting line %s' % (line))
                line_number += 1
                if line.startswith('module '):
                    split = line[7:].split('(', 1)
                    if len(split) == 2:
                        module_name = split[0]
                        if module_name == expected_module_name:
                            if has_expected_module:
                                nag('U007', 'module \'%s\' has already been \
defined' % (module_name), file_name, line_number, 7)
                            else:
                                has_expected_module = True
                        elif module_name.startswith("test"):
                            has_tests = True
                        else:
                            nag('U004', 'module \'%s\' neither expected nor test \
module' % (module_name), file_name, line_number, 7)
                    else:
                        nag('U001',
                            'module definition without \'(\' on same line',
                            file_name, line_number, 7)

                match = re.search(',[^ ]', line)
                if match:
                    nag('U005', 'missing space after comma', file_name,
                        line_number, match.start())

                match = re.search('[ 	]$', line)
                if match:
                    nag('U006', 'trailing whitespace', file_name,
                        line_number, match.start())

        if has_expected_module and not has_tests:
                nag('U003', 'module \'%s\' does not have tests\
' % (expected_module_name), file_name)
