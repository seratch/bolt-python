from typing import List, Optional, Union

from slack_sdk.web import WebClient
from slack_sdk.models.blocks import Block


class Configure:
    def __init__(self, *, callback_id: str, client: WebClient, body: dict):
        self.callback_id = callback_id
        self.client = client
        self.body = body

    def __call__(self, *, blocks: Optional[List[Union[dict, Block]]] = None,) -> None:
        self.client.views_open(
            trigger_id=self.body["trigger_id"],
            view={
                "type": "workflow_step",
                "callback_id": self.callback_id,
                "blocks": blocks,
            },
        )
