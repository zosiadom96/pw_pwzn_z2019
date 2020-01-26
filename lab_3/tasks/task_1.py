def parse_input(_input):
    """
    Splits multiline string into list of lists with integers.
    Napisz funkcję przymującą wielolinijkowy ciąg znaków.
    a zwracającą listę list liczb całkowitych znajdujących się w podanym ciągu znaków.
    Nie używaj pętl for i while.
    String może zawierać puste linie na początku i końcu.
    :param input: string to parse
    :type input: str
    :return: list of parsed list of integers
    :rtype: list
    """

# hint: module string i str

    lines = _input.strip().splitlines()
    lists = list(map(lambda line: line.split(' '), lines))

    def str_to_int(str_list):
        return list(map(int, str_list))
    number_lists = list(map(str_to_int, lists))
    output = number_lists
    return output


if __name__ == '__main__':
    _input = """
1 5
1 6 7
3 2
1 10
1 10
1 6
2 5
3 2
    
    
    """
    assert parse_input(_input) == [
        [1, 5], [1, 6, 7], [3, 2], [1, 10], [1, 10], [1, 6], [2, 5], [3, 2]
    ]
