import yaml
from fuzzywuzzy import fuzz, process

from updateDBs import getDatabase 
from updateDBs import printSubstep 
from updateDBs import DB_FILES 
ALIASES_STR_BEGIN = 4
ALIASES_STR_END = -3

def getSimilarEntries(item):
    aliases = getDatabase(DB_FILES['subjects'])
    ratios = []
    for i in range(len(aliases)): 
        dist = process.extractOne(item['name'], aliases[i].split('|'))
        ratios.append({'distance': dist, 'line': i, 'aliases': aliases[i]})
    return sorted(ratios, key = lambda entry: -entry['distance'][1])[:5]

def printWantToAddMessage(item):
    printSubstep('-'*10)
    print('Whant to add "' + item['name'] + '" in subjects database? [y/n]')
    print('Occurrence(s):')
    for url in item['url']:
        print(url)
    print('Similar enties in DB:')
    for sim in getSimilarEntries(item):
        print('  line: ' + str(sim['line']) + 
                '; distance: ' + str(sim['distance']) + 
                '; aliases: ' + sim['aliases'])

def handleWantToAddInput(item):
    printWantToAddMessage(item)
    while True:
        ans = input()
        if ans == 'y' or ans == 'n':
            break
    return ans

def getSetOfLinesWithSimEnties(item):
    linesSet = set()
    for entry in getSimilarEntries(item):
        linesSet.add(entry['line'])
    return linesSet
 
def isLineNumberValid(item, ans):
    return ans.isnumeric() and int(ans) in getSetOfLinesWithSimEnties(item) 

def handleCreateNewOrModifyOld(item):
    print('Do you want create new aliases or add to old? [old/line number]')
    while True:
        ans = input()
        print(type(ans))
        if ans == 'old' or isLineNumberValid(item, ans):
            break
    return ans

def handleAreYouSureInput(item, DBtype, aliases):
    if aliases == None:
        print("Error: invalid input. Please repeat.")
        return handleAliasesInput(DBtype)
    print('Do you whant to add "' + aliases +'"? [y(es)/r(etry)/n(ot)]')
    ans = input()
    while ans != 'y' and ans != 'n' and ans != 'r':
        ans = input()
    if ans == 'r': 
        return handleAliasesInput(item, DBtype)
    else: 
        return {'ans': ans, 'aliases': aliases}


def handleAliasesInput(item, DBtype):
    print('Please list aliases, separated by comma:')
    aliases = getStandardizeAliasesStrOrNull(
        '|'.join([item['name']] + input().split(',')) + '|', DBtype)
    return handleAreYouSureInput(item, DBtype, aliases)

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
        ans = handleCreateNewOrModifyOld(item)
        if ans == 'old':
            createNewAliasesEntry(item, DBtype)
        else: 
            updateOldEntry(item, DBtype, int(ans))

def createNewAliasesEntry(item, DBtype):
    ans = handleAliasesInput(item, DBtype)
    if ans['ans'] == 'n' or ans['aliases'] == None: 
        return
    with open(DB_FILES['subjects'], 'a') as f:
        print('- "' + ans['aliases'] + '"', file=f)
    printSubstep(' new aliases successfully added')

def updateOldEntry(item, DBtype, lineNumber):
    print('ollala')
    aliases = getDatabase(DB_FILES['subjects'])
    with open(DB_FILES[DBtype], 'r') as f:
        DBlines = f.readlines()
    print(DBlines)
    print(item)
    print(DBlines[lineNumber])

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

