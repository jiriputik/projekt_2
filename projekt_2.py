"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie - hra Bulls/Cows

author: Jiri Putik
email: j.putik@gmail.com
discord: peen_cz
"""
from sys import platform
import os, time

def check_player():             # zadání jména uživatele a požadované obtížnosti
    name = input("Welcome to the BULLS and COWS game.\nInput your name: ")
    level = ''
    while not level in ["0", "1", "2"]:
        print(f"""Welcome, {name}. Choose your level: \n
              0 - Rookie - three digits numbers
              1 - Experinced - four digits numbers
              2 - Pro - five digits number""")
        level = input()
    return(name, level)

def generate_number(level: int):  # generované číslice musí být unikátní a nesmí začínat nulou
    from random import randint
    digit_list = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
    generated = str(randint(1, 9))
    digit_list.remove(generated)
    for _ in range(2 + level):
        generated += (digit_list.pop())
    return generated

def check_system():                # zjistit systém -> win/něco jiného
    return True if platform.startswith("win") else False

def clear_screen():                 # smaž konzoli
    os.system('cls') if check_system else os.system('clear')

def validate_player_guess(guess, secret):       # je tip od uživatele validní? vrací list [(True nebo False), "důvod proč je False"]
    validate = [False, ""]
    try:
        int(guess)
    except ValueError:
        validate[1] += ("{} is not a number. ".format(guess))
    if len(guess) != len(secret):
        validate[1] += ("Wrong number of digits. ")
    if guess[0] == "0":
        validate[1] += ("Number cannot start with a zero. ")
    if len(set(guess)) != len(guess):
        validate[1] += ("Every digit had to be unique. ")
    validate[0] = True if validate[1] == "" else False
    return (validate)

def evaluate_player_guess(guess, secret):     # vyhodnocení uživatelského tipu, vrací tuple (bulls, cows)
    ...
    return (2, 2)





def read_hall_of_fame():
    if not "results.res" in os.listdir():
        with open("results.res", mode="w", encoding="utf-8"):
            pass
    else:
        ...
    ...
    # načtení souboru s výsledky
    # udělat adresář results, pokud neexistuje

def save_hall_of_fame():
    ...
    # uložení výsledků, aktualizace HoF

# MAIN PART

# před zahájením hry

player = check_player()
secret_sequence = generate_number(int(player[1]))
print(secret_sequence)


# hraj
#clear_screen()
print("SO THE GAME BEGINS!")

start_time = time.perf_counter()
attempt_counter = 0

while True:
    attempt_counter += 1
    print (f"Round no. {attempt_counter}. Enter your number.")
    player_guess = input()
    attempt_valid = validate_player_guess(player_guess, secret_sequence)
    if attempt_valid[0]:
        round_eval = evaluate_player_guess(player_guess, secret_sequence)
    else:
        print(f"Your number was not correct. Problem: {attempt_valid[1]}You've lost one round.")
        continue
    print("BULLS: {}   COWS: {}".format(round_eval[0], round_eval[1]))
        
    break



# konec hry

end_time = time.perf_counter()
game_duration = round(end_time - start_time, 0)

print("Total game duration: {} seconds.".format(game_duration))

read_hall_of_fame()
