# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

from datetime import datetime
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import quiz


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('pp3-snakequiz')


# Welcome message
print("Welcome to Snakequiz!!!\n")
print("Test your snake knowledge with this 10 questions quiz.")
print("To start play, just enter your name and let's roll.")


def game_menu():
    """
    Give player 5 different options to choose from: play, quit,
    restart, score board or my last 4 scores
    """
    print("\n")
    print("Press 1 - 5 to choose from below options:")
    print("1. Play \n2. Quit \n3. Restart \n4. Score board")
    print("5. My last 4 scores")

    while True:
        game_choice = input("What would you like to do? \n").strip()
        print("\n")

        if game_choice == "1":
            print("Great!\n")
            break
        elif game_choice == "2":
            print("GG. See you next time!")
            quit()
        elif game_choice == "3":
            print("How nice you want to play again!\n")
            restart_game()
        elif game_choice == "4":
            # need add code to get data from Gsheet, and display option 1 and 2
            display_top_10_scores()
            game_menu()
        elif game_choice == "5":
            print("Here are your last 4 scores!")
            # need code to get data from Gsheet, about player's scores
        else:
            print("Invalid input, please choose between 1 - 5")


def get_player_name():
    """
    Get player to enter their chosen name. The request will only ends
    when a valid input is received.
    """
    while True:
        print("Next choose a user name!\n")
        print("Characters A-Z, a-z, and 0-9 are permitted.")
        print("Maximum of 8 characters.")
        print("Any white space will be removed.\n")

        player_name = input("Please enter your name: \n")

        if check_player_name(player_name):
            print("\n")
            print(f"Hi {player_name}, let's begin the quiz!!\n")
            # quiz.play_quiz()
            data = quiz.play_quiz()
            update_score_worksheet(data, player_name)
            # print(data)
            # print("this is from get player name function")
            game_menu()

    check_player_name(player_name)
    return player_name.strip()


def check_player_name(player_name):
    """
    Validate user's input if the username provided is valid.
    It will raise ValueError if the lengh is more than 8 character,
    or no name was entered, or anything other than letters and
    numbers were used.
    """
    try:
        if not player_name:
            raise ValueError("Please enter a player name!")
        if len(player_name) > 8:
            raise ValueError("Player name too long")
        if not player_name.isalnum():
            raise ValueError("Only letters and digits are permitted")
    except ValueError as e:
        print(f"Invalid data: {e}! Please try again.\n")
        return False

    return True


def update_score_worksheet(data, player_name,):
    """
    update score of each player by add new data
    """
    print("Updating the score...\n")
    score_worksheet = SHEET.worksheet("score_list")
    # print(data)
    # print("this is from update function")
    # datetime object containing current date and time

    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    score_worksheet.append_row([data, player_name, dt_string])
    print("Score updated successfully.\n")


def restart_game():
    """
    allow player to play the game multiple times
    """
    # quiz.play_quiz()
    data = quiz.play_quiz()
    score_worksheet = SHEET.worksheet("score_list")
    score_worksheet.append_row([data])
    game_menu()


def display_top_10_scores():
    """
    display top 10 highest score to the player, data
    fethed from google sheet
    """
    # score_worksheet = SHEET.worksheet("score_list")
    # sheet = client.open('commentary data')
    # client = gspread.authorize(CREDS)
    # score_sheet = SHEET.get_worksheet(0)
    records_score_data = SHEET.worksheet("score_list").get_all_values()
    # print(records_score_data)
    # sorted_data = sorted(records_score_data, reverse=True)

    print("Top 10 Scores!")
    print("Pos\tName\t Score\t Date")

    records_df = pd.DataFrame.from_dict(records_score_data)
    print(records_df.nlargest(10, ["score"])
    # for line in range(10):
    #     print(str(line+1) + "\t" + str(sorted_data[line]))


def main():
    """
    Run all the functions for the game
    """
    game_menu()
    get_player_name()


main()
