#!/usr/bin/python
# -*- coding: utf8 -*-

#разборка единого файла библиотеки стиля qgis на кучку xmlек
#python depack.py [файл библиотеки] [директория куда сложить]
#python depack.py symbology-ng-style.xml tmp

from xml.etree import ElementTree as etree

import os, sys
#import codecs

pars = sys.argv
pars.extend(['symbology-ng-style.xml', 'tmp/'])

infile = pars[1]
outdir = pars[2]

tree = etree.parse(infile)

symbols = dict( (s.attrib['name'], s) for s in tree.find('symbols').findall('symbol') )
symbols_names = sorted(symbols.keys())

for (name, symb) in symbols.items():
    if name.startswith('@'): continue
    filename = '%s/symbols/%s/%s.xml' % (outdir, symb.attrib['type'], symb.attrib['name'].replace(u'ж/д',u'ж_д'))
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname): os.makedirs(dirname)
    txt = etree.tostring(symb, encoding='utf8')
    for sym_lay_name in [ n for n in symbols_names if n.startswith('@' + name + '@') ]:
        txt += etree.tostring(symbols[sym_lay_name], encoding='utf8')
    txt = txt.replace("<?xml version='1.0' encoding='utf8'?>\n", '')
    open(filename, 'wt').write(txt)

for symb in tree.find('colorramps').findall('colorramp'):
    filename = '%s/colorramp/%s/%s.xml' % (outdir, symb.attrib['type'], symb.attrib['name'])
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname): os.makedirs(dirname)
    txt = etree.tostring(symb, encoding='utf8')
    txt = txt.replace("<?xml version='1.0' encoding='utf8'?>\n", '')
    open(filename, 'wt').write(txt)
