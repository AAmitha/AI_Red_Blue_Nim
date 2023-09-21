#modules imported
import sys
import math

#function to check balls avialble in the piles , checking the player is human or computer and excecuting based on that
def play_modified_red_blue_game(balls_left, player, depth):
    
    balls_left = balls_left
    player_turn = player
    while balls_left["red"] > 0 and balls_left["blue"] > 0: 
        print(f"Balls left in the piles: {balls_left}")
        if player_turn == 'human':  
            pile = user_move(balls_left)
            balls_left[pile] -= 1
            print(f"The human removed one marble from the {pile} pile.")
            if(balls_left["red"] <= 0 or balls_left["blue"] <= 0):
                break
            else:
                player_turn = 'computer'
        if player_turn == 'computer': 
            pile, amount = computer_move_using_depth(balls_left, depth)
            balls_left[pile] -= amount
            print(f"The computer removed {amount} marble from the {pile} pile.")
            if(balls_left["red"] <= 0 or balls_left["blue"] <=0):
                break
            else:
                player_turn = 'human'

    print("Modified red_blue nim game over")
    if balls_left["red"] == 0 or balls_left["blue"] == 0:
        print(f"The {player_turn} wins!")
        score = 2 * balls_left["red"] + 3* balls_left["blue"]
    print(f"Score: {score}")

# taking user input to pick the ball from piles
def user_move(balls_left):
    pile = input("From which pile do you want to take red or blue marbles ")
    while pile not in ["red", "blue"] or balls_left[pile] == 0:
        pile = input("Invalid move choose only red or blue. From which pile do you want to take red or blue marbles ")
    return pile

# Minimax algorithm implementation With alpha beta pruning with depth limited search algorithm
def minmax(balls_left, depth, alpha, beta, max_player):
    if depth == 0 or balls_left["red"] == 0 or balls_left["blue"] == 0:
        return calculate_score(balls_left)
    if max_player:
        value = float("-inf") # turn is a maximizing player storing the value as negative infinity
        for possible_move in generate_possible_moves(balls_left):
            new_balls_left = balls_left.copy() # Copying the balls left into a new dummy variable to perform algorithm, so it doesn't effect the existing variable
            new_balls_left[possible_move[0]] -= possible_move[1]
            value = max(value, minmax(new_balls_left, 100 if depth==None else depth - 1, alpha, beta, False)) #Taking default depth as 100 if user doesn't given any input
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = float("inf") #now the  turn is a miniimizing player storing the value as positive infinity
        for possible_moves in generate_possible_moves(balls_left):
            new_balls_left = balls_left.copy()
            new_balls_left[possible_moves[0]] -= possible_moves[1]
            value = min(value, minmax(new_balls_left, 100 if depth==None else depth - 1, alpha, beta, True)) # As per the algorithm the first is max player so assuming it as TRUE
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

# This function is about the best move based on the minmax algorithm with alpha beta pruining based on depth limit search
def computer_move_using_depth(balls_left, depth):
    best_move = None
    best_score = float("-inf")
    for possible_move in generate_possible_moves(balls_left):
        new_balls_left = balls_left.copy()
        new_balls_left[possible_move[0]] -= possible_move[1]
        score = minmax(new_balls_left, depth, float("-inf"), float("inf"), False)
        if score > best_score:
            best_move = possible_move
            best_score = score
    return best_move[0], best_move[1]

# Calculating the score based on the balls left in the piles
def calculate_score(balls_left):
    return 2 * balls_left["red"] + 3 * balls_left["blue"]

# This function returns the number of moves made based on the balls left in the pile
def generate_possible_moves(balls_left):
    possible_moves = []
    if balls_left["red"] > 0:
        possible_moves.append(("red", 1))
    if balls_left["blue"] > 0:
        possible_moves.append(("blue", 1))
    return possible_moves


if __name__ == "__main__":
    """ we need to give 5 arguments while running the code and 1 argument is optional for first-player
        1) Python execution file(red_blue_nim.py)
        2) Number of Red Balls
        3) Number of Blue Balls
        4) player(Human or computer)- By default Computer, if the first player was not given by the user
        5) Depth required to search
    """

    if len(sys.argv) < 3:
        print("we need to give 4 arguments: red_blue_nim.py(python file with .py extension) <num-red> <num-blue> <first-player(optional)> <depth>")
        sys.exit()

    #storing input arguments to the below variables
    number_of_red_balls = int(sys.argv[1])
    number_of_blue_balls = int(sys.argv[2])
    #storing number of balls entered by user into variables
    balls_left = {"red": number_of_red_balls, "blue": number_of_blue_balls} 
    argument_3 = sys.argv[3].lower()
    if argument_3 == "human" or argument_3 == "computer":
        player = argument_3
        depth= None if len(sys.argv) < 5 else int(sys.argv[4])
    else:
        player = 'computer'
        depth= int(sys.argv[3])

    print(f" red balls:{number_of_red_balls} and blue balls:{number_of_blue_balls} and player:{player} and depth:{depth}")
    play_modified_red_blue_game(balls_left, player, depth)