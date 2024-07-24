import urllib.request, json


"""
REST API to access third party stock information
"""
class Stocks(object):

    def __init__(self, host, api_key):
        self.host = host
        self.headers = headers = {'Albert-Case-Study-API-Key': api_key}

    #TODO put in try catch block with error handeling and alerting around them

    def get_tickers(self):
        url = "https://" + self.host + "/casestudy/stock/tickers/"
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req) as response:
            response = response.read()
            return json.loads(response)

    def get_prices(self, tickers):
        url = "https://" + self.host + "/casestudy/stock/prices/?tickers=" + ",".join(tickers) # normally want to encode this
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req) as response:
            response = response.read()
            return json.loads(response)

