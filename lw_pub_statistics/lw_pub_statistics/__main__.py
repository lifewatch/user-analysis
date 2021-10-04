# -*- coding: utf-8 -*-
import argparse
import sys
import logging

from .LWStandardize import *

logname = 'lw_pub_statistics'
logfile = logname + '.log'
logging.basicConfig(level=logging.INFO, filename=logfile)
log = logging.getLogger(logname)


def get_arg_parser():
    """
    Defines the arguments to this script by using Python's [argparse](https://docs.python.org/3/library/argparse.html)
    """
    parser = argparse.ArgumentParser(description='Standardizes (lifewatch) publication data exported from IMIS',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-pubdata', '--publicationData', required=True, help='Specifies the folder with publication data')
    parser.add_argument('-refdata', '--referenceData', help='Specifies the folder with standardized data')
    parser.add_argument('-wosdata', '--wosExportData', help='Specifies the folder with export data from Web of Science (from publication with a WoS code)')
    parser.add_argument('-out', '--output', help='Specifies the file with updated/standardized publication data')

    return parser

def make_standardized(args: argparse.Namespace):
    df = Standardizator(args.publicationData)
    if args.wosExportData is not None:
        df.add_WOSaffil(args.wosExportData)
    if args.referenceData is not None:
        df.exactMatch(args.referenceData)
        #df.similarityMatch(args.referenceData)
    if args.output is not None:
        df.output(args.output)
    return df


def main():
    """
    The main entry point to this module.
    """
    args = get_arg_parser().parse_args()
    df = make_standardized(args)
    log.debug("df = %s" % df)

if __name__ == '__main__':
    main()
