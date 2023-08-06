#! /usr/bin/env python

# This file is part of IVRE.
# Copyright 2011 - 2020 Pierre LALET <pierre@droids-corp.org>
#
# IVRE is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IVRE is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IVRE. If not, see <http://www.gnu.org/licenses/>.


"""Parse NMAP scan results and add them in DB."""


from __future__ import print_function
import os
import sys


import ivre.db
import ivre.utils
import ivre.xmlnmap

from ivre.view import nmap_record_to_view


def recursive_filelisting(base_directories):
    "Iterator on filenames in base_directories"

    for base_directory in base_directories:
        for root, _, files in os.walk(base_directory):
            for leaffile in files:
                yield os.path.join(root, leaffile)


def main():
    parser, use_argparse = ivre.utils.create_argparser(__doc__,
                                                       extraargs='scan')
    if use_argparse:
        parser.add_argument('scan', nargs='*', metavar='SCAN',
                            help='Scan results')
    parser.add_argument('-c', '--categories', default='',
                        help='Scan categories.')
    parser.add_argument('-s', '--source', default=None,
                        help='Scan source.')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Test mode (JSON output).')
    parser.add_argument('--test-normal', action='store_true',
                        help='Test mode ("normal" Nmap output).')
    parser.add_argument('--ports', '--port', action='store_true',
                        help='Store only hosts with a "ports" element.')
    parser.add_argument('--open-ports', action='store_true',
                        help='Store only hosts with open ports.')
    parser.add_argument('--masscan-probes', nargs='+', metavar='PROBE',
                        help='Additional Nmap probes to use when trying to '
                        'match Masscan results against Nmap service '
                        'fingerprints.')
    parser.add_argument('--force-info', action='store_true',
                        help='Force information (AS, country, city, etc.)'
                        ' renewal (only useful with JSON format)')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Import all files from given directories.')
    parser.add_argument('--update-view', action='store_true',
                        help='Merge hosts in current view')
    parser.add_argument('--no-update-view', action='store_true',
                        help='Do not merge hosts in current view (default)')
    args = parser.parse_args()
    database = ivre.db.db.nmap
    categories = args.categories.split(',') if args.categories else []
    if args.test:
        args.update_view = False
        args.no_update_view = True
        database = ivre.db.DBNmap()
    if args.test_normal:
        args.update_view = False
        args.no_update_view = True
        database = ivre.db.DBNmap(output_mode="normal")
    if args.recursive:
        scans = recursive_filelisting(args.scan)
    else:
        scans = args.scan
    if not args.update_view or args.no_update_view:
        callback = None
    else:
        def callback(x):
            return ivre.db.db.view.store_or_merge_host(
                nmap_record_to_view(x)
            )
    count = 0
    error = False
    for scan in scans:
        try:
            if database.store_scan(
                    scan,
                    categories=categories, source=args.source,
                    needports=args.ports, needopenports=args.open_ports,
                    force_info=args.force_info,
                    masscan_probes=args.masscan_probes, callback=callback,
            ):
                count += 1
        except Exception:
            ivre.utils.LOGGER.warning("Exception (file %r)", scan,
                                      exc_info=True)
            error = True
    ivre.utils.LOGGER.info("%d results imported.", count)
    sys.exit(error)
