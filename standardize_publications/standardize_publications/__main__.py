# -*- coding: utf-8 -*-
import argparse
import sys
import logging

from .standardize import *

"""from .LWlabels import *"""

logname = "standardize_publications"
logfile = logname + ".log"
logging.basicConfig(level=logging.INFO, filename=logfile)
log = logging.getLogger(logname)


def get_arg_parser():
    """
    Defines the arguments to this script by using Python's [argparse](https://docs.python.org/3/library/argparse.html)
    """
    parser = argparse.ArgumentParser(
        description="Standardizes (lifewatch) publication data exported from IMIS",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i",
        "--input",
        help="Specifies the input publications that are to be standardized",
    )
    parser.add_argument(
        "-srf",
        "--standreffile",
        help="Specifies the file with standardized affiliation data",
    )
    parser.add_argument(
        "-wd",
        "--wosdata",
        help="Specifies the folder with export from Web of Science (of publications with a WoS code)",
    )
    # to do: move this within make_standardized function
    parser.add_argument(
        "-c",
        "--column",
        choices=["Affiliation", "wos_affil"],
        help="Specifies the column used to match similarity against in the reference data",
    )
    parser.add_argument(
        "-m",
        "--method",
        choices=["Affiliation", "wos_affil"],
        help="Specifies the column used to match similarity against in the reference data",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Specifies the output file of livewatch publications with added standardized affiliation information",
    )
    """parser.add_argument(
        "-labelfile", "--labelFile", help="Specifies the file with label information"
    )"""

    return parser


def make_standardized(args: argparse.Namespace):
    df = Standardizator(args.input, args.standreffile)
    print("Adding information from WoS-export")
    if args.wosdata is not None:
        df.add_wosinfo(args.wosdata)

    """if args.column is not None and args.method is not None:
        df.standardize(args.column, args.method)"""

    """if args.standdata is not None:
        df.to_file(folder=args.standdata)"""

    print("Writing dataframe to output-file")
    if args.output is not None:
        df.to_file(args.output)
    return df


"""def make_labelled(args: argparse.Namespace):
    df = Labeller(args.standardizedData)
    if args.labelfile is not None:
        df.add_label(args.labelfile)
    return df"""


def main():
    """
    The main entry point to this module.
    """
    args = get_arg_parser().parse_args()

    if args.input is not None:
        df = make_standardized(args)

    """if args.standardizedData is not None:
        df = make_labelled(args)"""

    log.debug("df = %s" % df)


if __name__ == "__main__":
    main()
