#!/usr/bin/python3
# -*- coding: utf8 -*-

#from lxml import etree

from xml.etree import ElementTree as etree

import os, sys
import optparse
import re
#import codecs

#сборка кучки xml с описанием стилей знаков в единую библиотеку qgis

tree = etree.fromstring("""
<!DOCTYPE qgis_style>
<qgis_style version="2" >
<symbols />
<colorramps />
<textformats />
<labelsettings />
<legendpatchshapes />
<symbols3d />
</qgis_style>
""")

symbols = tree.find('symbols')
colors = tree.find('colorramps')

parser = optparse.OptionParser("usage: %prog [options] dirs")
parser.add_option("-o", "--output", dest="outfile",
   default="symbology-ng-style.new.xml", type="string", help=u"выходной файл")
parser.add_option("-r", "--rename", dest="rename", action="store_true",
   default=False, help=u"переименовываем символ исходя из имени файла")

(options, args) = parser.parse_args()

print(options, args)

#def os.wal(arg, dirname, files):
for in_dir in args:
    for (root_dir, _, files) in os.walk(in_dir):
        for fn in files:
            filename = os.path.join(root_dir, fn)
            fname = os.path.basename(filename), sys.getfilesystemencoding()
            print(filename, fname)
            if not os.path.isfile(filename): continue
            if not filename.endswith('.xml'): continue
            tr = etree.fromstring("<xml>%s</xml>" % (open(filename, 'rt').read()))
        
            for child in tr.getchildren():
                if child.tag == 'symbol': 
                    if options.rename:
                        new_name = fname[:fname.rfind('.')]
                        if child.attrib['name'].startswith('@'):
                            child.attrib['name'] = re.sub('^@(.*)@', '@%s@' % (new_name, ), child.attrib['name'])
                        else:
                            child.attrib['name'] = new_name
                    symbols.append(child)
    
#os.path.walk(indir, walkdir, '12')

open(options.outfile, 'wb').write(etree.tostring(tree, encoding='utf8'))
