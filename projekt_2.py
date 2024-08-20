"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie - hra Bulls/Cows

author: Jiri Putik
email: j.putik@gmail.com
discord: peen_cz
"""
from sys import platform
import os, time

def choose_level():             # vyber si obtížnost
    level = ''
    while not level in ["0", "1", "2"]:
        print(f"""Choose your level: \n
              0 - Rookie - three digits numbers, no attempts limit
              1 - Experienced - four digits numbers, max 20 attempts
              2 - Pro - five digits number, max 40 attempts""")
        level = input()
    return(level)

def check_player():             # zadání jména uživatele a požadované obtížnosti
    name = input("Welcome to the BULLS and COWS game.\nInput your name: ")
    return(name)

def generate_number(level: int):  # generované číslice musí být unikátní a nesmí začínat nulou
    from random import randint
    digit_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    generated = str(randint(1, 9))
    digit_list.remove(generated)
    for _ in range(2 + level):
        generated += digit_list.pop(randint(0, len(digit_list)-1))
    return generated

def check_system():                # zjistit systém -> win/něco jiného
    return True if platform.startswith("win") else False

def clear_screen():                 # smaž konzoli
    os.system('cls') if check_system else os.system('clear')

def validate_player_guess(guess, secret):       # je tip od uživatele validní? vrací list [vyhodnocení, "důvod"] - vyhodnocení je True/False, důvod je předaná chybová hláška
    validate = [False, ""]
    if guess != "":
        try:
            int(guess)
        except ValueError:
            validate[1] += ("{} is not a number! ".format(guess))
        if len(guess) != len(secret):
            validate[1] += ("Wrong number of digits! ")
        if guess[0] == "0":
            validate[1] += ("Number cannot start with a zero! ")
        if len(set(guess)) != len(guess):
            validate[1] += ("Every digit has to be unique! ")
        validate[0] = True if validate[1] == "" else False
    else:
        validate[1] += ("You didn't entered a number! ")
    return (validate)

def evaluate_player_guess(guess, secret):     # vyhodnocení uživatelského tipu, vrací tuple (bulls, cows)
    cows, bulls = 0, 0
    for index,letter in enumerate(guess):
        if letter in secret:
            if guess[index] == secret[index]:
                bulls += 1 
            else:
                cows += 1
    return (bulls, cows)

def check_play_again():
    play = ""
    while play not in ["Y", "Yes", "y", "N", "No", "n"]:
        play = input("Play again? (Yes/No) ")
    return False if play.casefold().startswith("n") else True


def read_results():
    if not "results.res" in os.listdir():
        with open("results.res", mode="w", encoding="utf-8"):
            return False
    else:
        with open("results.res", mode="r", encoding="utf-8") as results_file:
            results_list = results_file.read().splitlines()
            return results_list
    
    # načtení souboru s výsledky do proměnné results_list
    # udělá soubor results.res, pokud neexistuje

def save_player_result(result):           # ulož výsledky aktuální hry
    read_results()
    with open("results.res", mode="a", encoding="utf-8") as results_file:
        results_file.writelines(";".join(str(item) for item in list(result.values())))
        results_file.write("\n")
    
def view_hall_of_fame(level):
    splitted_list_level = []
    results_list = read_results()
    show_level = ["ROOKIE", "EXPERIENCED", "PRO"]
    print(f"HALL OF FAME - TOP 10 LEVEL {show_level[int(level)]}".center(60, "_"))
    print(f"Pos. {"Name":<20}{"Attempts":<10}{"Time (sec)":<5}\n")
    for result_item in results_list:
        if level == result_item.split(";")[1]:
            spl = result_item.split(";")
            for index,item in enumerate(spl):
                if index == 2:
                    spl[index] = int(spl[index])
                elif index == 3:
                    spl[index] = float(spl[index])
            splitted_list_level.append(spl)
    splitted_list_level.sort(key=lambda res:(res[2],res[3]))
    for place,item in enumerate(splitted_list_level):
        print(f"{place + 1:>2}.  {item[0]:<20}{item[2]:<10}{item[3]:<5}")
        if place > 8:
            print(f"END OF TOP 10 LEVEL {show_level[int(level)]}".center(60, "_"))
            break
    else:
        print(f"END OF TOP 10 LEVEL {show_level[int(level)]}".center(60, "_"))
# MAIN PART

# před zahájením hry

player = ["name",0]                     # player[0] - jméno, player[1] - level
player[0] = check_player()
play_again = True


while play_again:
    player[1] = choose_level()
    secret_sequence = generate_number(int(player[1]))
    
    # hraj

    clear_screen()                      
    print("SO THE GAME BEGINS!")
    print(secret_sequence)            # při debugování odkomentovat, aby bylo vidět hádané číslo

    start_time = time.perf_counter()
    attempt_counter = 0

    while True:
        attempt_counter += 1
        if (attempt_counter > int(player[1])*20) and int(player[1]):
            print("You reached maximum attempts. You lost!")
            player_result = {"name": player[0], "level": player[1], "attempts":attempt_counter, "time":999999}
            break
        player_guess = input(f"Round no. {attempt_counter}. Enter your number: ")
        attempt_valid = validate_player_guess(player_guess, secret_sequence)
        if attempt_valid[0]:
            round_eval = evaluate_player_guess(player_guess, secret_sequence)
        else:
            print(f"Your input was not correct. Problem: {attempt_valid[1]}You've lost one round.")
            continue
        bulls = "BULL" if round_eval[0] == 1 else "BULLS"
        cows =  "COW" if round_eval[1] == 1 else "COWS"
        print(f"{round_eval[0]} {bulls},   {round_eval[1]} {cows}")
        if round_eval[0] == len(secret_sequence):               # počet BULLS = délka hádaného čísla => výhra
            end_time = time.perf_counter()
            game_duration = round(end_time - start_time, 1)
            print(f"Great, {player[0]}! Yes, the secret number was {secret_sequence}!")
            print("Total attempts: {} Total game duration: {} seconds.".format(attempt_counter, game_duration))
            player_result = {"name": player[0], "level": player[1], "attempts":attempt_counter, "time":game_duration}
            break
    save_player_result(player_result) if player_result["time"] != 999999 else ...
    input("... PRESS ENTER TO CONTINUE ...")
    clear_screen()
    view_hall_of_fame(player[1])
    play_again = check_play_again()  

# konec hry