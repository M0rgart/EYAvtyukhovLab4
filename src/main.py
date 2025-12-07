import simulation


def main() -> None:
    print('Симуляция №1')
    print('Вызов симуляции без указания переменных')
    simulation.run_sim()

    print('\nСимуляция №2')
    print('Вызов симуляции из 10 шагов')
    simulation.run_sim(steps=10)

    print('\nСимуляция №3')
    print('Вызов симуляции по сиду')
    simulation.run_sim(seed=67)

    print('\nСимуляция №4')
    print('Вызов симуляции по сиду с ограниченным количеством шагов')
    simulation.run_sim(steps=10, seed=67)

if __name__ == "__main__":
    main()
