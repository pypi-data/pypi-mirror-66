"""
Implement pre-process using regex
"""

import re


def preprocess(text):
    pattern = "[^\w\s]"
    repl = ""
    for i in range(len(text)):
        regexed_text = re.sub(pattern, repl, text[i])
        text[i] = regexed_text

    return text
