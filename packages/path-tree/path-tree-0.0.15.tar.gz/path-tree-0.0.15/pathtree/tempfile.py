'''

The issue is that you won't have a tmp path until you insttantiate/create the file/directory.

Also, a lot of the path methods aren't applicable to tmp files.

A File:

with pathtree.tmp.some_random_name.open('w') as f:
    f.write('asdfasdf')
    f.seek(3)
    f.write('234')

pathtree.tmp.some_random_name.read()
pathtree.tmp.some_random_name.rm()

A Directory:
adir = pathtree.tmp.some_random_dir


with adir.fileA.open('w') as f:
    f.write('asdfasdfasdfasd')

with adir.fileB.open('w') as f:
    f.write(adir.fileA.read()[::-1])

adir.rmglob()
assert not adir.exists()
assert not adir.fileB.exists()

'''

from .path import Path, Paths

class TmpPath(Path):
    def __init__(self, name):
        self.name = name

class TmpPaths(Paths):
    def __init__(self, root, data=None):
        self.root = root
        super().__init__(self, {}, data=data)

    def __getattr__(self, k):
        if k not in self:
            self.paths[k] = self._create_file(k)
        return self.paths[k]

    def _create_file(self, name):
        return name
