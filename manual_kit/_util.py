from typing import Mapping, Protocol, Sequence

type JsonValue = JsonObject | JsonArray | str | int | float | bool | None
type JsonArray = Sequence[JsonValue]
type JsonObject = Mapping[str, JsonValue]


def omit[K, V](input: Mapping[K, V], *keys: K) -> dict[K, V]:
    return {key: input[key] for key in input if not key in keys}


def compact[K, V](input: Mapping[K, V | None]) -> dict[K, V]:
    return {k: v for k, v in input.items() if v != None}


class Named(Protocol):
    name: str


def list_names(items: Sequence[Named]) -> list[str]:
    return [item.name for item in items]


def list_names_or_none(items: Sequence[Named] | None) -> list[str] | None:
    return [item.name for item in items] if items else None
