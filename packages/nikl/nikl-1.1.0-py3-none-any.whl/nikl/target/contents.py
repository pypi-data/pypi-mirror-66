"""
Implement pre-processing and save files: <text></text> part
"""
from bs4 import BeautifulSoup
import os

from nikl.preprocessor.specificChar import prep_special_char
from nikl.loader.loadfile import read_text_file


def save_info(filename, contents, newline):
    """ ===============
        Save .text info
        ===============
        Args:
            :param: filename(str): filename(test.txt)
            :param: infos(list): <text></text> contents
    """
    filename = (os.getcwd() + filename).replace(".txt", "")

    file = open(filename + "_content.txt", 'w', encoding="utf-8")
    enterVal = "\n" if newline is True else ""
    for content in contents:
        file.write(content + enterVal)
    file.close()


def get_content(filename, text, newline):
    """ ================
        Parsing contents
        ================
        Args:
            :param: filename(str): filename
            :param: text(str): raw_file
            :param: newline(boolean): check input '\n' or not
    """
    # get specific values & write
    soup = BeautifulSoup(text, "html.parser")
    raw_text = soup.select("s")
    rawList = [text.getText() for text in raw_text]

    # pre-processing
    result = prep_special_char(rawList)
    return save_info(filename, result, newline)


if __name__ == "__main__":
    filename = "./data/" + "8CM00002.txt"
    raw_text = read_text_file(filename)
    get_content(filename, raw_text, True)