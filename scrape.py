import requests
import re
import json

def scrape(functions, args):



    # emailregex.com
    regexp = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    json_cfg = json.loads(open('json/data.json').read())

    if "scrape-url-stdin" in functions:
        urls = [args.url]

    elif "scrape-urls-file" in functions:
        urls = open(args.urls_file).read().split('\n')

        # Cleaning up
        urls = [x for x in urls if x != ""]

    for url in urls:
        try:
            r = requests.get(url, headers = json_cfg["config"]["dummy_headers"])
        except:
            continue

        emails = re.findall(regexp, r.content)

        emails = list(set([x.lower for x in emails if not x.endswith('.png') and not x.endswith('.jpg')]))
        if len(emails) > 0:
            print "Email(s) found! {}.".format(', '.join(emails))
            print "Writing to file..."
            out = open(args.out_file, 'a')
            for email in emails:
                    out.write(email + '\n')

            out.close()
