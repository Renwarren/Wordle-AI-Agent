def load_dict(filename):
    file = open(filename)
    words = file.readlines()
    file.close()
    return words

#Return 5 letters of the words in UPPERCASE
def slice_word(words):
    return [word[:5].upper() for word in words]
