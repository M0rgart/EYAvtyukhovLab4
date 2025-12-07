from typing import Optional, Union, List, MutableSequence, Iterator
import main


class Player:
    def __init__(self, name: str, start_balance: int = 100):
        self.name = name
        self.balance = start_balance

    def bet(self, amount: int) -> bool:
        if amount < self.balance:
            self.balance -= amount
            return True
        return False

    def win(self, amount: int) -> None:
        self.balance += amount

    def __repr__(self) -> str:
        return f'Player(name={self.name}, balance={self.balance})'


class PlayerCollection(MutableSequence):
    def __init__(self, players: Optional[List[Player]] = None):
        self._players = players if players is not None else []

    def __len__(self) -> int:
        return len(self._players)

    def __getitem__(self, index: Union[int, slice]) -> Union[Player, 'PlayerCollection']:
        if isinstance(index, slice):
            return PlayerCollection(self._players[index])
        return self._players[index]

    def __setitem__(self, index: int, player: Player) -> None:
        self._players[index] = player

    def __delitem__(self, index: int) -> None:
        del self._players[index]

    def insert(self, index: int, player: Player) -> None:
        self._players.insert(index, player)

    def __iter__(self) -> Iterator[Player]:
        return iter(self._players)

    def __repr__(self) -> str:
        return f'PlayerCollection({self._players})'

    def find_by_name(self, name: str) -> Optional[Player]:
        for player in self._players:
            if player.name == name:
                return player
        return None


if __name__ == "__main__":
    main.main()