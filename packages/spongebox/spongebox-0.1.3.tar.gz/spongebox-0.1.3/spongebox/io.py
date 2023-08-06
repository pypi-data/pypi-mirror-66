import os
import pandas as pd
from spongebox.reg import filter_list

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option("display.unicode.east_asian_width", True)
pd.set_option("display.float_format", lambda x: "%.4f" % x)


def list_dir(dir_path, exp=None):
    if exp is None:
        return os.listdir(dir_path)
    else:
        return filter_list(os.listdir(dir_path), exp=exp)


def list_all_files(dir_path, lst=[]):
    children = os.listdir(dir_path)
    for f in children:
        _path_ = os.path.join(dir_path, f)
        if os.path.isdir(_path_):
            list_all_files(_path_)
        else:
            lst.append(_path_)
    return lst


if __name__ == "__main__":
    print(list_dir("../", exp=".*md$"))
    print(list_all_files("."))