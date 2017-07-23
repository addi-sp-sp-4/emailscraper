import requests
import re
import json
import urllib


class DuckDuckGo:
    """
    Class to handle extracting the URLS from DuckDuckGo search results
    """

    def __init__(self, query):
        self.name = "DuckDuckGo"
        self.query = urllib.quote(query, safe='')
        self.base_url = "https://duckduckgo.com/{}".format(self.query)

        self.instance_id_required = True
        self.instance_id = self.get_instance_id()
        self.multiplier = 0

    def get_instance_id(self):
        """
        For every search term, a instance id is given, which we need to give to the 'vqd' parameter later to fetch search results
        The value of this instance id is stored on duckduckgo.com/{search_term}, we are retrieving it with the regex "vqd=\'(\d+)\'"
        """

        json_cfg = json.loads(open('json/data.json').read())
        r = requests.get(self.base_url, headers=json_cfg["config"]["dummy_headers"])
        return re.search("vqd=\'(\d+)\'", r.content).group(1)

    def get_links(self):
        """
        We need to extract all urls from the results. There is a json object hidden in the response, with some handy regex we can retrieve it
        """

        json_cfg = json.loads(open('json/data.json').read())
        r = requests.get("https://duckduckgo.com/d.js?q={query}&s={skips}&vqd={instance_id}".format(query = self.query, skips = 30 * self.multiplier, instance_id=self.instance_id), headers=json_cfg["config"]["dummy_headers"])

        urls = re.search("\"en\":\[([^\];]+)\]", r.content).group(1).replace("\"", "").split(',')

        self.multiplier += 1
        return urls

if __name__ == '__main__':
    ddg = DuckDuckGo('foo bars')

    ddg.get_links()
