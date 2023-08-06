"""
Implement load .txt files
"""


def read_text_file(filename):
    """
    Read .txt file

        Args:
            :param: filename(str): the name of .txt file
        Returns:
            :param: text(str): text in .txt file
    """
    with open(filename, "r", encoding="utf-16") as file:
        text = file.readlines()
    return str(text)


if __name__ == "__main__":
    filename = "8CM00002.txt"
    path = "./data/" + filename
    text = read_text_file(path)
    print(text)
