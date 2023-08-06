import re

path = '../topoly/'

with open(path + '__init__.py', 'r') as f:
    for line in f.readlines():
        m = re.search('def (.*?)\(.*', line)
        if m:
            record = m.group(1)
            print('.. _doc_{}:'.format(record))
            print('.. autofunction:: topoly.{}'.format(record))

                                                                                
with open(path + 'params.py', 'r') as f:
    for line in f.readlines():
        m = re.search('class (.*?)[(:].*', line)
        if m:
            record = m.group(1)
            print('.. _doc_{}:'.format(record))
            print('.. autoclass:: topoly.params.{}'.format(record))
