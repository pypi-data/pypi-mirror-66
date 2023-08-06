class GandiAuth:
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, req):
        req.headers["Authorization"] = f"Apikey {self.api_key}"
        return req
