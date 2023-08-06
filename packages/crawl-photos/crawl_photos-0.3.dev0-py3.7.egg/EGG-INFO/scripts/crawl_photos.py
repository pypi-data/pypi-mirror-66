# -*- coding: utf-8 -*-

__version__ = '0.3-dev'
__author__ = 'mcwT'

import argparse


def main():
    parser = argparse.ArgumentParser(description="According to enter parameters crawl photos")
    parser.add_argument('-n', '--number', type=int, help='Number of photos')
    parser.add_argument('-base64', '--output_base64', help='Output a base64 to csv file')
    parser.add_argument('-file', '--output_file', help='Output a photos folder', default=False)
    parser.add_argument('-ofp', '--output_file_path', help='Output file path. Save to current directory by default.',
                        default='.')

    args = parser.parse_args()

    express_code = args.code

    if express_code is None:
        print("hello world")
    else:
        print("no express_code")
