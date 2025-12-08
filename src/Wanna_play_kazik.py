import main, random
from typing import MutableMapping, List, Dict, Iterator
from src.Players import PlayerCollection, Player
from src.We_need_one_more_goose import Goose, WarGoose, HonkGoose


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
        self.players = PlayerCollection()
        self.geese = PlayerCollection()
        self.balance = CasinoBalance()
        self.goose_income = CasinoBalance()
        self.chips: List[Chip] = []

    def register_player(self, player: Player) -> None:
        self.players.append(player)
        self.balance[player.name] = player.balance

    def register_geese(self, goose: Goose) -> None:
        self.geese.append(goose)
        self.goose_income[goose.name] = 0

    def players_bet(self) -> str:
        rich_players = self.players.get_players_with_balance()
        if not rich_players:
            return 'Никто не может сделать ставку'
        player = random.choice(rich_players)
        bet = random.randint(1, min(100, player.balance))

        if player.bet(bet):
            self.balance[player.name] = player.balance
            if random.random() > 0.67:
                win = bet * 2
                player.win(win)
                self.balance[player.name] = player.balance
                return f'{player.name} ставит {bet} и выигрывает {win}!'
            return f'{player.name} ставит {bet} и проигрывает.'
        return f"{player.name} не может поставить {bet} (баланс = {player.balance})"

    def geese_attack(self) -> str:
        if not self.geese or not self.players:
            return 'Нет гусей или игроков. Атака не удалась.'
        war_geese = [goose for goose in self.geese if isinstance(goose, WarGoose)]
        if not war_geese:
            return 'Нет военных гусей. Атака не удалась.'

        goose = random.choice(war_geese)
        player = random.choice(self.players)
        old_balance = player.balance
        res = goose.attack(player)
        self.balance[player.name] = player.balance

        return res + f'(было: {old_balance}, стало: {player.balance})'

    def goose_honk(self) -> str:
        if not self.geese or not self.players:
            return 'Нет гусей или игроков. Атака не удалась.'
        goose = random.choice(self.geese)
        if isinstance(goose, HonkGoose):
            return goose.super_honk(self)
        return goose.honk()

    def goose_steal(self) -> str:
        if not self.geese or not self.players:
            return 'Нет гусей или игроков. Атака не удалась.'

        goose = random.choice(self.geese)
        rich_players = self.players.get_players_with_balance()

        if not rich_players:
            return f"{goose.name} пытался украсть, но все игроки бомжуют."

        player = random.choice(rich_players)
        steal = random.randint(1, min(10, player.balance))
        player.balance -= steal
        self.balance[player.name] = player.balance

        current_income = goose.income.get(goose.name, 0)
        self.goose_income[goose.name] = current_income + steal

        return f"{goose.name} украл {steal} у {player.name} (баланс {player.balance})."

    def player_panic(self) -> str:
        if not self.players:
            return 'Нет игроков для паники.'

        rich_players = self.players.get_players_with_balance()
        if not rich_players:
            return 'Все игроки приняли антидеприсанты после проигрыша всех своих денег. Паники не будет :('
        player = random.choice(rich_players)
        lost = player.balance
        player.balance -= lost
        self.balance[player.name] = 0

        return f'{player.name} паникует и теряет все {lost}!'

    def create_chip(self) -> str:
        value = random.randint(1, 100)
        chip = Chip(value)
        self.chips.append(chip)

        if len(self.chips) > 2:
            combination = random.choice(self.chips) + random.choice(self.chips)
            return f'Создана фишка {chip}, объединена с одной из предыдущих: {combination}'
        return f'Создана фишка {chip}'

    def goose_gang(self) -> str:
        if len(self.geese) < 2:
            return 'Гусей слишком мало, они не могут объедениться в стаю'
        goose1, goose2 = random.sample(list(self.geese), 2)
        flock = goose1 + goose2
        return f'{goose1.name} и {goose2.name} объединились в стаю: {flock}!'

    def step(self) -> str:
        events = [
            self.players_bet(),
            self.geese_attack(),
            self.goose_honk(),
            self.goose_steal(),
            self.player_panic(),
            self.create_chip(),
            self.goose_gang()
        ]
        weight = [0.2, 0.15, 0.15, 0.15, 0.1, 0.15, 0.1]
        return random.choices(events, weights=weight, k=1)[0]()

if __name__ == "__main__":
    main.main()