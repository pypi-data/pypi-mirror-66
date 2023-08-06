import os
from spongebox.reg import filter_list


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
    print(list_all_files("C:\\Users\\LuoJi\\Documents\\01Python"))
