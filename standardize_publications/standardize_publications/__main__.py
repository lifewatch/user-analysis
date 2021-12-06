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
        "-sl",
        "--standref_long",
        help="Specifies the mapping between affiliations and the standardized affiliation",
    )
    parser.add_argument(
        "-si",
        "--standref_info",
        help="Specifies the standardized affiliation data with extra info regarding country, flemish, category, QH-term, ...",
    )
    parser.add_argument(
        "-wd",
        "--wosdata",
        help="Specifies the folder with export from Web of Science (of publications with a WoS code)",
    )
    
    """
    # to do: implement choice of col and mode to standardize
    parser.add_argument(
        "-c",
        "--column",
        action="append",
        help="Specifies the columns that are to be standardized",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["exact", "fuzzy"],
        help="Specifies the mode used to standardize, either as exact match or fuzzy matches",
    )"""
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
    df = Standardizator(args.input, args.standref_long)
    print("Adding information from WoS-export")
    if args.wosdata is not None:
        df.add_wosinfo(args.wosdata)

    print("Standardizing affiliation information")
    if args.standref_long is not None:
        df.exactMatch(args.standref_long)
        df.similarityMatch(args.standref_long)

    #print("Adding other affiliation information")    
    #if args.standref_info is not None:
    #    df.add_affilinfo(args.standref_info)

    #print("Standardizing country")
    #df.add_standcountry()

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
