# The MIT License
#
# Copyright (C) 2008-2009 Floris Bruynooghe
#
# Copyright (C) 2008-2009 Abilisoft Ltd.
#
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import unittest

import psi


class ProcessTableTests(unittest.TestCase):
    def setUp(self):
        self.archtype = psi.arch.arch_type()
        self.pt = psi.process.ProcessTable()

    def test_type(self):
        self.assert_(isinstance(self.pt, psi.process.ProcessTable))
        self.assert_(isinstance(self.pt, dict))

    def test_len_nonzero(self):
        self.assert_(len(self.pt) > 0)

    def test_keys(self):
        for pid in self.pt.keys():
            self.assert_(pid >= 0)

    def test_vals(self):
        for p in self.pt.values():
            break
        self.assert_(isinstance(p, psi.process.Process))

    def test_setitem(self):
        self.assertRaises(TypeError, self.pt.__setitem__, 123, 'dummy')

    def test_delitem(self):
        self.assertRaises(TypeError, self.pt.__delitem__, 1)


class ProcessAttributeTests(unittest.TestCase):
    """Check the bahaviour of some process attributes

    Some process attributes must be present on all processes, these
    tests check for this.
    """
    def setUp(self):
        self.archtype = psi.arch.arch_type()
        if isinstance(self.archtype, psi.arch.ArchLinux):
            self.zombie_stat = psi.process.PROC_STATUS_ZOMBIE
        else:
            self.zombie_stat = psi.process.PROC_STATUS_SZOMB

    def test_name(self):
        for p in psi.process.ProcessTable().values():
            if p.status == self.zombie_stat:
                self.assertEqual(type(str(p.name)), type(''))
            else:
                self.assert_(p.name, str(p))

    def test_argc(self):
        for p in psi.process.ProcessTable().values():
            try:
                self.assert_(p.argc >= 0, '%s, argc=%s' % (p, p.argc))
            except psi.AttrInsufficientPrivsError:
                if isinstance(self.archtype, psi.arch.ArchDarwin):
                    # On OS X, argc is not available if the process is
                    # in a Zombie state or if the process is not owned
                    # by the current user.
                    if (p.pid != 0 and
                            (p.status != psi.process.PROC_STATUS_SZOMB or
                             p.euid == os.geteuid())):
                        print p, p.name
                        raise

    def test_command(self):
        for p in psi.process.ProcessTable().values():
            if p.status == self.zombie_stat:
                self.assertEqual(type(str(p.command)), type(''))
            else:
                self.assert_(p.command, str(p))


if __name__ == '__main__':
    unittest.main()
