from typing import Any


class Node:
    def __init__(
        self, key: Any, value: Any, hash_value: int
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value


class Dictionary:
        def __init__(
        self,
        initial_capacity: int = 8,
        load_factor: float = 0.7
    ) -> None:
        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._size = 0
        self._buckets: list[Node | None] = (
            [None] * self._capacity
        )

    def __len__(self) -> int:
        return self._size

    def _get_hash(self, key: Any) -> int:
        return hash(key)

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0

        for node in old_buckets:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size / self._capacity >= self._load_factor:
            self._resize()

        hash_value = self._get_hash(key)
        index = hash_value % self._capacity

        original_index = index
        while self._buckets[index] is not None:
            node = self._buckets[index]
            if node.hash == hash_value and node.key == key:
                node.value = value
                return
            index = (index + 1) % self._capacity
            if index == original_index:
                break

        self._buckets[index] = Node(
            key, value, hash_value
        )
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        hash_value = self._get_hash(key)
        index = hash_value % self._capacity

        original_index = index
        while self._buckets[index] is not None:
            node = self._buckets[index]
            if node.hash == hash_value and node.key == key:
                return node.value
            index = (index + 1) % self._capacity
            if index == original_index:
                break

        raise KeyError(f"Ключ не найден: {key}")

    def __delitem__(self, key: Any) -> None:
        hash_value = self._get_hash(key)
        index = hash_value % self._capacity

        original_index = index
        target_index = None

        while self._buckets[index] is not None:
            node = self._buckets[index]
            if node.hash == hash_value and node.key == key:
                target_index = index
                break
            index = (index + 1) % self._capacity
            if index == original_index:
                break

        if target_index is None:
            raise KeyError(f"Ключ не найден: {key}")

        old_buckets = self._buckets
        old_buckets[target_index] = None
        self._buckets = [None] * self._capacity
        self._size = 0

        for node in old_buckets:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def clear(self) -> None:
        self._size = 0
        self._buckets = [None] * self._capacity
