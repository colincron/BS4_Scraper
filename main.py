#!/usr/bin/env python3
import argparse
from functions import main_crawler

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--Domain", help="Starts with http")
    parser.add_argument("-c", "--concurrency", type=int, default=10, help="Number of concurrent requests (default: 10)")
    args = parser.parse_args()

    if args.Domain:
        main_crawler(args.Domain, args.concurrency)
    else:
        print("\n\nStarting domain must be input after command name and -D flag: ")
        print("./main.py -D https://www.example.com\n\n")
