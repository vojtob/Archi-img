# -*- coding: utf-8 -*-

import sys
import os

import xml.etree.ElementTree as ET

import archiModel as am

# Poziadavky na deliverables
def reqDeliverables(projectDir):
    reqDeliverables = tree.getroot().find(
        ".//folder[@name='3.1 Požiadavky na organizáciu a výstupy projektu P01-P18']", ns)
    reqMD = []
    for req in reqDeliverables.findall('element'):
        reqMD.extend(am.req2paragraph(req))
        reqMD.append("\n")
    am.writeToFile(projectDir, '90-Project_IS_ORSR/Poziadavky/poziadavky01deliverables.md', reqMD)

# Poziadavky na aplikacne sluzby
def reqAppServices(projectDir):
    md = [[],[]]
    asServicesVO = tree.getroot().find(
        "./folder[@name='Application']/folder[@name='90 Verejné obstarávanie, štúdia']/folder[@name='Aplikačné služby podľa VO']/folder[@name='BRIS']", ns)
    for asVO in asServicesVO.findall("./element[@xsi:type='archimate:ApplicationService']", ns):
        md[0].append(am.element2tableRow(asVO, tree.getroot()))
    asServicesVO = tree.getroot().find(
        "./folder[@name='Application']/folder[@name='90 Verejné obstarávanie, štúdia']/folder[@name='Aplikačné služby podľa VO']/folder[@name='ORSR']", ns)
    for asVO in asServicesVO.findall("./element[@xsi:type='archimate:ApplicationService']", ns):
        md[1].append(am.element2tableRow(asVO, tree.getroot()))
    am.writeToFile(projectDir, '90-Project_IS_ORSR/Poziadavky/poziadavky02appServices.md', md)

# Poziadavky na aplikacne komponenty
def reqComponents(projectDir):
    md = []
    acFolder = tree.getroot().find(
        "./folder[@name='Application']/folder[@name='90 Verejné obstarávanie, štúdia']/folder[@name='Aplikačné komponenty VO']", ns)
    # v adresari so sluzbami z VO prejdem vsetky podfoldre a z nich vypisem vsetky Application Services
    for acVO in acFolder.findall("./element[@xsi:type='archimate:ApplicationComponent']", ns):
        md.append(am.element2tableRow(acVO, tree.getroot()))
    am.writeToFile(projectDir, '90-Project_IS_ORSR/Poziadavky/poziadavky02appComponents.md', md)


## pre kazdy adresar sa vytvori samostatny zoznam poziadaviek
def processFolders(projectDir, folders, mdName):
    reqMD = []
    for folderDesc in folders:
        md = []
        reqMD.append(md)
        reqFolder = tree.getroot().find(".//folder[@name='" + folderDesc + "']", ns)
        for req in reqFolder.findall('element'):
            md.append(am.element2tableRow(req, tree.getroot()))
    am.writeToFile(projectDir, '90-Project_IS_ORSR/Poziadavky/' + mdName + '.md', reqMD)    

## poziadavky zo vsetkych adresarov sa zleju do jedneho zoznamu
def aggregateFolders(projectDir, folders, mdName):
    md = []
    for folderDesc in folders:
        reqFolder = tree.getroot().find(".//folder[@name='" + folderDesc + "']", ns)
        for req in reqFolder.findall('element'):
            md.append(am.element2tableRow(req, tree.getroot()))
    am.writeToFile(projectDir, '90-Project_IS_ORSR/Poziadavky/' + mdName + '.md', md)    


# read project dir from arguments
if (len(sys.argv) < 2):
    print('usage: principles.py projectPath')
    exit(1)
else:
    projectDir = os.path.normpath(sys.argv[1])

# Natiahni model a vyber z neho poziadavky
folderName = '../..'
tree = ET.parse(os.path.join(projectDir, 'src', 'model', 'or.archimate'))
ns = {'xsi': "http://www.w3.org/2001/XMLSchema-instance",
      'archimate': 'http://www.archimatetool.com/archimate'}

reqDeliverables(projectDir)
reqAppServices(projectDir)
reqComponents(projectDir)
# frontend
folders = [ '3.2.2.1 Komponent Informačný portál pre prístup k údajom OR SR',
            '3.2.2.2 Komponent elektronických služieb OR SR pre podávanie návrhov',
            '3.2.2.3 Komponent neverejnej časti OR SR pre agendových pracovníkov']
processFolders(projectDir, folders, 'poziadavky03')
# spracovanie
folders = [ '3.2.3.1 Manažment konaní',
            '3.2.3.2 Elektronický spis',
            '3.2.3.3 Zbierka listín',
            '3.2.4.1 Centrum dátových služieb',
            '3.2.4.2 Centrum webových služieb']
processFolders(projectDir, folders, 'poziadavky04')
# Integracie
folders = [ '3.2.5 Integrácia s BRIS',
            '3.2.6 Integrácia s rezortnými IS MSSR',
            '3.2.7 Integrácia s IS verejnej správy']
aggregateFolders(projectDir, folders, 'poziadavky05')
# Kvalitativne
folders = [ '3.2.8 Kvalitatívne požiadavky']
aggregateFolders(projectDir, folders, 'poziadavky06')
# Technology
folders = [ '3.3.1 Vládny cloud',
            '3.3.2 Systémový softvér',
            '3.3.3 Nasadzovanie a správa systémov',
            '3.3.4 Monitorovanie a dohľad',
            '3.3.5 Zálohovanie',
            '3.3.6 Bezpečnosť operačných systémov']
processFolders(projectDir, folders, 'poziadavky07')
