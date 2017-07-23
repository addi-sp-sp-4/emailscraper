#!/usr/bin/env python2.7

import json
import optparse
import subprocess

from return_functions import return_functions
from search import search
from scrape import scrape

json_cfg = json.loads(open('json/data.json').read())

page_number_def = json_cfg["config"]["pages"]["page-number"]
random_term_number_def = json_cfg["config"]["random-terms"]["random-term-number"]

parser = optparse.OptionParser()
parser.add_option("--search", "-s", help="Search for one or more terms", default=False, action="store_true")
parser.add_option("--search-engine", "-e", help="Used with --search. If omitted, all available engines will be used", default=False, action="store")
parser.add_option("--search-term", "-t", help="Used with --search. Searches for a term.", default=False, action="store")
parser.add_option("--search-terms-file", help="Used with --search. Searches for all terms in a file. Terms should be seperated with a newline", default=False, action="store")
parser.add_option("--search-terms-random", help="Used with --search. Selects random terms to search. The amount of terms can be set with --search-terms-random-amount", default=False, action="store_true")
parser.add_option("--search-terms-random-amount", help="Used with --search and --search-terms-random, amount of terms randomly generated. default = {}".format(random_term_number_def), default=random_term_number_def, action="store")
parser.add_option("--search-pages", "-p", help="Used with --search. Amount of pages where the links should be extracted from per term per engine, default is {}".format(page_number_def), default=page_number_def, action="store")

parser.add_option("--out-file", "-o", help="Used with --search AND --scrape-email. Outfile", default=False, action="store")

parser.add_option("--scrape-email", "-S", help="Scrape emails from one or more terms", default=False, action="store_true")
parser.add_option("--url", "-u", help="Used with --scrape-email. URL to search for email adresses", default=False, action="store")
parser.add_option("--urls-file", help="Used with --scrape-email. File with URLs, divided with a newline. --search generates such files", default=False, action="store")

(args, _) = parser.parse_args()

functions = return_functions(args)

if functions == "ERR_MISSING_ARGUMENT":
    parser.print_help()
    exit()

elif functions == "ERR_INVALID_ENGINE":
    print "Invalid search engine chosen, please choose from {}".format(', '.join(json_cfg["search_engines"]["available_search_engines"]))
    exit()
elif functions == "ERR_NO_OUTFILE":
    print "Please set an outfile. --out-file or -o"
    exit()

if "search" in functions:
    search(functions, args)

    subprocess.Popen(['sort', '-u', args.out_file, '-o', args.out_file])

    print "Removing duplicate entries..."

elif "scrape" in functions:
    scrape(functions, args)

    subprocess.Popen(['sort', '-u', args.out_file, '-o', args.out_file])

    print "Removing duplicate entries..."