import main
from typing import MutableMapping, List, Dict, Iterator


class Chip:
    def __init__(self, value: int):
        self.value = value

    def __add__(self, other: 'Chip') -> 'Chip':
        return Chip(self.value + other.value)

    def __repr__(self):
        return f'Chip(value={self.value})'


class CasinoBalance(MutableMapping):
    def __init__(self):
        self._balances: Dict[str, int] = {}
        self._change_log: List[str] = []

    def __getitem__(self, key: str) -> int:
        return self._balances[key]

    def __setitem__(self, key: str, value: int) -> None:
        old_value = self._balances.get(key, 0)
        self._balances[key] = value
        change = value - old_value
        log = f'Балланс {key}: {old_value} -> {value} (Изменение: {'+' if change >+ 0 else ''}{change})'
        self._change_log.append(log)
        print(f"[LOG] {log}")

    def __delitem__(self, key: str) -> None:
        del self._balances[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._balances)

    def __len__(self) -> int:
        return len(self._balances)

    def __contains__(self, key: str) -> bool:
        return key in self._balances

    def get_log(self) -> List[str]:
        return self._change_log

    def __repr__(self) -> str:
        return f'Casino_balance({self._balances})'


class Casino:
    def __init__(self):
        pass

if __name__ == "__main__":
    main.main()