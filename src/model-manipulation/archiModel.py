import os

ns = {'xsi': "http://www.w3.org/2001/XMLSchema-instance",
      'archimate': 'http://www.archimatetool.com/archimate'}

def getElementName(element):
    return element.attrib['name']

def getElementDoc(element):
    eDoc = element.find('documentation')
    if (eDoc == None):
        return '--'
    return eDoc.text.replace('\n', '').replace('\r', '<BR/>').replace(' ', '• ')

def req2paragraph(req):
    # nazov poziadavky
    text = []
    text.append("### " + req.attrib['name'])
    # dokumentacia poziadavky
    d = req.find('documentation')
    text.append("\n" + d.text.replace(' ', '• '))
    # realizacia poziadavky
    return text

def element2tableRow(e, modelRoot):
    # name
    eName = getElementName(e)
    # documentation
    eDoc = getElementDoc(e)
    # realization
    reqReal = []
    relationships = modelRoot.find(".//folder[@name='Relations']", ns)
    eID = e.attrib['id']
    for realizationRelationship in relationships.findall(".//element[@xsi:type='archimate:RealizationRelationship'][@target='"+eID+"']", ns):
        sourceID = realizationRelationship.attrib['source']
        sourceElement = modelRoot.find(".//element[@id='"+sourceID+"']", ns)
        relDoc = '**' + getElementName(sourceElement) + '**: ' + getElementDoc(realizationRelationship)
        reqReal.append(relDoc)
        # reqReal.append(sourceElement.attrib['name'])
    if(len(reqReal) > 0):
        reqReal = "<BR/><BR/>".join(reqReal)
    else:
        reqReal = "--"
    return "| {} | {} | {} |".format(eName, eDoc, reqReal)
    
# bez realizacie
def element2tableRowSimple(e):
    # name
    eName = getElementName(e)
    # documentation
    eDoc = getElementDoc(e)
    return "| {} | {} |".format(eName, eDoc)
    
def writeToFile(projectDir, fileName, mdData):
    fillCounter = 0
    with open(os.path.join(projectDir, 'src', 'specifikacia', fileName), 'r', encoding='utf8') as fIn:
        with open(os.path.join(projectDir, 'temp', 'spec_local', 'content', fileName), 'w', encoding='utf8') as fOut:
            for l in fIn:
                if (l.find('<TO FILL>') > -1):
                    if(isinstance(mdData[0],list)):
                        fOut.writelines('\n'.join(mdData[fillCounter]))
                        fillCounter += 1
                    else:
                        fOut.writelines('\n'.join(mdData))
                else:
                    # normal line
                    fOut.write(l)
    print('Do suboru ' + fileName + ' doplnene aplikacne komponenty')


def testModule(message):
    print("test success: " + message)