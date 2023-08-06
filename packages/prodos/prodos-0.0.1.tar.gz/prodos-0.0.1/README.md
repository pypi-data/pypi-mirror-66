# prodos
`os` and `glob` extensions with advanced path joining.


## Install

```bash
pip install prodos
```

## Usage

```python
from prodos import prodglob, pathprod, prodmake

print('pathprod: creating a product of path items.')
for f in pathprod('base', ('a', 'b'), 'something', ('c', 'd')):
    print(f)
print()

print('prodglob: globbing over the product of path items.')
for f in prodglob('base', ('a', 'b'), 'something', ('c', 'd')):
    print(f)
fs = pathprod('base', ('a', 'b'), 'something', ('c', 'd'))
print('how many files exist?', sum(os.path.exists(f) for f in fs))
print()

print('prodmake: making directories from the product of path items.')
fs = prodmake('base', ('a', 'b'), 'something', ('c', 'd'))
print('how many files exist?', sum(os.path.exists(f) for f in fs))
print()

print('prodglob: globbing over the product of path items.')
for f in prodglob('base', ('a', 'b'), 'something', ('c', 'd')):
    print(f)
```

Outputs:
```
pathprod: creating a product of path items.
base/a/something/c
base/a/something/d
base/b/something/c
base/b/something/d

prodglob: globbing over the product of path items.
how many files exist? 0

prodmake: making directories from the product of path items.
how many files exist? 4

prodglob: globbing over the product of path items.
base/a/something/c
base/a/something/d
base/b/something/c
base/b/something/d
```
