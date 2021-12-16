# Name: Codenames.py
# Authors: Ryan C Hood and Shanjida Khatun
#
# Description: This python script contains the Codenames class, which allows someone to create
# an initial instance of a Codenames board and designations, and update it as the game is
# played.  The class includes printing methods along with a method to update the class variables
# during a Codenames game.

from Board import Board
import helper_methods as helper


class Codenames:

    def __init__(self, red_model, blue_model, guesser_model, red_model_type, blue_model_type, guesser_model_type, red_model_score_threshold=0.18, blue_model_score_threshold=0.18):
        """ This method initializes a Codenames game.  The models are set and the board is initialized as well. """
        self.red_model = red_model
        self.blue_model = blue_model
        self.guesser_model = guesser_model

        self.red_model_type = red_model_type
        self.blue_model_type = blue_model_type
        self.guesser_model_type = guesser_model_type

        self.red_model_score_threshold = red_model_score_threshold
        self.blue_model_score_threshold = blue_model_score_threshold

        self.board_specs = Board()

    # ======================================================================================
    # Helper methods for playing games.
    # ======================================================================================

    # -------------------------- Methods to get the code word ------------------------------

    def get_result_set(self, used_code_words):
        """ This method finds a result set given the current turn and the current designations, and then cleans
         up the result set which it then returns.  A result set is a list of tuples.  Each tuple is made of a word
         and a number.  The word being a potential code word, and the number being a "score" that represents the
         quality of the match."""
        # STEP 1: Get initial result set for the player whose turn it is.  We can get the player whose turn it is
        # by looking in the current state of board_specs.  We get our models estimate of the 50 best words to guess
        # looking at both teams' words.  So the below method does take the other team's words into account (and tries
        # to NOT match them!).  Also, get the bad_set of words that originate from the assassin.

        if self.board_specs.current_turn == 'red':
            result_set = self.red_model.most_similar(positive=self.board_specs.designations_currently['red'],
                                                     negative=self.board_specs.designations_currently['blue'],
                                                     restrict_vocab=50000,
                                                     topn=100)
            bad_set = self.red_model.most_similar(positive=self.board_specs.designations_currently['assassin'],
                                                     restrict_vocab=50000,
                                                     topn=100)
        else:
            result_set = self.blue_model.most_similar(positive=self.board_specs.designations_currently['blue'],
                                                      negative=self.board_specs.designations_currently['red'],
                                                      restrict_vocab=50000,
                                                      topn=100)
            bad_set = self.blue_model.most_similar(positive=self.board_specs.designations_currently['assassin'],
                                                  restrict_vocab=50000,
                                                  topn=100)

        # We need to remove the used_code_words from both the result set and the bad set.
        result_set = helper.remove_used_code_words(result_set, used_code_words)
        bad_set = helper.remove_used_code_words(bad_set, used_code_words)

        all_board_words = self.board_specs.get_board_words()

        # STEP 2: Perform a series of transformations to improve the result set.
        result_set = helper.full_pipeline(all_board_words, result_set, bad_set)

        return result_set

    def get_scores(self, result_set):
        """ This method calculates our own "score" to help in deciding the best code word.  This score is better than
        the previous score because it maximizes the number of broad matches, rather than maximizing the level of match
        to a specific word. """
        tuple_list = []
        if self.board_specs.current_turn == 'red':
            words_to_match = self.board_specs.designations_currently['red']
        else:
            words_to_match = self.board_specs.designations_currently['blue']

        for tuple in result_set:
            potential_code_word = tuple[0]
            score = 0

            for word_to_match in words_to_match:
                # Some words which were previously recommended by our model are not valid words in the
                # similarity method.  Only strange words or non word abbreviations (like asx) are not valid.
                # In those cases, give them a similarity score of 0, which will put them at the end of the
                # recommendations, which is OK.

                # Similarity scores are from -1 to 1.
                try:
                    if self.board_specs.current_turn == 'red':
                        similarity = self.red_model.similarity(potential_code_word, word_to_match)
                    else:
                        similarity = self.blue_model.similarity(potential_code_word, word_to_match)
                except:
                    similarity = 0

                if self.board_specs.current_turn == 'red':
                    if similarity > self.red_model_score_threshold:
                        score = score + 1
                if self.board_specs.current_turn == 'blue':
                    if similarity > self.blue_model_score_threshold:
                        score = score + 1

            tuple_list.append((potential_code_word, score))

        return tuple_list

    def find_best_valid_word(self, sorted_tuples):
        """ This method finds the best tuple to use for the code word.  This is not necessarily the first element since
        the best word must be a key in the guesser model. """

        for tuple in sorted_tuples:
            potential_code_word = tuple[0]
            try:
                similarity = self.guesser_model.similarity('sample', potential_code_word)
                # If we reach here, then the previous line of code must not have thrown an error, so we can end.
                return tuple
            except:
                continue

        # If we reach here, none of the potential words are valid.
        print("ERROR in find_best_valid_word().  None of the potential words are keys in the guesser model.")
        return ('ERROR', -1)


    def get_code_word(self, used_code_words):
        """ This method takes a model, its position (red or blue) and the current state of the board_specs, and it
         comes up with a codeword to present to the guesser.  A word and a number are returned."""
        result_set = self.get_result_set(used_code_words)
        score_tuples = self.get_scores(result_set)
        score_tuples.sort(key=lambda x: x[1], reverse=True)

        best_tuple = self.find_best_valid_word(score_tuples)

        code_word = best_tuple[0]
        number = best_tuple[1]

        return code_word, number

    # ----------------------- Methods to pick words from the middle ---------------------------

    def pick_words(self, code_word, intended_matches):
        """ This method takes a codeword, and the current state of the board_specs and determines which words in the
        middle to guess.  The guessed words are returned as a list."""

        board_words = self.board_specs.get_board_words()

        if self.guesser_model_type == 'guesser':
            # ==================================================================================
            # TO DO: FILL IN WITH NEW WAY TO GET LIST OF GUESSES THAT IS NOT A WORD 2 VEC MODEL
            # ==================================================================================
            print("Need to fill this in.")
        elif self.guesser_model_type == 'word2vec':

            # We just find the top matches in the board to the code word and we select the top (intended_matches) of them.
            score_tuples = []
            for board_word in board_words:
                similarity = self.guesser_model.similarity(code_word, board_word)
                tuple = (board_word, similarity)
                score_tuples.append(tuple)

            # Now we need to sort the score_tuples list by the score.
            score_tuples.sort(key=lambda x: x[1], reverse=True)

            subset = score_tuples[0:intended_matches]

            final_list = []
            for tuple in subset:
                final_list.append(tuple[0])
        else:
            print("A valid guesser model type was not provided.")

        return final_list

    # -----------------------------------------------------------------------------------------

    def update_board_specs(self, guessed_words):
        """ Given a list of words that were guessed, this method updates the current board_specs. """
        for guessed_word in guessed_words:
            self.board_specs.remove_word_from_designation(guessed_word)
        return

    # ======================================================================================
    # Methods to actually play the games.
    # ======================================================================================

    def play_full_game(self):
        """ This method plays a full game between the red model and the blue model using the guesser model."""

        # We need to initialize the team going first.  The team going first is in the board_specs.
        if self.board_specs.first_player == 'red':
            current_turn = 'red'
        else:
            current_turn = 'blue'

        # We need a list of all code words used in this game.  We require the models to use different code words
        # each turn.  If we don't, the model will tend to use the same code words repeatedly.
        used_code_words = []

        # The red team and blue team alternate until there is a winner, so we need a while loop.
        turns = 0
        while not self.board_specs.is_game_over():

            print("RED WORDS LEFT: ", self.board_specs.red_words_currently)
            print("BLUE WORDS LEFT: ", self.board_specs.blue_words_currently)

            # For the team currently going, get a code word.
            code_word, intended_matches = self.get_code_word(used_code_words)

            # Add code word to used_word_words to prevent the same code word from being used in the future.
            used_code_words.append(code_word)

            print("CURRENT TURN: ", current_turn)
            print("CODE WORD: ", code_word)
            print("INTENDED MATCHES: ", intended_matches)

            # Have the guesser interpret the code word.
            guessed_words = self.pick_words(code_word, intended_matches)

            print("GUESSED WORDS: ", guessed_words)

            # Adjust the board_specs accordingly.
            self.update_board_specs(guessed_words)

            # Check if the assassin was guessed.
            assassin_was_guessed = self.board_specs.assassin_was_guessed()

            if assassin_was_guessed:
                if current_turn == 'red':
                    winner = 'blue'
                else:
                    winner = 'red'
                return winner

            # Assassin was not guessed, so prepare the next turn.
            turns = turns + 1
            if current_turn == 'red':
                current_turn = 'blue'
            else:
                current_turn = 'red'

            continue

        # We reach here once a win condition has been reached.
        # Now we find the winning team.
        winner = self.board_specs.determine_winner()

        return winner



