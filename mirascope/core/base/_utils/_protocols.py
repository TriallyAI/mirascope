"""Protocols for reusable type hints."""

import inspect
from collections.abc import AsyncGenerator, Awaitable, Callable, Generator
from typing import (
    Any,
    Literal,
    ParamSpec,
    Protocol,
    TypeVar,
    overload,
)

from typing_extensions import TypeIs

from ..call_kwargs import BaseCallKwargs
from ..call_response_chunk import BaseCallResponseChunk
from ..message_param import BaseMessageParam
from ..tool import BaseTool

_BaseCallResponseChunkT = TypeVar(
    "_BaseCallResponseChunkT", covariant=True, bound=BaseCallResponseChunk
)
_BaseClientT = TypeVar("_BaseClientT", contravariant=True)
_BaseCallParamsT = TypeVar("_BaseCallParamsT", contravariant=True)
_BaseDynamicConfigT = TypeVar("_BaseDynamicConfigT", contravariant=True)
_ResponseT = TypeVar("_ResponseT", covariant=True)
_AsyncResponseT = TypeVar("_AsyncResponseT", covariant=True)
_ResponseChunkT = TypeVar("_ResponseChunkT", covariant=True)
_InvariantResponseChunkT = TypeVar("_InvariantResponseChunkT", contravariant=True)
_BaseToolT = TypeVar("_BaseToolT", bound=BaseTool)
_P = ParamSpec("_P")
_R = TypeVar("_R", contravariant=True)


class LLMFunctionDecorator(Protocol[_BaseDynamicConfigT, _ResponseT, _AsyncResponseT]):
    @overload
    def __call__(
        self, fn: Callable[_P, _BaseDynamicConfigT]
    ) -> Callable[_P, _ResponseT]: ...

    @overload
    def __call__(
        self, fn: Callable[_P, list[BaseMessageParam]]
    ) -> Callable[_P, _ResponseT]: ...

    @overload
    def __call__(
        self, fn: Callable[_P, Awaitable[_BaseDynamicConfigT]]
    ) -> Callable[_P, Awaitable[_AsyncResponseT]]: ...

    @overload
    def __call__(
        self, fn: Callable[_P, Awaitable[list[BaseMessageParam]]]
    ) -> Callable[_P, Awaitable[_AsyncResponseT]]: ...

    def __call__(
        self,
        fn: Callable[_P, _BaseDynamicConfigT]
        | Callable[_P, Awaitable[_BaseDynamicConfigT]]
        | Callable[_P, list[BaseMessageParam]]
        | Callable[_P, Awaitable[list[BaseMessageParam]]],
    ) -> Callable[_P, _ResponseT | Awaitable[_AsyncResponseT]]: ...  # pragma: no cover


class AsyncCreateFn(Protocol[_ResponseT, _ResponseChunkT]):
    @overload
    def __call__(
        self,
        *,
        stream: Literal[False] = False,
        **kwargs: Any,  # noqa: ANN401
    ) -> Awaitable[_ResponseT]: ...

    @overload
    def __call__(
        self,
        *,
        stream: Literal[True] = True,
        **kwargs: Any,  # noqa: ANN401
    ) -> Awaitable[AsyncGenerator[_ResponseChunkT, None]]: ...

    def __call__(
        self, *, stream: bool = False, **kwargs: Any
    ) -> Awaitable[
        _ResponseT | AsyncGenerator[_ResponseChunkT, None]
    ]: ...  # pragma: no cover


class CreateFn(Protocol[_ResponseT, _ResponseChunkT]):
    @overload
    def __call__(
        self,
        *,
        stream: Literal[False] = False,
        **kwargs: Any,  # noqa: ANN401
    ) -> _ResponseT: ...

    @overload
    def __call__(
        self,
        *,
        stream: Literal[True] = True,
        **kwargs: Any,  # noqa: ANN401
    ) -> Generator[_ResponseChunkT, None, None]: ...

    def __call__(
        self, *, stream: bool = False, **kwargs: Any
    ) -> _ResponseT | Generator[_ResponseChunkT, None, None]: ...


def fn_is_async(
    fn: Callable[_P, _R] | Callable[_P, Awaitable[_R]],
) -> TypeIs[Callable[_P, Awaitable[_R]]]:
    return inspect.iscoroutinefunction(fn)


class SetupCall(
    Protocol[
        _BaseClientT,
        _BaseDynamicConfigT,
        _BaseCallParamsT,
        _ResponseT,
        _ResponseChunkT,
        _BaseToolT,
    ]
):
    @overload
    def __call__(
        self,
        *,
        model: str,
        client: _BaseClientT | None,
        fn: Callable[..., Awaitable[_BaseDynamicConfigT]],
        fn_args: dict[str, Any],
        dynamic_config: _BaseDynamicConfigT,
        tools: list[type[BaseTool] | Callable] | None,
        json_mode: bool,
        call_params: _BaseCallParamsT,
        extract: bool,
    ) -> tuple[
        AsyncCreateFn[_ResponseT, _ResponseChunkT],
        str | None,
        list[Any],
        list[type[_BaseToolT]] | None,
        BaseCallKwargs,
    ]: ...

    @overload
    def __call__(
        self,
        *,
        model: str,
        client: _BaseClientT | None,
        fn: Callable[..., _BaseDynamicConfigT],
        fn_args: dict[str, Any],
        dynamic_config: _BaseDynamicConfigT,
        tools: list[type[BaseTool] | Callable] | None,
        json_mode: bool,
        call_params: _BaseCallParamsT,
        extract: bool,
    ) -> tuple[
        CreateFn[_ResponseT, _ResponseChunkT],
        str | None,
        list[Any],
        list[type[_BaseToolT]] | None,
        BaseCallKwargs,
    ]: ...

    def __call__(
        self,
        *,
        model: str,
        client: _BaseClientT | None,
        fn: Callable[..., _BaseDynamicConfigT | Awaitable[_BaseDynamicConfigT]],
        fn_args: dict[str, Any],
        dynamic_config: _BaseDynamicConfigT,
        tools: list[type[BaseTool] | Callable] | None,
        json_mode: bool,
        call_params: _BaseCallParamsT,
        extract: bool,
    ) -> tuple[
        CreateFn[_ResponseT, _ResponseChunkT]
        | AsyncCreateFn[_ResponseT, _ResponseChunkT],
        str | None,
        list[Any],
        list[type[_BaseToolT]] | None,
        BaseCallKwargs,
    ]: ...  # pragma: no cover


class HandleStream(
    Protocol[_InvariantResponseChunkT, _BaseCallResponseChunkT, _BaseToolT]
):
    def __call__(
        self,
        stream: Generator[_InvariantResponseChunkT, None, None],
        tool_types: list[type[_BaseToolT]] | None,
    ) -> Generator[
        tuple[_BaseCallResponseChunkT, _BaseToolT | None], None, None
    ]: ...  # pragma: no cover


class HandleStreamAsync(
    Protocol[_InvariantResponseChunkT, _BaseCallResponseChunkT, _BaseToolT]
):
    def __call__(
        self,
        stream: AsyncGenerator[_InvariantResponseChunkT, None],
        tool_types: list[type[_BaseToolT]] | None,
    ) -> AsyncGenerator[
        tuple[_BaseCallResponseChunkT, _BaseToolT | None], None
    ]: ...  # pragma: no cover


class GetJsonOutput(Protocol[_R]):
    def __call__(self, response: _R, json_mode: bool) -> str: ...  # pragma: no cover


class CalculateCost(Protocol):
    def __call__(
        self,
        input_tokens: int | float | None,
        output_tokens: int | float | None,
        model: str,
    ) -> float | None: ...  # pragma: no cover
