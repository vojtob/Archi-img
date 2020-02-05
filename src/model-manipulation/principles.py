# -*- coding: utf-8 -*-

import os
import sys

import xml.etree.ElementTree as ET

import archiModel as am

# read project dir from arguments
if (len(sys.argv) < 2):
    print('usage: principles.py projectPath')
    exit(1)
else:
    projectDir = os.path.normpath(sys.argv[1])

# Natiahni model
tree = ET.parse(os.path.join(projectDir, 'src', 'model', 'or.archimate'))
ns = {'xsi': "http://www.w3.org/2001/XMLSchema-instance",
      'archimate': 'http://www.archimatetool.com/archimate'}


principlesFolder = tree.getroot().find(".//folder[@name='Motivation']/folder[@name='Princípy VO']", ns)
principlesMD = []
for p in principlesFolder.findall("element[@xsi:type='archimate:Principle']", ns):
    principlesMD.append(am.element2tableRowSimple(p))
am.writeToFile(projectDir, '00-Motivation/principy.md', principlesMD)