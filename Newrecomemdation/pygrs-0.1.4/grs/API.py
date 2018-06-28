import falcon
import json
from waitress import serve

class model_deploy():
    def give_result(self, request_json):
        if "id" not in request_json:
            raise deploy_error("api error", "message")
        result = {
            'request': request_json,
            'massage': 'Please inherit the class'
        }
        return json.dumps(result, ensure_ascii=False)

class deploy_error(Exception):
    def __init__(self, title, message):
        super().__init__(message)
        self.title = title
        self.message = message


class rest_api():
    def __init__(self, deploy_model):
        self.deploy_model = deploy_model

    def on_post(self, req, resp):
        request_body = json.loads(req.stream.read())
        try:
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = self.deploy_model.give_result(request_body)
        except deploy_error as e:
            raise falcon.HTTPBadRequest(
                e.title,
                e.message
            )


class api_route():
    def __init__(self):
        self.apis = falcon.API()

    def add_api(self, model, route):
        self.apis.add_route(route, model)

    def serve_api(self, host_address, api_port):
        serve(self.apis, host= host_address, port=api_port)


