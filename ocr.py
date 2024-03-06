import easyocr


def perform_ocr(ocr_reader, img_path):
    """  """
    result = ocr_reader.readtext(img_path)
    return result


def filter_words(ocr_results, valid_words_file_path):
    """  """
    with open(valid_words_file_path) as valid_words_file:
        valid_words_list = valid_words_file.read().splitlines() 
        print(valid_words_list)


    final_words = []
    for found_word_record in ocr_results:
        bbox = found_word_record[0]
        word = found_word_record[1]
        prob = found_word_record[2]

        if word in valid_words_list:
            final_words.append(word)
        
        continue

    return final_words




if __name__ == "__main__":
    reader = easyocr.Reader(['en']) 
    result = perform_ocr(reader, '../codenames_ai/imgs/codenames_board_2.jpg')
    

    final_words = filter_words(result, "../codenames_ai/words.txt")
    print(final_words)