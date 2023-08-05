"""
Implement load .txt files
"""


def read_text_file(name):
    """
    Read .txt file

        Args:
            :param: name(str): the name of .txt file
        Returns:
            :param: text(str): text in .txt file
    """
    path = "./data/" + name + '.txt'
    with open(path, "r", encoding="utf-16") as file:
        text = file.readlines()
    return str(text)
