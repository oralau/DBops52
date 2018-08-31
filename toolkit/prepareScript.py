#!/usr/bin/env python
# encoding: utf-8
import argparse


class prepareScript():

    def printScript(self):

        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", help="print script",
                            action="store_true")
        return parser.parse_args()



        # if args.verbose:
        #         print "verbosity turned on"