import requests

class Request:

    def __init__(self, url: str, headers: Dict, data: Dict):
        self.url = url
        self.headers = headers
        self.data = data
    
    def exceute_request(self, method: str):
        match method:
            case "GET":
                requests.get(self.url, self.headers, self.data)
            case "POST":
                requests.post(self.url, self.headers, self.data)



