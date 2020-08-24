import random

# Write your code here


def identify_user():
    """"Returns user name input"""
    name = input("Enter your name: ")
    print(f"Hello, {name}")
    return name


def get_starting_score(name):
    """"
    Searches rating.txt for the user's score.
    Returns score as int.
    """
    ratings_file = open("rating.txt", "r")
    lines = ratings_file.readlines()
    ratings_file.close()
    for line in lines:
        record_name = line.split()[0]
        if record_name == name:
            return int(line.split()[1].strip())
    return 0


def get_move_list(moves):
    """
    Reads a comma-separated string of possible moves.
    Returns list of moves (list of str).
    If input string is empty, use rock/paper/scissors.
    """
    if moves == "":
        return ["rock", "paper", "scissors"]
    else:
        return moves.split(",")


def get_hierarchy(move_list):
    """
    Reads a move list (list of str).
    Returns a dictionary where keys are moves and corresponding values are the
    moves that will win against the given key.
    """
    hierarchy = {}
    for i in range(len(move_list)):
        move = move_list[i]
        winning_moves = []
        moves_left_to_find = (len(move_list) - 1) // 2
        if i < len(move_list) - 1:  # skip this if i is at the end
            for j in range(i + 1, len(move_list)):
                winning_moves.append(move_list[j])
                moves_left_to_find -= 1
                if moves_left_to_find == 0:
                    break
        if moves_left_to_find > 0:
            for j in range(0, i):
                winning_moves.append(move_list[j])
                moves_left_to_find -= 1
                if moves_left_to_find == 0:
                    break
        # finally, define the dictionary entry
        hierarchy[move] = winning_moves

    return hierarchy


def determine_winner(option1, option2, hierarchy):
    """
    Given two options (e.g. rock vs. paper), determines the winner.
    Reads the two options and a hierarchy (see get_hierarchy).
    Returns (str) option1 if option1 wins, option2 if option2 wins,
    and "draw" if neither win.
    """
    if option1 == option2:
        return "draw"
    elif option2 in hierarchy[option1]:
        return option2
    else:
        return option1


if __name__ == "__main__":
    # get name and score
    user_name = identify_user()
    score = get_starting_score(user_name)

    # get the move set and determine the hierarchy
    move_set_input = input()
    MOVE_LIST = get_move_list(move_set_input)
    COMMAND_LIST = ["!rating"]
    VALID_INPUTS = MOVE_LIST + COMMAND_LIST
    HIERARCHY = get_hierarchy(MOVE_LIST)

    # get initial moves
    print("Okay, let's start")
    user_move = input()
    computer_move = MOVE_LIST[random.randint(0, len(MOVE_LIST)-1)]

    # start game loop
    while user_move != "!exit":
        # deal with command inputs
        if user_move not in VALID_INPUTS:
            print("Invalid input")
            user_move = input()
            computer_move = MOVE_LIST[random.randint(0, len(MOVE_LIST)-1)]
            continue
        elif user_move == "!rating":
            print(f"Your rating: {score}")
            user_move = input()
            computer_move = MOVE_LIST[random.randint(0, len(MOVE_LIST) - 1)]
            continue

        # deal with move inputs
        winner = determine_winner(user_move, computer_move, HIERARCHY)
        if winner == computer_move:  # computer wins
            print("Sorry, but the computer chose " + computer_move)
        elif winner == "draw":
            print(f"There is a draw ({user_move})")
            score += 50
        elif winner == user_move:  # user wins
            print(f"Well done. The computer chose {computer_move} and failed")
            score += 100

        user_move = input()
        computer_move = MOVE_LIST[random.randint(0, len(MOVE_LIST)-1)]

    print("Bye!")
