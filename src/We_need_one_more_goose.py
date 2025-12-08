import Wanna_play_kazik, Players
import random


class Goose:
    def __init__(self, name: str, honk_volume: int):
        self.name = name
        self.honk_volume = honk_volume
        self._stolen_chips = 0

    def honk(self) -> str:
        return f"{self.name} кричит с громкостью {self.honk_volume}!"

    def __repr__(self) -> str:
        return f"Goose(name={self.name}, honk_volume={self.honk_volume})"

    def __add__(self, other: "Goose") -> "GooseFlock":
        return GooseFlock([self, other])

class WarGoose(Goose):
    def __init__(self, name: str, honk_volume: int, power: int = 10):
        super().__init__(name, honk_volume)
        self.power = power

    def attack(self, player: 'Players.Player') -> str:
        dmg = random.randint(1, self.power)
        player.balance = max(0, player.balance - dmg)
        return f'{self.name} атакует {player.name}! Баланс игрока уменьшен на {dmg}'

    def __repr__(self) -> str:
        return f'WarGoose(name={self.name}, power={self.power})'

class HonkGoose(Goose):
    def __init__(self, name: str, honk_volume: int, honk_power: int = 10):
        super().__init__(name, honk_volume)
        self.honk_power = honk_power

    def super_honk(self, casino: 'Wanna_play_kazik.Casino') -> str:
        res = f'{self.name} издает особый крик!'
        win = 0

        for player in casino.players:
            if random.random() > 0.5:
                player.balance += self.honk_power
                casino.balance[player.name] = player.balance
                win += 1

        return res + f' {win} игроков получили по {self.honk_power} монет.'

    def __call__(self) -> str:
        return f'Гусь {self.name} отвечает ГОГОГО с силой {self.honk_volume}!'


class GooseFlock:
    def __init__(self, geese: list[Goose]):
        self.geese = geese

    def __repr__(self) -> str:
        goose_names = ', '.join(goose.name for goose in self.geese)
        return f"GooseFlock({goose_names})"

if __name__ == "__main__":
    pass