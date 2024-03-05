# Name: play_games.py
# Authors: Ryan C Hood and Shanjida Khatun
#
# Description: This python script is designed to play many Codenames games and do statistical analysis on the results.
#

from Codenames import Codenames
import gensim
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models.keyedvectors import KeyedVectors


def play_games(num_games, red_model, blue_model, guesser_model):
    """ This method takes a list of models, a plays a bulk number of games. """
    # Set up lists to hold final results.
    winners = []
    first_players = []

    for game_index in range(0, num_games):
        print("Starting to play game", game_index, " out of", num_games)

        # Instantiate a game of Codenames
        codenames = Codenames(red_model, blue_model, guesser_model, 'word2vec', 'glove', 'word2vec')

        # Get info related to the current game.
        first_player = codenames.board_specs.first_player

        winner = codenames.play_full_game()
        first_players.append(first_player)
        winners.append(winner)

    return winners, first_players


def find_basic_statistics(winners, first_players):
    """ This method takes a list of winners and first players and finds basic statistics about it. """

    num_games = len(winners)
    num_red_wins = 0
    num_blue_wins = 0
    num_first_player_wins = 0
    num_second_player_wins = 0

    for game_index in range(0, num_games):
        winner = winners[game_index]
        first_player = first_players[game_index]

        if winner == first_player:
            num_first_player_wins = num_first_player_wins + 1
        else:
            num_second_player_wins = num_second_player_wins + 1

        if winner == 'red':
            num_red_wins = num_red_wins + 1
        else:
            num_blue_wins = num_blue_wins + 1

    return num_red_wins, num_blue_wins, num_first_player_wins, num_second_player_wins


if __name__ == '__main__':
    NUM_GAMES = 3
    print("The number of games to be played is: ", NUM_GAMES)

    # RED MODEL
    print("Loading in red team's model...")
    RED_MODEL = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True, limit=500000)

    # BLUE MODEL
    print("Loading in blue team's model...")
    #glove2word2vec(glove_input_file="glove.6B.100d.txt", word2vec_output_file="glove_100d_as_word2vec.txt")
    BLUE_MODEL = KeyedVectors.load_word2vec_format("glove_100d_as_word2vec.txt", binary=False, limit=500000)

    # GUESSER MODEL
    print("Loading in guesser model...")
    # TO DO: Change this to effectively load in a guesser model that is not word2vec or glove.  Right now it is word2vec.
    GUESSER_MODEL = gensim.models.KeyedVectors.load_word2vec_format('wiki-news-300d-1M.vec', binary=False, limit=500000)

    print("Finished Loading in models.")


    print("Beginning to play games.")
    winners, first_players = play_games(NUM_GAMES, RED_MODEL, BLUE_MODEL, GUESSER_MODEL)
    print("Games finished!")
    num_red_wins, num_blue_wins, num_first_player_wins, num_second_player_wins = find_basic_statistics(winners, first_players)

    print("NUM RED WINS: ", num_red_wins)
    print("NUM BLUE WINS: ", num_blue_wins)
    print("NUM FIRST PLAYER WINS: ", num_first_player_wins)
    print("NUM SECOND PLAYER WINS: ", num_second_player_wins)


