def get_search_strings():
    alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                 'y', 'z']
    search_strings = []

    for index, value in enumerate(alphabets):
        for value2 in alphabets:
            search_strings.append(value + value2)
    return search_strings
