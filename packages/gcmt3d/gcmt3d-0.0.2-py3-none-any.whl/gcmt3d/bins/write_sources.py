#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script will create the perturbed Moment tensors in the perturbation
directories.


:copyright:
    Lucas Sawade (lsawade@princeton.edu)
:license:
    GNU Lesser General Public License, version 3 (LGPLv3)
    (http://www.gnu.org/licenses/lgpl-3.0.en.html)

Last Update: January 2020
"""

from gcmt3d.workflow.generate_sources import write_sources
import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', dest='filename',
                        help='Path to CMTSOLUTION file',
                        required=True, type=str)
    parser.add_argument('-p', dest='param_path',
                        help='Path to param directory',
                        required=True, type=str)
    args = parser.parse_args()

    # Run
    write_sources(args.filename, args.param_path)


if __name__ == "__main__":
    main()
