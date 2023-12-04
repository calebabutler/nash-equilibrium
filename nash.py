#!/usr/bin/env python3
import random
import tabulate
import sys


def run_single_game(move1, move2, game_number):
    '''
    Return two scores for individual prisoner's dilemma game given two moves
    and the game number
    '''
    # Important variables according to Wikipedia table
    R = 6
    S = 2
    T = 9
    P = 3
    discount_rate = 0.999

    # Decay given discount rate and game number
    decay = discount_rate ** game_number

    # Give correct scores based on move combination
    if move1 == 0 and move2 == 0:
        return (R * decay, R * decay)
    if move1 == 0 and move2 == 1:
        return (S * decay, T * decay)
    if move1 == 1 and move2 == 0:
        return (T * decay, S * decay)
    if move1 == 1 and move2 == 1:
        return (P * decay, P * decay)


def get_next_move(strategy, previous_moves):
    '''
    Return next move given a strategy and previous moves of other player
    '''
    forgiveness_factor = 0.1     # What is the probability you "forgive"
    reputation_randomness = 0.7  # What is the reputation of last strategy
    match strategy:
        # 1 means defect
        case 'always defect':
            return 1
        # 0 means collaborate
        case 'always collaborate':
            return 0
        # Do what previous player does except for first move, where you
        # collaborate
        case 'tit-for-tat':
            if len(previous_moves) == 0:
                return 0
            return previous_moves[-1]
        # Do random move
        case 'random':
            return random.randint(0, 1)
        # Do what previous player does except for first move, where you
        # collaborate, or with a probability of forgiveness factor,
        # collaborate anyway
        case 'tit-for-tat with forgiveness':
            random_var = random.random()
            if random_var < forgiveness_factor or len(previous_moves) == 0:
                return 0
            return previous_moves[-1]
        # Do what previous player does except for first move, where you
        # collaborate. If player has poor reputation, always defect. If player
        # has good reputation, always collaborate.
        case 'tit-for-tat with reputation':
            if len(previous_moves) == 0:
                return 0
            reputation = sum(previous_moves) / len(previous_moves)
            if reputation < (1/3):
                return 0
            if reputation < (2/3):
                return previous_moves[-1]
            return 1
        # Do random move but weighted according to 'reputation_randomness'
        case 'randomness with reputation':
            random_var = random.random()
            if random_var < reputation_randomness:
                return 1
            return 0


def run_whole_game(iterations, strategy1, strategy2):
    '''
    Run game with two strategies and 'iterations' number of iterations
    '''
    # Initial scores
    score1 = 0
    score2 = 0
    # Initial list of previous moves
    previous_moves1 = []
    previous_moves2 = []
    # For each game
    for game_number in range(iterations):
        # Get next moves using strategy and previous move lists
        move1 = get_next_move(strategy1, previous_moves2)
        move2 = get_next_move(strategy2, previous_moves1)
        # Add to previous moves
        previous_moves1.append(move1)
        previous_moves2.append(move2)
        # Run single game and get single game scores
        s1, s2 = run_single_game(move1, move2, game_number)
        # Add scores to score total
        score1 += s1
        score2 += s2
    # Return ending scores
    return (score1, score2)


def main():
    '''
    Runs all strategy pairs defined in 'headers' to 'iterations' number of
    iterations, puts scores in a table and prints the table to the screen
    '''
    iterations = 100000
    headers = ['',
               'always defect',
               'always collaborate',
               'tit-for-tat',
               'random',
               'tit-for-tat with forgiveness',
               'tit-for-tat with reputation',
               'randomness with reputation']

    # Create table one row at a time
    table = []
    for i, strategy1 in enumerate(headers[1:]):
        # Each strategy gets a row
        row = [strategy1]
        # Skip first i lines (don't recompute pairs already computed elsewhere)
        for j in range(i):
            row.append('')
        # Each second strategy gets a column
        for strategy2 in headers[i + 1:]:
            print(f'Running game {strategy1} vs. {strategy2}...',
                  file=sys.stderr)
            row.append(str(run_whole_game(iterations, strategy1, strategy2)))
        # Append row to table
        table.append(row)
    # Print table
    print(file=sys.stderr)
    print(tabulate.tabulate(table, headers, tablefmt='grid'))


if __name__ == '__main__':
    main()
