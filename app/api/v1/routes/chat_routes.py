from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

from app.schemas.query import Query
from app.services.query_service import get_replay, stream_replay
from app.services.query_service import qa
from app.services.stream_service import stream_response_sse

router = APIRouter()


@router.post("/chat/")
def chat(query: Query):
    replay = get_replay(query.query)
    return JSONResponse(
        content={"replay": replay},
        status_code=status.HTTP_200_OK
    )



@router.post("/chat/stream/")
def chat_stream(query: Query):
    async def event_generator():
        async for chunk in stream_replay(query.query):
            # Each chunk must be bytes
            yield f"data: {chunk}\n\n".encode("utf-8")

    return StreamingResponse(event_generator(), media_type="text/event-stream")
