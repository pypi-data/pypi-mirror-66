import os, json, tqdm, difflib, copy
from pprint import pprint
import pandas as pd

def read_api_rst(file_path):
    """
    file_path is a string which is a path to API rst file. 
    """
    with open(file_path, "r", encoding = "utf-8") as fp:
        contents = json.load(fp)
    return contents

def dump_json_to_file(dic, file_path, indent = 4, sort_keys = True):
    with open(file_path, "w", encoding = "utf-8") as fp:
        json.dump(dic, fp, indent=indent, sort_keys=sort_keys)
    return

def function_04():
    return "弱水长东情自转，儿郎热泪也沾裳。"

def function_05():
    return "战胜困难最好的办法就是面对困难, 加油奥里给!"