import json


class Response:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        response_bak = response
        if (response.status_code // 100 == 2):
            try:
                if not response.data.has_key(swagger):
                    response.data = {"status": True, "detail": response.data,
                                     "error_detail": {}}
                    response.content = json.dumps(response.data)
            except:
                response = response_bak

        else:
            try:

                response.data = {"status": False, "detail": {},
                                 "error_detail": response.data}
                response.content = json.dumps(response.data)
            except:
                response = response_bak
        return response
