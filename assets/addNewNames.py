import yaml
from fuzzywuzzy import fuzz

from updateDBs import getDatabase 
from updateDBs import printSubstep 
from updateDBs import DB_FILES 
ALIASES_STR_BEGIN = 4
ALIASES_STR_END = -3

def printWantToAddMessage(item):
    printSubstep('-'*10)
    print('Whant to add "' + item['name'] + '" in subjects database? [y/n]')
    print('Occurrence(s):')
    for url in item['url']:
        print(url)

def handleWantToAddInput(item):
    printWantToAddMessage(item)
    while True:
        ans = input()
        if ans == 'y' or ans == 'n':
            break
    return ans

def handleAreYouSureInput(aliases, DBtype):
    if aliases == None:
        print("Error: invalid input. Please repeat.")
        return handleAliasesInput(DBtype)
    print('Do you whant to add "' + aliases +'"? [y(es)/r(etry)/n(ot)]')
    ans = input()
    while ans != 'y' and ans != 'n' and ans != 'r':
        ans = input()
    if ans == 'r': 
        return handleAliasesInput(DBtype)
    else: 
        return {'ans': ans, 'aliases': aliases}


def handleAliasesInput(item, DBtype):
    print('Please list aliases, separated by comma:')
    aliases = getStandardizeAliasesStrOrNull(
        '|'.join([item['name']] + input().split(',')) + '|', DBtype)
    return handleAreYouSureInput(aliases, DBtype)

def addInSetName(name, namesSet, DBtype):
    if name.strip() == '':
        return
    if DBtype == 'lecturers':
        namesSet.add(name.strip().capitalize())
    namesSet.add(name.strip().lower())

def getStandardizeAliasesStrOrNull(aliasesStr, DBtype):
    aliases = aliasesStr.split('|')
    namesSet = set()
    for name in aliases:
        addInSetName(name, namesSet, DBtype)
    if len(namesSet) == 0:

        return None
    standardizedStr = '|'
    for name in sorted(namesSet):
        standardizedStr += name + '|'
    return standardizedStr

def addNewNames(file, DBtype):
    if getDatabase(file) == None:
        return
    for item in getDatabase(file):
        ans = handleWantToAddInput(item)
        if ans == 'n': 
            continue
        ans = handleAliasesInput(item, DBtype)
        if ans['ans'] == 'n' or ans['aliases'] == None: 
            continue
        with open(DB_FILES['subjects'], 'a') as f:
            print('- "' + ans['aliases'] + '"', file=f)
        printSubstep(' new aliases successfully added')

def standardizeNamesAndSort(DBtype):
    with open(DB_FILES[DBtype], 'r') as f:
        lines = f.readlines()
    finalLines = ''
    for line in sorted(lines):
        assert len(line) > 0
        aliasesStr = line[ALIASES_STR_BEGIN:ALIASES_STR_END]
        finalLines += '- "' +\
            getStandardizeAliasesStrOrNull(aliasesStr, DBtype)+ '"\n'
    with open(DB_FILES[DBtype], 'w') as f:
        f.write(finalLines)

def main():
    addNewNames(DB_FILES['newSubjects'], 'subjects')
    addNewNames(DB_FILES['newLecturers'], 'lecturers')
    standardizeNamesAndSort('subjects')
    standardizeNamesAndSort('lecturers')

if __name__ == "__main__":
    main()

