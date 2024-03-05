# Name: helper_methods.py
# Authors: Ryan C Hood and Shanjida Khatun
#
# Description: This python script contains some helper methods that did not have a better home anywhere else!

import inflect


# ====================================================================================================================
# Pipeline methods
# ====================================================================================================================

def keep_single_words(result_set):
    """ This method remove words in the result set such as "high_five". It also removes "words" that have numbers in
    them, such as "V8" """
    new_list = []
    for index in range(0, len(result_set)):
        # If the word is composed of only alphabetical letters...
        if result_set[index][0].isalpha():
            # ...then it's a good word and needs to stay in the list.
            new_list.append(result_set[index])
    return new_list


def set_lowercase(result_set):
    """ Makes every word lowercase. """
    new_list = []
    for index in range(0, len(result_set)):
        old_word = result_set[index][0]
        new_word = old_word.lower()
        new_tuple = (new_word, result_set[index][1])
        new_list.append(new_tuple)
    return new_list

def remove_repeats(result_set):
    """ Remove repeated words in the result_set. """
    new_result_set = []
    # A word bank will hold all words that have been seen.
    word_bank = []
    for tup in result_set:
        if tup[0] not in word_bank:
            new_result_set.append(tup)
            word_bank.append(tup[0])
    return new_result_set


def remove_plural_copies(result_set):
    """ This method removes the "plural copies" from the result set, so we don't have essential copies of every
     word in the result set. """
    # We use the inflect library to get plural forms.
    p = inflect.engine()

    # trouble_indices will hold the indices that need to be removed.
    trouble_indices = []
    # The first step is to figure out which entries need to be removed from the result set.
    for first_index in range(0, len(result_set)):
        # If index is in trouble indices then move along.
        if first_index in trouble_indices:
            continue

        # If not... start by getting the word.
        word = result_set[first_index][0]

        # Get the plural opposite.  That is, if word is already plural, then the plural
        # opposite will be singular.
        plural_opposite = p.plural(word)

        # Figure out if and where the plural opposite shows up in result set.
        for second_index in range(0, len(result_set)):
            if plural_opposite == result_set[second_index][0]:
                # Then add it to trouble_indices.
                trouble_indices.append(second_index)

    # Now trouble_indices should contain the indices we need to remove from the result set.
    new_result_set = []
    for number in range(0, len(result_set)):
        if number not in trouble_indices:
            new_result_set.append(result_set[number])
    return new_result_set


def remove_board_words(all_board_words, result_set):
    """ This method removes the plural version of words on the board from the result set.  We are not allowed to use
     them as code words! """
    # As before, we use inflect to get plural forms.
    p = inflect.engine()

    # The first step is to pluralize all of the board words.
    plural_board_words = []
    for word in all_board_words:
        plural_word = p.plural(word)
        plural_board_words.append(plural_word)

    # Now, we need to go through and make sure that none are in our result set.
    trouble_indices = []
    for plural_word in plural_board_words:
        for index in range(0, len(result_set)):
            if plural_word == result_set[index][0]:
                trouble_indices.append(index)

    # Second, we go through the regular board words.
    for word in all_board_words:
        for index in range(0, len(result_set)):
            if (word == result_set[index][0]) and (index not in trouble_indices):
                trouble_indices.append(index)

    # Now we have the bad indices and we can remove them from the results set.
    new_result_set = []
    for num in range(0, len(result_set)):
        if num not in trouble_indices:
            new_result_set.append(result_set[num])
    return new_result_set


def remove_bad_words(result_set, bad_set):
    """ We need to remove words in the bad set from our result set.  We certainly don't want to make any of those words
     a code word! """
    # We create a fresh result_set.
    new_result_set = []

    # Outer loop is result set.
    for tup_good in result_set:
        # Assume there will not be a match initially.
        there_is_match = False
        # Inner loop is bad set.
        for tup_bad in bad_set:
            if tup_good[0] == tup_bad[0]:
                # If the words agree, then there is a match.
                there_is_match = True
        # After comparing a good word with all of the bad words...
        if not there_is_match:
            # If there is no match, the good word can stay in the result set.
            new_result_set.append(tup_good)
    return new_result_set


def full_pipeline(all_board_words, result_set, bad_set):
    """ Combines every pipeline step into one to refine our result set. """
    # First, we want to perform all of the transformations on our result set.
    result_set = keep_single_words(result_set)
    result_set = set_lowercase(result_set)
    result_set = remove_repeats(result_set)
    result_set = remove_plural_copies(result_set)
    result_set = remove_board_words(all_board_words, result_set)

    # Then, we want to perform most of the transformations on our bad set.  We do not perform the last two because we want our bad set to contain
    # as many variations as it can contain.
    bad_set = keep_single_words(bad_set)
    bad_set = set_lowercase(bad_set)
    bad_set = remove_repeats(bad_set)

    # Now our bad set is ready to be contrasted with our good set.
    result_set = remove_bad_words(result_set, bad_set)

    return result_set


# ====================================================================================================================
# Other methods
# ====================================================================================================================

def remove_used_code_words(tuple_set, used_code_words):
    """ Removes tuples in the tuple set where the word (the first element of the tuple) is in the used_code_words.
    We do not want those tuple to persist in the result sets! """
    final_tuple_set = []
    for tuple in tuple_set:
        word = tuple[0].lower()
        if word not in used_code_words:
            final_tuple_set.append(tuple)
    return final_tuple_set



