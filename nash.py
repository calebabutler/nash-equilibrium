#!/usr/bin/env python3

# Copyright (c) 2023 Susana Brewer Costano, Caleb Butler, Maria Calvo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import random
import tabulate
import sys
from matplotlib import pyplot as plt


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
    Run game with two strategies and 'iterations' number of iterations.
    'score1' is the score history of player 1 and 'score2' is the score
    history of player 2.
    '''
    # Initial score histories
    score1 = []
    score2 = []
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
        # Add scores to score histories
        score1.append(s1)
        score2.append(s2)
    # Return final score histories
    return (score1, score2)


def main():
    '''
    Runs all strategy pairs defined in 'headers' to 'iterations' number of
    iterations, puts scores in a table and prints the table to the screen
    '''
    iterations = 10000
    headers = ['',
               'always defect',
               'always collaborate',
               'tit-for-tat',
               'random',
               'tit-for-tat with forgiveness',
               'tit-for-tat with reputation',
               'randomness with reputation']

    # Variable for graphs
    fig, axs = plt.subplots(28)
    subplot = 0

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
            score1, score2 = run_whole_game(iterations, strategy1, strategy2)
            # Graph information
            axs[subplot].set_title(f'{strategy1} vs. {strategy2}')
            axs[subplot].set_xlabel('iteration')
            axs[subplot].set_ylabel('score')
            axs[subplot].plot(score1, label='Player 1')
            axs[subplot].plot(score2, label='Player 2')
            axs[subplot].legend()
            subplot += 1
            # Add to row
            row.append(f'({sum(score1):.2f}, {sum(score2):.2f})')
        # Append row to table
        table.append(row)
    # Print table
    print(tabulate.tabulate(table, headers, tablefmt='github'))
    # Save plot
    fig.set_size_inches(12.8, 201.6)
    plt.savefig('plots.png', dpi=100)
    plt.close(fig)


if __name__ == '__main__':
    main()
