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
import time
import unittest

import apphelper

import psi


class ExceptionsTests(unittest.TestCase):
    def test_attr_subclass(self):
        self.assert_(issubclass(psi.AttrNotAvailableError, AttributeError))
        self.assert_(issubclass(psi.AttrInsufficientPrivsError, AttributeError))
        self.assert_(issubclass(psi.AttrNotImplementedError, AttributeError))

    def test_attr_instances(self):
        na = psi.AttrNotAvailableError()
        ip = psi.AttrInsufficientPrivsError()
        ni = psi.AttrNotImplementedError()
        self.assert_(isinstance(na, AttributeError))
        self.assert_(isinstance(ip, AttributeError))
        self.assert_(isinstance(ni, AttributeError))

    def test_resource_subclass(self):
        self.assert_(issubclass(psi.MissingResourceError, Exception))

    def test_resource_instance(self):
        mr = psi.MissingResourceError()
        self.assert_(isinstance(mr, Exception))


class LoadavgTests(unittest.TestCase):
    def test_type(self):
        loadavg = psi.loadavg()
        self.assertTrue(isinstance(loadavg, tuple))

    def test_len(self):
        loadavg = psi.loadavg()
        self.assertEqual(len(loadavg), 3)

    def test_value_types(self):
        loadavg = psi.loadavg()
        for v in loadavg:
            self.assertTrue(isinstance(v, float))

    def test_values(self):
        psiavg = psi.loadavg()
        if hasattr(os, 'getloadavg'):
            osavg = os.getloadavg()
            for i, j in zip(psiavg, osavg):
                self.assertAlmostEqual(i, j)
        else:
            for l in psiavg:
                self.assert_(0.0 <= l < 1000.0, '0.0 < %f < 1000.0'%l)


class BoottimeTests(unittest.TestCase):
    def test_timespec(self):
        self.assert_(isinstance(psi.boottime(), psi.TimeSpec))

    def test_gt_epoch(self):
        bt = psi.boottime()
        self.assert_(bt.timestamp() > 0, '%s > 0' % bt.timestamp())

    def test_lt_now(self):
        bt = psi.boottime()
        now = time.time()
        self.assert_(bt.timestamp() < now, '%s < %s' % (bt.timestamp(), now))

    def test_boottime_calc(self):
        psi_bt = psi.boottime()
        calc_bt = time.time() - psi.uptime().timestamp()
        calc_min = calc_bt - 2
        calc_max = calc_bt + 2
        self.assert_(calc_min < psi_bt.timestamp() < calc_max,
                     '%s < %s < %s' % (calc_min, psi_bt.timestamp(), calc_max))


class UptimeTests(unittest.TestCase):
    def test_timedelta(self):
        ut = psi.uptime()
        self.assert_(isinstance(ut, psi.TimeSpec))

    def test_uptime_gt_null(self):
        self.assert_(psi.uptime().timestamp() > 0)

    def test_uptime_calc(self):
        psi_uptime = psi.uptime().timestamp()
        calc_uptime = time.time() - psi.boottime().timestamp()
        calc_min = calc_uptime - 2
        calc_max = calc_uptime + 2
        self.assert_(calc_min < psi_uptime < calc_max,
                     "%s < %s < %s" % (calc_min, psi_uptime, calc_max))


if hasattr(psi, 'getzoneid'):
    class SolarisZonesTests(unittest.TestCase):
        def setUp(self):
            self.zoneids = []
            self.zonenames = []
            self.zonename = apphelper.run(['zonename'])
            zones = apphelper.run(['/usr/sbin/zoneadm', 'list', '-p'])
            for zone in zones.splitlines():
                zid, zname, tail = zone.split(':', 2)
                if zname == self.zonename:
                    self.zoneid = int(zid)
                self.zoneids.append(int(zid))
                self.zonenames.append(zname)

        def test_getzoneid(self):
            self.assertEqual(psi.getzoneid(), self.zoneid)

        def test_getzonenamebyid(self):
            self.assertEqual(psi.getzonenamebyid(self.zoneid), self.zonename)

        def test_getzonenamebyid_exception(self):
            zid = self.zoneid * 2
            while zid in self.zoneids:
                zid *= 2
            self.assertRaises(ValueError, psi.getzonenamebyid, zid)

        def test_getzoneidbyname(self):
            self.assertEqual(psi.getzoneidbyname(self.zonename), self.zoneid)

        def test_getzoneidbyname_exception(self):
            name = self.zonename * 2
            while name in self.zonenames:
                name *= 2
            self.assertRaises(ValueError, psi.getzoneidbyname, name)


if __name__ == '__main__':
    unittest.main()
