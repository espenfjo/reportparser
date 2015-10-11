#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import os
from reportparser import PDFReportparser, datetime_serialiser, HTMLReportparser
from reportparser.configreader import parse_config

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

import simplejson
from sys import stderr


def main():
    """
    Tool to do magic
    """
    conf_parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)

    conf_parser.add_argument('-c', '--config',
                             help="Configuration file",
                             default="~/.reportparser.conf",
                             type=str)
    args, remaining_argv = conf_parser.parse_known_args()

    parser = argparse.ArgumentParser(
        parents=[conf_parser],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__
    )
    parser.add_argument('-d', '--disable-database',
                        help="Disable database storage",
                        action="store_true")

    parser.add_argument('-q', '--quiet',
                        help="Disable output to terminal",
                        action="store_true")

    parser.add_argument('-s', '--no-save',
                        help="Do not save document to storage",
                        action="store_true")

    parser.add_argument('report', nargs='+', help="PDF reports to parse")


    if os.path.isfile(args.config):
        config_obj = parse_config(args.config)
        parser.set_defaults(**config_obj)
    args = parser.parse_args(remaining_argv)

    for report in args.report:
        if report.endswith(".pdf"):
            parser = PDFReportparser(report, args)
        else:
            parser = HTMLReportparser(report, args)

        parser.process()

    if not args.disable_database:
        parser.store_database(parser.result)

    if not args.quiet:
        print(simplejson.dumps(parser.result, sort_keys=True, indent=4, default=datetime_serialiser))


if __name__ == '__main__':
    main()
