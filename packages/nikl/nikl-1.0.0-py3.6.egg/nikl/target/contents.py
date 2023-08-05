"""
Implement pre-processing and save files: <text></text> part
"""
from bs4 import BeautifulSoup
import os
from nikl.preprocessor.preprocess import preprocess


def save_info(name, contents, newline):
    """ ===============
        Save .text info
        ===============
        Args:
            :param: name(str): filename(test.txt)
            :param: infos(list): <text></text> contents
    """
    name = name.replace(".txt", "")
    dir = os.getcwd() + "\\data"

    file = open(dir + "\\" + name + "_content.txt", 'w', encoding="utf-8")
    enterVal = "\n" if newline is True else ""
    for info in contents:
        file.write(info + enterVal)
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
    result = preprocess(rawList)
    return save_info(filename, result, newline)
