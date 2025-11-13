#!/usr/bin/env python3
import argparse
from crawler import main_crawler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--Domain", help="Starts with http")
    args = parser.parse_args()

    if args.Domain:
        main_crawler(args.Domain)
    else:
        print("\n\nStarting domain must be input after command name and -D flag: ")
        print("./main.py -D https://www.example.com\n\n")
