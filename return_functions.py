import json

def return_functions(args):

    # Located in emailscraper.py
    json_cfg = json.loads(open('json/data.json').read())

    functions = []

    if args.search:

        functions.append('search')

        if args.search_engine:

            if args.search_engine not in json_cfg["search_engines"]["available_search_engines"]:

                return "ERR_INVALID_ENGINE"

            functions.append('search-engine-specific')

        else:

            functions.append('search-engine-all')

        if args.search_terms_file:

            functions.append('search-terms-file')

        elif args.search_term:

            functions.append('search-term-stdin')

        elif args.search_terms_random_amount:
            functions.append('search-terms-random')

        else:

            return "ERR_MISSING_ARGUMENT"

    elif args.scrape_email:

        functions.append('scrape')

        if args.urls_file:
            functions.append('scrape-urls-file')

        elif args.url:

            functions.append('scrape-url-stdin')

        else:

            return "ERR_MISSING_ARGUMENT"

    else:

        return "ERR_MISSING_ARGUMENT"

    if not args.out_file:
        return "ERR_NO_OUTFILE"

    return functions