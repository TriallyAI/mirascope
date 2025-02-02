"""The Mirascope Cohere Module."""

from typing import TypeAlias

from cohere.types import ChatMessage

from ._call import cohere_call
from ._call import cohere_call as call
from .call_params import CohereCallParams
from .call_response import CohereCallResponse
from .call_response_chunk import CohereCallResponseChunk
from .dynamic_config import CohereDynamicConfig
from .stream import CohereStream
from .tool import CohereTool

CohereMessageParam: TypeAlias = ChatMessage

__all__ = [
    "call",
    "CohereDynamicConfig",
    "CohereCallParams",
    "CohereCallResponse",
    "CohereCallResponseChunk",
    "CohereMessageParam",
    "CohereStream",
    "CohereTool",
    "cohere_call",
]
