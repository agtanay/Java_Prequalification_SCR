import os
import re

def recurCheck(tbf, depList):
    pc = 0
    cc = 1
    Found = False
    temp = tbf
    for fd in depList:
        if temp in fd:
            Found = True
            print('found')
        else:
            i = 0
            print(tbf)
            print('notFound')
            while i < 3:
                patt = r"\.\w+$"
                temp = re.sub(patt, '', temp)
                if temp in fd:
                    Found = True
                    break
            i += 1
        if Found:
            break
    return Found


def getImport(source_path):
    pattern = r"import (.*);"

    isis = []
    # parse all the java files for import statements
    for dir, subdirs, files in os.walk(source_path):
        for file in files:
            if file.endswith('.java'):
                try:
                    java_file = open(os.path.join(dir, file))
                    for line in java_file.readlines():
                        if re.match(pattern, line):
                            temp = line.strip("\n").strip(";").replace('import ', "").replace('static ', '')
                            if not (any([re.match("(.)*.junit.(.)*", line), re.match("(.)*.fasterxml.(.)*", line),
                                         re.match("(.)*java.(.)*", line), re.match("(.)*javax.(.)*", line),
                                         re.match("(.)*.xlf4.(.)*", line), re.match("(.)*.spring.(.)*", line),
                                         re.match("(.)*.log4j.(.)*", line), re.match("(.)*.apache.(.)*", line),
                                         re.match("(.)*.sun.(.)*", line)])):
                                isis.append(temp)
                            del temp
                except Exception as e:
                    print(str(e))
                    pass

    isis = list(set(isis))
    return isis


def parseDep(isis, source_path):
    tbr = source_path.replace('\\', '.')
    depList = []
    for dir, subdirs, files in os.walk(source_path):
        for file in files:
            if file.endswith('.java') or file.endswith('.class'):
                depList.append(os.path.join(dir, file).replace('\\', '.').replace(tbr, ''))

    notFound = []
    yesFound = []

    depList = list(set(depList))

    for item in depList:
        open('totalDepUsedInCode.txt', 'a+').write(item + "\n")

    for dep in isis:
        Found = False
        for dep2 in depList:
            if dep in dep2:
                Found = True
                yesFound.append(dep)
                break
            else:
                patt = r"\.\w+$"
                td = dep.split('.')[-1]
                # print(td, dep.split('.')[-1])
                if td.isupper() or td == '*':
                    temp = re.sub(patt, '', dep)
                    if temp in dep2:
                        Found = True
                        yesFound.append(dep)
        if not Found:
            notFound.append(dep)


    print(len(isis))
    print(len(list(set(yesFound))))
    print(len(list(set(notFound))))

    for item in notFound:
        open('depNotPresentInCode.txt', 'a+').write(item + "\n")
    return notFound


def startCheckDep():
    source_path = r"C:\Users\tanay\Documents\spbrd (1)\spbrd"  # input("Enter the absolute path to the source folder :\n")
    isis = getImport(source_path)

    retList = parseDep(isis, source_path)


startCheckDep()