"""Check for memory leak

If the memory goes consistent and significantly up there is a leak,
either directly or from reference counting errors.

Note that this isn't perfect, not all code is executed during the loop
(e.g. since this process doesn't have children part of the .children()
code won't be exercised).
"""


import datetime
import glob
import os
import sys
import time
import unittest
import warnings

warnings.simplefilter('ignore', FutureWarning)

import psi
import psi.arch
import psi.process
import psi.mount


# If python didn't get compiled with PYDEBUG enabled we can't keep
# track of the reference count.  Returning 1 to avoid zero-devision
# errors.
if not hasattr(sys, 'gettotalrefcount'):
    sys.gettotalrefcount = lambda: 1


def check_psi():
    psi.loadavg()
    psi.boottime()
    psi.uptime()


def check_arch():
    psi.arch.ArchBase()


def check_process(pid):
    p = psi.process.Process(pid)
    p.children()
    p.exists()
    p.refresh()
    psi.process.ProcessTable()


def check_mount():
    for m in psi.mount.mounts():
        pass


def check_test_suite():
    tdir = os.path.join(os.path.dirname(__file__), '..', 'tests')
    if tdir not in sys.path:
        sys.path.insert(0, tdir)
    testfiles = []
    for t in glob.glob(os.path.join(tdir, '*_test.py')):
        testfiles.append(os.path.splitext(os.path.basename(t))[0])
    tests = unittest.TestLoader().loadTestsFromNames(testfiles)
    t = unittest.TextTestRunner(stream=file(os.devnull, 'w'))
    t.run(tests)


def loop(count=300):
    pid = os.getpid()
    print 'pid:', os.getpid()
    for i in xrange(1):         # Allocate initial memory
        check_psi()
        check_arch()
        check_process(pid)
        check_test_suite()
    p = psi.process.Process(os.getpid())
    fmt = '%(n)s: rss: %(rss)s (%(pctrss)s%%) vsz: %(vsz)s (%(pctvsz)s%%) '
    fmt += 'refcnt: %(refcnt)d (%(increfcnt)+d)'
    n = 0
    startrss = p.rss
    startvsz = p.vsz
    startrefcnt = sys.gettotalrefcount()
    while n < count:
        check_psi()
        check_arch()
        check_process(pid)
        check_test_suite()
        p.refresh()
        print fmt % {'n': n,
                     'rss': p.rss,
                     'pctrss': p.rss*100/startrss,
                     'vsz': p.vsz,
                     'pctvsz': p.vsz*100/startvsz,
                     'refcnt': sys.gettotalrefcount(),
                     'increfcnt': sys.gettotalrefcount() - startrefcnt}
        n += 1
    p.refresh()
    print
    print 'RSS: %d - %d  diff=%+d (%d%%)' % (startrss, p.rss, p.rss-startrss,
                                             p.rss*100/startrss)
    print 'VSZ: %d - %d  diff=%+d (%d%%)' % (startvsz, p.vsz, p.vsz-startvsz,
                                             p.vsz*100/startvsz)
    endrefcnt = sys.gettotalrefcount() - 1
    print 'Refcount: %d - %d  diff=%+d (%d%%)' % (startrefcnt, endrefcnt,
                                                  endrefcnt-startrefcnt,
                                                  endrefcnt*100/startrefcnt)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        loop(int(sys.argv[1]))
    else:
        loop()
