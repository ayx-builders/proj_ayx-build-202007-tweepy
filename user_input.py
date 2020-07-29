import re


def parse_keywords(user_input):
    split_user_input = split_newlines(user_input)
    line = len(split_user_input)-1
    while line >= 0:
        input = split_user_input[line]
        if len(input) == 0:
            del split_user_input[line]
            line -= 1
            continue

        split_user_input[line] = "(" +input + ")"
        line -= 1

    query = " OR ".join(split_user_input)
    return "(" + query + ")"


def parse_mentions(user_input):
    split_user_input = split_newlines(user_input)
    line = len(split_user_input)-1
    while line >= 0:
        input = split_user_input[line]
        if len(input) == 0:
            del split_user_input[line]
            line -= 1
            continue
        if input[0] != '@':
            split_user_input[line] = "@" + input
        line -= 1

    query = " OR ".join(split_user_input)
    return "(" + query + ")"


def parse_hashtags(user_input):
    split_user_input = split_newlines(user_input)
    line = len(split_user_input)-1
    while line >= 0:
        input = split_user_input[line]
        if len(input) == 0:
            del split_user_input[line]
            line -= 1
            continue
        if input[0] != '#':
            split_user_input[line] = "#" + input
        line -= 1

    query = " OR ".join(split_user_input)
    return "(" + query + ")"


def split_newlines(text):
    newline = re.compile('\r?\n')
    return newline.split(text)
