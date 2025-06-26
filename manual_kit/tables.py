from typing import Callable


class WorldSpecTable[Data, Spec]:
    def __init__(self, name: str, create_spec: Callable[[str, Data], Spec]) -> None:
        self.name = name
        self._items: dict[str, Data] = {}
        self.__create_spec = create_spec

    def add(self, name: str, data: Data) -> Spec:
        if name in self._items:
            raise Exception(f"Item {name} already exists in {self.name}")

        spec = self.__create_spec(name, data)
        self._items[name] = data
        return spec

    @property
    def values(self):
        return self._items.values()

    @property
    def keys(self):
        return self._items.values()


class WorldSpecList[Data, Spec](WorldSpecTable[Data, Spec]):
    @property
    def data(self) -> list[Data]:
        return [data for data in self._items.values()]


class WorldSpecDict[Data, Spec](WorldSpecTable[Data, Spec]):
    @property
    def data(self) -> dict[str, Data]:
        return {name: data for name, data in self._items.items()}
