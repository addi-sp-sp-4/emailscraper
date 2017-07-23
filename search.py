import requests
import subprocess
import json

from duckduckgo import DuckDuckGo



def search(functions, args):

    json_cfg = json.loads(open('json/data.json').read())
    urls = []
    out = open(args.out_file, 'a')

    engine_objects = []

    if "search-term-stdin" in functions:

        terms = [args.search_term]

    elif "search-terms-file" in functions:
        terms = open(args.search_terms_file).read().split('\n')

    elif "search-terms-random" in functions:
        # query to get random terms from dictionary
        terms = subprocess.check_output(['shuf', json_cfg["config"]["random-terms"]["dictionary"]]).split('\n')[:int(args.search_terms_random_amount)]

    # Cleaning up
    terms = [x for x in terms if x != ""]

    for term in terms:
        engine_objects = []
        if "search-engine-specific" in functions:

            engine = args.search_engine

            if engine == "duckduckgo":

                engine_objects = [DuckDuckGo(term)]

        elif "search-engine-all" in functions:
            engine_objects.append(DuckDuckGo(term))

        for engine in engine_objects:

            for page in range(int(args.search_pages)):
                try:
                    links = engine.get_links()
                except AttributeError:
                    print "No more search results..."
                    break

                print "Fetched results for {}, page {}, on engine {}".format(term, page + 1, engine.name)
                urls.extend(links)

                # Use limited amount of memory
                if len(urls) > 256:
                    print "Writing to file; Fetched more than 256 urls"
                    for i in urls:
                        if i.startswith('http://') or i.startswith('https://'):
                            out.write(i + '\n')

                    urls = []

    print "Writing to file..."
    for i in urls:
        if i.startswith('http://') or i.startswith('https://'):
            out.write(i + '\n')


