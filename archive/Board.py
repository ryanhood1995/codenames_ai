# Name: Board.py
# Authors: Ryan C Hood and Shanjida Khatun
#
# Description: This python script contains the Board class, which allows someone to create
# an initial instance of a Codenames board and designations, and update it as the game is
# played.  The class includes printing methods along with a method to update the class variables
# during a Codenames game.

import random
import copy


class Board:

    def __init__(self, file_name="words.txt", board_size=5, num_first_player_words=9, num_second_player_words=8, num_assassins=1):
        """ This method is called when an instance of Board is created. """
        # First initialize our basic class variables from provided parameters. If a class variable is
        # appended with 'initially', then that class variable corresponds to the initial state of the
        # board which does not change over time.  If the class variable is appended with 'currently',
        # then that class variable corresponds to the current state of the board, which will change
        # as words are guessed.
        self.board_size = board_size
        self.num_first_player_words_initially = num_first_player_words
        self.num_second_player_words_initially = num_second_player_words
        self.num_assassins_initially = num_assassins
        self.num_civilians_initially = board_size*board_size - num_first_player_words - num_second_player_words - num_assassins

        self.num_first_player_words_currently = num_first_player_words
        self.num_second_player_words_currently = num_second_player_words
        self.num_assassins_currently = num_assassins
        self.num_civilians_currently = self.num_civilians_initially

        # Now we do the more complicated process to actually initialize the board we will play with.

        # -------------------------------------------------------------------------------------------
        # STEP 1: Get the word list from the file provided.
        # -------------------------------------------------------------------------------------------
        word_list = open(file_name).readlines()
        # Remove whitespace from the ends of each element in list.
        word_list = [elem.strip().lower() for elem in word_list]

        # -------------------------------------------------------------------------------------------
        # STEP 2: Create the board in the middle.
        # -------------------------------------------------------------------------------------------

        if board_size not in range(0, 26):
            print("Invalid board size entered.")
        board = []
        for row_index in range(0, board_size):
            row = []
            for column_index in range(0, board_size):
                elem_index = random.randint(0, len(word_list) - 1)
                elem = word_list.pop(elem_index)
                row.append(elem)
            board.append(row)

        # Now the board in the middle is fully created.

        # -------------------------------------------------------------------------------------------
        # STEP 3: Create the Designations.
        # -------------------------------------------------------------------------------------------
        available_words = [word for sublist in board for word in sublist]

        # First, sample the first player's words.
        first_player_words = random.sample(available_words, num_first_player_words)
        available_words = [word for word in available_words if word not in first_player_words]

        # Second, sample the second player's words.
        second_player_words = random.sample(available_words, num_second_player_words)
        available_words = [word for word in available_words if word not in second_player_words]

        # Third, sample the assassin(s).
        assassin_words = random.sample(available_words, num_assassins)
        available_words = [word for word in available_words if word not in assassin_words]

        # The rest of the words are all civilians.
        civilian_words = available_words

        # Now that we have the four different lists, we can select a first player: red or blue.
        if random.randint(0, 1) == 0:
            first_player = "red"
            red_words = first_player_words
            blue_words = second_player_words
        else:
            first_player = "blue"
            blue_words = first_player_words
            red_words = second_player_words

        # Lastly, we construct the dict.
        designations = {"red": red_words, "blue": blue_words, "assassin": assassin_words, "civilian": civilian_words}

        # -------------------------------------------------------------------------------------------
        # STEP 4: Finish initializing class variables.
        # -------------------------------------------------------------------------------------------

        self.board = board
        self.designations_initially = designations
        self.first_player = first_player
        self.red_words_initially = red_words
        self.blue_words_initially = blue_words
        self.assassin_words_initially = assassin_words
        self.civilian_words_initially = civilian_words

        self.designations_currently = copy.deepcopy(self.designations_initially)
        self.red_words_currently = copy.deepcopy(self.red_words_initially)
        self.blue_words_currently = copy.deepcopy(self.blue_words_initially)
        self.assassin_words_currently = copy.deepcopy(self.assassin_words_initially)
        self.civilian_words_currently = copy.deepcopy(self.civilian_words_initially)
        self.current_turn = copy.deepcopy(self.first_player)

        # The full description of a board is complete, so we are done.
        return

    # --------------------------------------------------------------------------------------
    # Printing methods
    # --------------------------------------------------------------------------------------
    def print_board(self):
        print("BOARD: ")
        for row in self.board:
            print(row)
        return

    def print_designations(self, initial_0_current_1):
        print("DESIGNATIONS: ")
        if initial_0_current_1 == 0:
            print(self.designations_initially)
        if initial_0_current_1 == 1:
            print(self.designations_currently)
        return

    def print_red_words(self, initial_0_current_1):
        print("RED WORDS: ")
        if initial_0_current_1 == 0:
            print(self.red_words_initially)
        if initial_0_current_1 == 1:
            print(self.red_words_currently)
        return

    def print_blue_words(self, initial_0_current_1):
        print("BLUE WORDS: ")
        if initial_0_current_1 == 0:
            print(self.blue_words_initially)
        if initial_0_current_1 == 1:
            print(self.blue_words_currently)
        return

    def print_assassin_words(self, initial_0_current_1):
        print("ASSASSIN WORDS: ")
        if initial_0_current_1 == 0:
            print(self.assassin_words_initially)
        if initial_0_current_1 == 1:
            print(self.assassin_words_currently)
        return

    def print_civilian_words(self, initial_0_current_1):
        print("CIVILIAN WORDS: ")
        if initial_0_current_1 == 0:
            print(self.civilian_words_initially)
        if initial_0_current_1 == 1:
            print(self.civilian_words_currently)
        return

    def print_first_player(self):
        print("FIRST PLAYER: ")
        print(self.first_player)
        return

    def print_all(self, initial_0_current_1):
        self.print_board()
        self.print_designations(initial_0_current_1)
        self.print_first_player()
        return

    # --------------------------------------------------------------------------------------
    # Methods to update class variables.
    # --------------------------------------------------------------------------------------

    def remove_word_from_designation(self, word):
        """ We search the designations dict for the word to be removed.  We remove the word
        from the dict and also the appropriate list.  This allows a game to be played with an
        instance of a board, and things will update as the game is played."""
        # Below, key will be either red, blue, assassin, or civilian depending on the identity
        # of the word being removed.
        dict_as_nested_list = list(self.designations_currently.values())

        new_dict_as_nested_list = []
        index_removed = -1
        for lst_index in range(0, len(dict_as_nested_list)):
            lst = dict_as_nested_list[lst_index]
            if word in lst:
                index_removed = lst_index
                lst.remove(word)
            new_dict_as_nested_list.append(lst)

        # Now the new_dict_as_nested_list has been made.
        new_dict = {'red': new_dict_as_nested_list[0], 'blue': new_dict_as_nested_list[1], 'assassin': new_dict_as_nested_list[2], 'civilian': new_dict_as_nested_list[3]}

        # Reassign the designations dict.
        self.designations_currently = new_dict

        # Now adjust the individual list that we changed.
        if index_removed == 0:
            self.red_words_currently.remove(word)
        if index_removed == 1:
            self.blue_words_currently.remove(word)
        if index_removed == 2:
            self.assassin_words_currently.remove(word)
        if index_removed == 3:
            self.civilian_words_currently.remove(word)

        return

    def change_turns(self):
        """ This method changes whose turn it currently is. """
        if self.current_turn == 'red':
            self.current_turn = 'blue'
        if self.current_turn == 'blue':
            self.current_turn = 'red'
        return

    def is_game_over(self):
        """ This method determines if the game is over by looking at the current list for both the red and blue team.
         If one of the list is empty, then the game must be over."""
        is_game_over = False
        if not self.blue_words_currently or not self.red_words_currently:
            is_game_over = True
        return is_game_over

    def determine_winner(self):
        """ This method is called after the game has been concluded, and it returns the winner of the game. """
        if not self.red_words_currently:
            return 'red'
        else:
            return 'blue'

    def get_board_words(self):
        """ This method returns the words in the board in the middle as a single list. """
        final_list = []
        for row in self.board:
            for word in row:
                final_list.append(word)
        return final_list

    def assassin_was_guessed(self):
        """ Checks to see if the assassin part of designations is empty.  If so, the assassin was guessed. """
        assassin_list = self.designations_currently['assassin']
        if not assassin_list:
            # Then the list is empty.
            return True
        return False


if __name__ == "__main__":

    # Testing the above class.
    board_specs = Board()
    board_specs.print_designations(1)
    board_specs.print_blue_words(1)

    word = board_specs.designations_currently['blue'][0]
    board_specs.remove_word_from_designation(word)

    board_specs.print_designations(1)
    board_specs.print_blue_words(1)

