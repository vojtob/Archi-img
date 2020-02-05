import sys
import fileinput

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

if (len(sys.argv) < 3):
    print('usage: text-2-import-requirements.py inFileName outFile')
    print('use default setup')
    inFile = 'C:/Projects_src/Work/temp/req.txt'
    outFile = 'C:/Projects_src/Work/temp/reqelements.csv'
    outFile2 = 'C:/Projects_src/Work/temp/reqrelations.csv'
else:
    inFile = sys.argv[1]
    outFile = sys.argv[2]  

with open(inFile, mode="r", encoding="utf-8") as fin:
    with open(outFile, mode="w", encoding='utf-8') as foutElements:
        foutElements.write('"ID";"Type";"Name";"Documentation"\n')
        with open(outFile2, mode="w", encoding='utf-8') as foutRelations:
            foutRelations.write('"ID";"Type";"Name";"Documentation";"Source";"Target"\n')
            counter = 0
            for line in fin:
                if(line.startswith('P')):
                    # requirement
                    index = line.index('\t')
                    reqText = line[index+1:-1].replace(';', ',').replace('„','').replace('“','')
                    reqNum = line[1:index]
                    reqNum = reqNum.split(".")
                    foutElements.write('"ID-req-P{reqNum[0]:0>1}-{reqNum[1]:0>2}-{reqNum[2]:0>2}";"Requirement";"P{reqNum[0]:0>1}.{reqNum[1]:0>2}.{reqNum[2]:0>2}";"{reqText}"\n'.format(reqNum=reqNum, reqText=reqText, counter=counter))
                    foutElements.write('"ID-ass-P{reqNum[0]:0>1}-{reqNum[1]:0>2}-{reqNum[2]:0>2}";"Assessment";"P{reqNum[0]:0>1}.{reqNum[1]:0>2}.{reqNum[2]:0>2} -> ";""\n'.format(reqNum=reqNum, counter=counter))
                    foutRelations.write('"";"AssociationRelationship";"";"";"ID-ass-P{reqNum[0]:0>1}-{reqNum[1]:0>2}-{reqNum[2]:0>2}";"ID-req-P{reqNum[0]:0>1}-{reqNum[1]:0>2}-{reqNum[2]:0>2}"\n'.format(reqNum=reqNum))
                    counter += 1
                else:
                    # problem
                    print("!!!! PROBLEM ", line)
    print ("{} requirements DONE".format(counter))