import romaji


def find_kana(char_to_find=None, raw_input=raw_input):
    """write katakana if uppercase, else hiragana"""
    if not char_to_find:
        char_to_find = romaji.choice()
    char_guessed = raw_input("translation for %s:\n" % char_to_find)
    char_guessed = unicode(char_guessed, "utf-8")
    if romaji.roma(char_guessed) == char_to_find:
        answer = "Good job !"
    else:
        answer = "Wrong"
    return answer


if __name__ == "__main__":
    while 1:
        print find_kana()
