from sys import argv as args
from bs4 import BeautifulSoup as bs
from os.path import exists as path_exists
import json


def get_child_by_index(container, index):
    iter = container.children
    for i in range(index+1):
        child = iter.next()

    return child

def get_username(container):

    div = get_child_by_index(container, 1)
    for i in range(7):
        div = get_child_by_index(div, 0)

    return div.text


def get_following(path):
    """
    Returns a list of user handles from html file.
    The HTML has to be copied from instagrams following tab and should contain the bottom most div containing all users.
    """

    following = list()

    with open(path) as sourcef:
        soup = bs(sourcef, "html.parser")
        flist = soup.find("div")
        spans = flist.find_all("span", {"class": "_aap6 _aap7 _aap8"})

        for span in spans:
            following.append(span.text.strip())

    return following

def main():
    path = args[1]
    network = args[2]
    user = args[3]

    following = get_following(path)
    if path_exists(network):
        with open(network, "r") as fp:
            network_dict = json.load(fp)
    else:
        network_dict = dict()

    network_dict[user] = {"display": "", "follows": following}

    with open(network, "w") as fp:
        json.dump(network_dict, fp, indent=2)



if __name__ == '__main__':
    main()
