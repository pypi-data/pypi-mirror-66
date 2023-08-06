# -*- coding: utf-8 -*-

__version__ = '0.2-dev'
__author__ = 'mcwT'

import argparse


def main():
    parser = argparse.ArgumentParser(description="According to enter parameters crawl photos")
    parser.add_argument('-n', '--number', type=int, help='Number of photos')
    parser.add_argument('-base64', '--output', help='Output a base64 to csv file')
    parser.add_argument('-file', '--output', help='Output a photos folder', default=False)
    parser.add_argument('-ofp', '--output_file_path', help='Output file path. Save to current directory by default.',
                        default='.')

    print("hello world")
