"""
Implement pre-process using regex
"""

import re


def prep_special_char(text):
    """ =============
        Delete specific character: !@#$%^&*()[]{}'",.~
        =============
        Args:
            :param: text(list): contents
        Returns:

    """
    pattern = "[^\w\s]"
    repl = ""
    for i in range(len(text)):
        regexed_text = re.sub(pattern, repl, text[i])
        text[i] = regexed_text

    return text


if __name__ == "__main__":
    text = ["@@안]녕!!하'##세&요*", "만@!$%나서#^&*반가(워.."]
    print(prep_special_char(text))
