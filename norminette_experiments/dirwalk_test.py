#!/usr/bin/env python3
import os, re, sys, time
from itertools import combinations
from pprint import pprint


class Listaroni:
    files = None

    def setup(self):
        self.files = []

    def populate_files(self, dirpath):
        self.populate_recursive([dirpath])

    def populate_recursive(self, objects):
        for obj in objects:
            if not os.path.isabs(obj):
                obj = os.path.abspath(obj)
            if os.path.isdir(obj):
                self.populate_recursive(self.list_dir(obj))
            else:
                self.populate_file(obj)

    def list_dir(self, dirpath):
        final = []
        for entry in os.listdir(dirpath):
            if entry[0] is not ".":
                final.append(os.path.join(dirpath, entry))
        return final

    def is_a_valid_file(self, f):
        return (
            f is not None
            and os.path.isfile(f)
            and re.match(".*\\.[ch]$", f) is not None
        )

    def populate_file(self, f):
        if not self.is_a_valid_file(f):
            return
        self.files.append(f)


def scan_files(path):
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and (entry.name.endswith('.c') or entry.name.endswith('.h')):
            yield entry.path


def scan_subdirs(lst, paths):
    for path in paths:
        if os.path.isdir(path) and "/." not in path:
            scan_subdirs(lst, scan_files(path))
        elif path is not None and os.path.isfile(path):
            lst.append(path)


def lst_append(lst, *args):
    for elem in args:
        lst.append(elem)
# lst_append(l1, *files)
# lst_append(l1, *list(os.path.join(root, f) for f in files))


def run_test(path):
    start = time.time()
    # l1 = [os.path.join(root,f) for root,_,files in os.walk(path) for f in files if f[0] != "."]
    l1 = []
    for root, dirs, files in os.walk(path):
        for ff in files:
            if ff[0] != ".":
                l1.append(os.path.join(root, ff))
        for ii, dd in enumerate(dirs):
            if dd[0] == "." and dd is not path:
                del dirs[ii]
    elapsed = time.time() - start
    print(f"   os.walk({path}): {elapsed}")

    start = time.time()
    lst = Listaroni()
    lst.setup()
    lst.populate_files(path)
    l2 = lst.files
    elapsed = time.time() - start
    print(f"  list_dir({path}): {elapsed}")

    start = time.time()
    l3 = []
    scan_subdirs(l4, [path])
    elapsed = time.time() - start
    print(f"os.scandir({path}): {elapsed}")

    print("len1:", len(l1), "len2:", len(l2), "len3:", len(l3))
    ll = [(sorted(l1), "l1"), (sorted(l2), "l2"), (sorted(l3), "l3")]
    for aa, bb in combinations(ll, 2):
        print(f"{aa[1]} == {bb[1]}:", aa[0] == bb[0])
        tmp = set() #setdiff_sorted(aa[0], bb[0])
        for pth in aa[0]:
            if pth not in bb[0]:
                tmp.add(pth)
        print(len(tmp))#, tmp)
    # pprint([l1, l2, l3])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        run_test(os.getcwd())
    else:
        for path in sys.argv[1:]:
            run_test(path)
