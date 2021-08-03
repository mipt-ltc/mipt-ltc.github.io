import yaml

from updateDBs import getDatabase 
from updateDBs import printSubstep 
from updateDBs import DB_FILES 
ALIASES_STR_BEGIN = 4
ALIASES_STR_END = -3

def handleWantToAddInput(item):
    printSubstep('-'*10)
    print('Whant to add "' + item['name'] + '" in subjects database? [y/n]')
    print('Occurrence(s):')
    for url in item['url']:
        print(url)
    while True:
        ans = input()
        if ans == 'y' or ans == 'n':
            break
    return ans

def handleAliasesInput():
    print('list aliases, separated by comma:')
    aliases = getNewAliasesStr(input())
    print('Do you whant to add "' + aliases +'"? [y(es)/r(etry)/n(ot)]')

    while True:
        ans = input()
        if ans == 'y' or ans == 'n' or ans == 'r':
            break
    if ans == 'r': return handleAliasesInput()
    else: return {'ans': ans, 'aliases': aliases}

def getNewAliasesStr(rawStr):
    newAliasesStr = '|'
    for alias in rawStr.split(','):
        newAlias = alias.lower().strip()
        if newAlias != '':
            newAliasesStr += newAlias + '|'
    print(newAliasesStr)
    return newAliasesStr

def addNewNames(file):
    if getDatabase(file) == None:
        return
    for item in getDatabase(file):
        ans = handleWantToAddInput(item)
        if ans == 'n': continue
        ans = handleAliasesInput()
        if ans['ans'] == 'n': continue
        with open(DB_FILES['subjects'], 'a') as f:
            print('- "' + ans['aliases'] + '"', file=f)
        printSubstep(' new aliases successfully added')

def addInSetName(name, namesSet, DBtype):
    if DBtype == 'lecturers':
        namesSet.add(name.capitalize())
    namesSet.add(name.lower())


def standardizeNamesAndSort(DBtype):
    with open(DB_FILES[DBtype], 'r') as f:
        lines = f.readlines()
    finalLines = ''
    for line in sorted(lines):
        assert len(lines) > 0
        names = line[ALIASES_STR_BEGIN:ALIASES_STR_END].split('|')
        namesSet = set()
        for name in names:
            assert len(name) > 0
            addInSetName(name, namesSet, DBtype)
        finalLines += '- "|'
        for name in sorted(namesSet):
            finalLines += name + '|'
        finalLines += '"\n'
    with open(DB_FILES[DBtype], 'w') as f:
        f.write(finalLines)

def main():
    print(DB_FILES)
    addNewNames(DB_FILES['newSubjects'])
    addNewNames(DB_FILES['newLecturers'])
    standardizeNamesAndSort('subjects')
    standardizeNamesAndSort('lecturers')

if __name__ == "__main__":
    main()

