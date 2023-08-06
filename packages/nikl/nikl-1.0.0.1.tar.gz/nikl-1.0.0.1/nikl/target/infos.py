"""
Implement pre-processing and save files: <teiHeader></teiHeader> part
"""
from bs4 import BeautifulSoup
import os


def save_info(name, infos):
    """ ===============
        Save .text info
        ===============
        Args:
            :param: name(str): filename(test.txt)
            :param: infos(list): <teiHeader></heiHeader> contents
    """
    dir = os.getcwd() + "\\data"

    file = open(dir + "\\" + name + "_info.txt", 'w', encoding="utf-8")
    for info in infos:
        file.write(info+"\n")
    file.close()


def make_fileDesc(text):
    """ ============================
        Parsing fileDesc information
        ============================
        Args:
            :param: text(str): raw_file
    """
    soup = BeautifulSoup(text, "html.parser")
    element = {
        "titleStmt": ["title",
                      "author",
                      "sponsor",
                      "respStmt"],
        "extent": None,
        "publicationStmt": ["distributor",
                            "idno",
                            "availability"],
        "sourceDesc": None
    }

    # setting list options: element's values
    result = list()
    for key, value in element.items():
        if value is not None:
            for tag in value:
                result.append(tag)
        else:
            result.append(key)

    # find result's values
    idx = 0
    for _ in result:
        if _ is not "respStmt":
            tag = soup.select(_)[0].text
            _ += ": " + tag
        else:
            resp = soup.select("resp")[0].text
            tname = soup.select("tname")[0].text
            _ = "    " + _ + "\n        resp: " + resp + "\n        tname: " + tname
        result[idx] = _
        idx += 1

    # insert section: [fileDesc]
    result.insert(0, "[fileDesc]")
    return result


def make_encodingDesc(text):
    """ ================================
        Parsing encodingDesc information
        ================================
        Args:
            :param: text(str): raw_file
    """
    soup = BeautifulSoup(text, "html.parser")
    result = [
        "projectDesc",
        "samplingDecl",
        "editorialDecl"
    ]

    # find result's values
    idx = 0
    for _ in result:
        tag = soup.select(_)[0].text
        _ += ": " + tag
        result[idx] = _
        idx += 1

    # insert section: [encodingDesc]
    result.insert(0, "\n\n[encodingDesc]")

    return result


def make_profileDesc(text):
    """ ============================
        Parsing profileDesc information
        ============================
        Args:
            :param: text(str): raw_file
    """
    soup = BeautifulSoup(text, "html.parser")
    element = {
        "creation": ["date"],
        "langUsage": ["language"],
        "particDesc": ["person"],
        "settingDesc": None,
        "textClass": ["catRef"]
    }

    # setting list options: element's values
    result = list()
    for key, value in element.items():
        if value is not None:
            for tag in value:
                result.append(tag)
        else:
            result.append(key)

    # find result's values
    idx = 0
    for _ in result:
        tag = soup.select(_)[0]
        if _ is "date":
            _ = "creation:\n    " + _ + ": " + tag.text
        elif _ is "language":
            _ = "language:\n    " + _ + ": " + tag.text
        elif _ is "person":
            personId = tag['id']
            personSex = tag['sex']
            personAge = tag['age']
            _ += ": " + "\n    id: " + personId + "\n    sex: " + personSex + "\n    " + "age: " + personAge
        elif _ is "settingDesc":
            _ += ": " + tag.text
        elif _ is "catRef":
            _ += ": " + tag.text
        result[idx] = _
        idx += 1

    # insert section: [profileDesc]
    result.insert(0, "\n\n[profileDesc]")

    return result


def make_revisionDesc(text, i):
    """ ============================
        Parsing profileDesc information
        ============================
        Args:
            :param: text(str): raw_file
    """
    soup = BeautifulSoup(text, "html.parser")
    element = {
        "date": None,
        "respStmt": ["resp", "tname"],
        "item": None
    }

    # setting list options: element's values
    result = list()
    for key, value in element.items():
        if value is not None:
            for tag in value:
                result.append(tag)
        else:
            result.append(key)

    # find result's values
    idx = 0
    for _ in result:
        tag = soup.select(_)[0]
        if _ is "date":
            _ = "change:\n    " + _ + ": " + tag.text
        elif _ is "resp":
            _ = "respStmt \n    " + _ + ": " + soup.select("resp")[0].text
        elif _ is "tname":
            _ = "    " + _ + ": " + soup.select("tname")[0].text
        elif _ is "item":
            _ += ": " + tag.text
        result[idx] = _
        idx += 1

    # insert section: [revisionDesc]
    result.insert(0, "\n\n[revisionDesc " + str(i) + ']')

    return result


def get_info(filename, text):
    """ =======================
        Parsing the information
        =======================
        Args:
            :param: filename(str): filename
            :param: text(str): raw_file
    """
    # get specific values & write
    soup = BeautifulSoup(text, 'html.parser')
    revisionText = soup.select('change')

    fileDesc = make_fileDesc(text)
    encodingDesc = make_encodingDesc(text)
    profileDesc = make_profileDesc(text)
    revList = list()

    for i in range(1, len(revisionText)):
        tmp = make_revisionDesc(str(revisionText[i]), i)
        revList += tmp
    result = fileDesc + encodingDesc + profileDesc + revList


    # save data as .txt file
    save_info(filename, result)
