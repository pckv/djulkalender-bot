from __future__ import annotations

from asyncio import StreamReader, StreamWriter
from dataclasses import dataclass
from typing import Awaitable, Callable, Protocol


@dataclass
class Context:
    """Context for a command to be used by the command callback."""
    author: str
    say: Callable[[str], Awaitable[None]]
    send: Callable[[str], Awaitable[None]]
    reader: StreamReader
    writer: StreamWriter
    commands: list[Command]


class CommandCallback(Protocol):
    """A callback for a executing a command."""
    __name__: str

    async def __call__(self, ctx: Context, *args: str) -> None:
        ...


@dataclass
class Command:
    """A command that can be executed by the bot."""
    name: str
    description: str
    callback: CommandCallback
    min_args: int
