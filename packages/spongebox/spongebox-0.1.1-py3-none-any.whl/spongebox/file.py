import os
import re

def list_dir(dir, exp=None):
    if exp is None:
        return os.listdir(dir)
    match = [re.search(exp, f) for f in os.listdir(dir)]
    return [f.group() for f in match if f is not None]


if __name__ == "__main__":
    print(list_dir(".", exp=".*md$"))
