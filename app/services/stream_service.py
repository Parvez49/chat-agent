import json
from typing import Callable, Optional, Union, Any
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk


class StreamHandler(BaseCallbackHandler):

    def __init__(self, send_token: Callable[[str], None]):
        self.send_token = send_token

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        self.send_token(json.dumps({"token": token}) + "\n\n")


async def stream_response_sse(chain, query: str):
    """
    Stream token from chain as SSE
    :param chain:
    :param query:
    :return:
    """
    buffer = []

    def send_token(event_data: str):
        buffer.append(f"data: {event_data}")

    handler = StreamHandler(send_token)
    chain.llm.callbacks = [handler]
    chain.run(query)

    for chunk in buffer:
        yield chunk
