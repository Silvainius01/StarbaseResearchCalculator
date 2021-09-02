# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import CraftingResearch
from ItemObjects import *

# Unknown or unavailable materials default to -1 credits
test_material_costs = {
    "aegisium": 12300,
    "ajatite": 550,
    "arkanium": 20000,
    "bastium": 2500,
    "charodium": 4000,
    "corazium": 90000,
    "daltium": -1,
    "exorium": 4400,
    "haderite": -1,
    "ice": 800,
    "ilmatrium": -1,
    "karnite": 10000,
    "kutonium": 46000,
    "lukium": 44500,
    "merkerium": -1,
    "naflite": -1,
    "nhurgite": 4000,
    "oninum": -1,
    "surtrite": 4500,
    "targium": -1,
    "tengium": -1,
    "ukonium": -1,
    "valkite": 600,
    "vokarium": 2400,
    "xhallium": -1,
    "ymrium": 53000
}

test_data = {
    "Assault Rifle": {
        "screenshot": "screenshot_0.png",
        "valkite": 312,
        "bastium": 1565,
        "charodium": 3128,
        "vokarium": 1251,
        "red": 1,
        "blue": 21,
        "time": -1,
        "sell": -1,
        "buy": -1
    },
    "Pistol": {
        "screenshot": "screenshot_0.png",
        "ajatite": 73,
        "bastium": 233,
        "charodium": 507,
        "vokarium": 110,
        "blue": 2
    },
    "Assault Rifle Magazine": {
        "screenshot": "screenshot_0.png",
        "bastium": 7.56,
        "ice": 18.96,
        "nhurgite": 0.84,
        "blue": 1,
        "time": -1,
        "sell": -1,
        "buy": -1
    },
    "Tripod Autocannon": {
        "screenshot": "screenshot_0.png",
        "bastium": 463.3,
        "charodium": 2162.9,
        "vokarium": 463.4,
        "red": 31,
        "blue": 294,
        "time": -1,
        "sell": -1,
        "buy": -1
    },
    "Tripod Autocannon Magazine": {
        "screenshot": "screenshot_0.png",
        "bastium": 515.74,
        "ice,": 75.2,
        "nhurgite": 678.4,
        "red": 1,
        "blue": 75,
        "time": -1,
        "sell": -1,
        "buy": -1
    },
    "Tripod": {
        "screenshot": "screenshot_0.png",
        "ajatite": 517,
        "bastium": 827.3,
        "charodium": 723.8,
        "red": 17,
        "blue": 168,
        "time": -1,
        "sell": 900
    }
}

def print_hi(name):
    print("hi")
    pass


def test():
    init_material_pairs()
    analyzer = CraftingResearch.CraftingResearchAnalyzer()

    analyzer.import_raw_data(test_data)
    analyzer.export_data("./test2.json")
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
