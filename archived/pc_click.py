import time

from pykeyboard import PyKeyboard


def wait_for_input(input_str):
    k = PyKeyboard()
    period_interval = int(input("Plz input ur intervals time"))
    battle_interval = int(input("Plz input ur intervals time"))
    print(f"Ur wait_time is {period_interval}\nUr battle_time is {battle_interval}")
    for _ in range(3):
        print(f"_\n")
        time.sleep(1)
    while 1:
        time.sleep(1)
        k.tap_key(input_str.pop(0))
        if not input_str:
            break
