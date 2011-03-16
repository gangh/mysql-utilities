#!/usr/bin/env python

import os
import diskusage_basic
from mysql.utilities.exception import MySQLUtilError, MUTException

class test(diskusage_basic.test):
    """Disk usage
    This test executes the disk space utility on a single server.
    It uses the diskusage_basic test for setup and teardown methods.
    """

    def check_prerequisites(self):
        return diskusage_basic.test.check_prerequisites(self)

    def setup(self):
        return diskusage_basic.test.setup(self)

    def run(self):
        self.res_fname = self.testdir + "result.txt"

        from_conn = "--server=%s" % self.build_connection_string(self.server1)

        _FORMATS = ("CSV", "TAB", "GRID", "VERTICAL", "NOT_THERE")

        cmd_base = "mysqldiskusage.py %s util_test --format=" % from_conn
        test_num = 1
        for format in _FORMATS:
            comment = "Test Case %d : Testing disk space with " % test_num
            comment += "%s format " % format

            res = self.run_test_case(0, cmd_base+format, comment)
            if not res:
                raise MUTException("DISKUSAGE: %s: failed" % comment)

            test_num += 1

        diskusage_basic.test.mask(self)

        return True

    def get_result(self):
        return self.compare(__name__, self.results)

    def record(self):
        return self.save_result_file(__name__, self.results)

    def cleanup(self):
        return diskusage_basic.test.cleanup(self)