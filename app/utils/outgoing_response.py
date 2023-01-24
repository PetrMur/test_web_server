from aiohttp import web


class ServerResponse:
    def __init__(self):
        self._data = None
        self.status_code = 200

    def as_json_data(self, data):
        """Prepare answer as json"""

        self._data = data
        return self

    def make_exception(self, data, status_code):
        """Create answer as exception"""

        self._data = data
        self.status_code = status_code
        return self

    def response_as_json(self):
        """Return json data"""

        if isinstance(self._data, str):
            return web.Response(body=self._data, status=self.status_code)
        else:
            return web.json_response(self._data, status=self.status_code)
