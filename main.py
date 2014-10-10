import imp

try:
    imp.find_module('sklearn')
    found = True
except ImportError:
    found = False

print(found)