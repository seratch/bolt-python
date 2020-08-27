import azure.functions as func
from slack_bolt import App
import logging


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.basicConfig(level=logging.DEBUG)

    app = App()

    @app.event("app_mention")
    def hi(body, say, logger):
        logger.info(body)
        user_id = body["event"]["user"]
        say(f"Hi <@{user_id}>!")

    handler = SlackRequestHandler(app)
    return handler.handle(req)


# -------------------------------
from typing import Dict, List, Optional

import azure.functions as func

from slack_bolt.oauth import OAuthFlow
from slack_bolt.request import BoltRequest
from slack_bolt.response import BoltResponse


class SlackRequestHandler:
    def __init__(self, app: App):  # type: ignore
        self.app = app

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        logger.addHandler(sh)

        if self.app.oauth_flow is not None:
            self.app.oauth_flow.redirect_uri_page_renderer.install_path = "?"

    def handle(self, req: func.HttpRequest) -> func.HttpResponse:
        if req.method == "GET":
            if self.app.oauth_flow is not None:
                oauth_flow: OAuthFlow = self.app.oauth_flow
                bolt_req = to_bolt_request(req)
                query = bolt_req.query
                is_callback = query is not None and (
                    (
                        _first_value(query, "code") is not None
                        and _first_value(query, "state") is not None
                    )
                    or _first_value(query, "error") is not None
                )
                if is_callback:
                    bolt_resp = oauth_flow.handle_callback(bolt_req)
                    return to_func_response(bolt_resp)
                else:
                    bolt_resp = oauth_flow.handle_installation(bolt_req)
                    return to_func_response(bolt_resp)
        elif req.method == "POST":
            bolt_resp: BoltResponse = self.app.dispatch(to_bolt_request(req))
            return to_func_response(bolt_resp)

        return func.HttpResponse(body="Not Found", status_code=404)


def to_bolt_request(req: func.HttpRequest) -> BoltRequest:
    return BoltRequest(
        body=req.get_body().decode("utf-8"),
        query=req.params,
        headers=req.headers,
    )


def to_func_response(bolt_resp: BoltResponse) -> func.HttpResponse:
    return func.HttpResponse(
        body=bolt_resp.body,
        status_code=bolt_resp.status,
        headers=bolt_resp.first_headers(),
    )


def _first_value(query: Dict[str, List[str]], name: str) -> Optional[str]:
    if query:
        values = query.get(name, [])
        if values and len(values) > 0:
            return values[0]
    return None