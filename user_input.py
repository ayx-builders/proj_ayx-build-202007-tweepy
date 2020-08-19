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

    return join_to_query_string(split_user_input)


def parse_users(user_input, prefix):
    if user_input == '':
        return []

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
        split_user_input[line] = prefix + split_user_input[line]
        line -= 1
    return split_user_input


def parse_mentions(user_input):
    return join_to_query_string(parse_users(user_input, ''))


def parse_from(user_input):
    return join_to_query_string(parse_users(user_input, 'from:'))


def parse_to(user_input):
    return join_to_query_string(parse_users(user_input, 'to:'))


def parse_from_to(user_input):
    from_users = parse_users(user_input, 'from:')
    to_users = parse_users(user_input, 'to:')
    return join_to_query_string(from_users + to_users)


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

    return join_to_query_string(split_user_input)


def split_newlines(text):
    newline = re.compile('\r?\n')
    return newline.split(text)


def join_to_query_string(items):
    if len(items) == 0:
        return ''
    query = " OR ".join(items)
    return "(" + query + ")"
