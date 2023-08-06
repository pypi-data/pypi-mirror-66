#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Script to copy test result ref.new files into local test directories to avoid re-running the tests locally

usage:
  GetNightlyRefs.py.py slot [day(=today)] [application(=cwd)] [destination(=pwd)] [--help]

options:
  day is today if not specified
  application is taken from the current directory name if not specified
  destination, where to put the references, starts at the current working directory unless specified.
  If no destination is given, local references will be updated, but new directories will not be added.

  cmtconfig is always taken from the corresponding environment variable
  the ordering of options is fixed.

standard usage:
  check your local cmtconfig
  setup local project structure for the correct project
  get the packages you want to update
  go to the PROJECT_version top directory
  call this script
  go through and replace the references you want to update

"""
from __future__ import print_function

import time
import os
import sys

from zipfile import ZipFile
from StringIO import StringIO
from urllib2 import HTTPError

from LbEnv import fixProjectCase

CHECK_SSL = False


def urlopen(url):
    """
    Wrapper for urllib2.urlopen to enable or disable SSL verification.
    """
    import urllib2
    if not CHECK_SSL and sys.version_info >= (2, 7, 9):
        # with Python >= 2.7.9 SSL certificates are validated by default
        # but we can ignore them
        from ssl import SSLContext, PROTOCOL_SSLv23
        return urllib2.urlopen(url, context=SSLContext(PROTOCOL_SSLv23))
    return urllib2.urlopen(url)


def usage():
    print(__doc__)


def guess_project_name():
    proj = os.path.basename(os.getcwd())
    if '_' in proj:
        proj = proj.split('_', 1)[0]
    if proj.endswith('Dev'):
        proj = proj[:-3]
    return fixProjectCase(proj)


def main():
    # if set to True, do not extract files if the directory is missing
    ignore_missing_dirs = True

    if "--help" in sys.argv or "-h" in sys.argv:
        usage()
        sys.exit(0)

    if len(sys.argv) < 2 or len(sys.argv) > 5:
        usage()
        raise AttributeError("Incorrect number of options")

    # usage()
    args = sys.argv[1:]

    slot = args.pop(0)
    day = args.pop(0) if args else time.strftime('%a')
    app = fixProjectCase(args.pop(0)) if args else guess_project_name()
    if args:
        dest = args.pop(0)
        ignore_missing_dirs = False
    else:
        dest = os.curdir

    for k, v in (('slot', slot), ('app', app), ('day', day), ('dest', dest)):
        if not v.strip():
            usage()
            print(k, v)
            raise ValueError("Could not parse option")

    platform = os.environ.get('BINARY_TAG') or os.environ.get('CMTCONFIG')
    if not platform:
        raise RuntimeError('Nither BINARY_TAG nor CMTCONFIG is set')

    print("looking for slot: %s, day: %s, app: %s, platform: %s" %
          (slot, day, app, platform))

    arch_url = (
        'https://lhcb-nightlies-artifacts.web.cern.ch/lhcb-nightlies-artifacts/'
        '{flavour}/{slot}/{day}/tests/{platform}/newrefs/{project}.zip'
    ).format(
        slot=slot, day=day, project=app, platform=platform, flavour='nightly')

    try:
        print("Getting data from:", arch_url)
        arch_data = urlopen(arch_url).read()
    except HTTPError:
        # treat HTTP errors as "no data available"
        arch_data = None

    if not arch_data:
        print('cannot find data for the requested combination')
        exit(1)

    arch = ZipFile(StringIO(arch_data))

    print('Extracting', 'specific' if ignore_missing_dirs else 'all',
          'refs...')

    def should_extract(filename):
        '''
        Tell if a filename should be extracted.
        '''
        return (not ignore_missing_dirs  # True means extract everything
                or (not filename.endswith('/')  # ignore directories
                    and os.path.isdir(os.path.dirname(filename))))

    for info in arch.infolist():
        if should_extract(info.filename):
            if dest == os.curdir:
                print(info.filename)
            else:
                print(info.filename, '->', os.path.join(dest, info.filename))

            arch.extract(info, path=dest)


if __name__ == '__main__':
    main()
