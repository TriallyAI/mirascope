"""The Mirascope Groq Module."""

from typing import TypeAlias

from groq.types.chat import ChatCompletionMessageParam

from ._call import groq_call
from ._call import groq_call as call
from .call_params import GroqCallParams
from .call_response import GroqCallResponse
from .call_response_chunk import GroqCallResponseChunk
from .dynamic_config import GroqDynamicConfig
from .stream import GroqStream
from .tool import GroqTool

GroqMessageParam: TypeAlias = ChatCompletionMessageParam

__all__ = [
    "call",
    "GroqDynamicConfig",
    "GroqCallParams",
    "GroqCallResponse",
    "GroqCallResponseChunk",
    "GroqMessageParam",
    "GroqStream",
    "GroqTool",
    "groq_call",
]
