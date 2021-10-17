# -*- coding: utf-8 -*-
import argparse
import sys
import logging

from .LWStandardize import *
from .LWlabels import *

logname = 'lw_pub_statistics'
logfile = logname + '.log'
logging.basicConfig(level=logging.INFO, filename=logfile)
log = logging.getLogger(logname)


def get_arg_parser():
    """
    Defines the arguments to this script by using Python's [argparse](https://docs.python.org/3/library/argparse.html)
    """
    parser = argparse.ArgumentParser(
        description='Standardizes (lifewatch) publication data exported from IMIS',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-pubdata',
        '--publicationData',
        help='Specifies the folder with publication data')
    parser.add_argument(
        '-reffile',
        '--referenceFile',
        help='Specifies the file with standardized data')
    parser.add_argument(
        '-wosdata',
        '--wosExportData',
        help='Specifies the folder with export data from Web of Science (from publication with a WoS code)')
    parser.add_argument(
        '-col',
        '--column',
        choices=['Affiliation', 'wos_affil'],
        help='Specifies the column used to match similarity against in the reference data')
    parser.add_argument(
        '-standdata',
        '--standardizedData',
        help='Specifies the folder with standardized data')
    parser.add_argument(
        '-labelfile',
        '--labelFile',
        help='Specifies the file with label information')

    return parser


def make_standardized(args: argparse.Namespace):
    df = Standardizator(args.publicationData)
    if args.wosExportData is not None:
        df.add_WOSaffil(args.wosExportData)
        df.add_WOScountry(args.wosExportData)
        df.add_WOSpluskeywords(args.wosExportData)
    if args.referenceFile is not None:
        # df.exactMatch(args.referenceFile)
        if args.column is not None:
            df.similarityMatch(args.referenceFile, args.column)

    return df


def make_labelled(args: argparse.Namespace):
    df = Labeller(args.standardizedData)
    if args.labelfile is not None:
        df.add_label(args.labelfile)
    return df


def main():
    """
    The main entry point to this module.
    """
    args = get_arg_parser().parse_args()

    if args.publicationData is not None:
        df = make_standardized(args)

    if args.standardizedData is not None:
        df = make_labelled(args)

    log.debug("df = %s" % df)


if __name__ == '__main__':
    main()
