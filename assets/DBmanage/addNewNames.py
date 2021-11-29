from fuzzywuzzy import fuzz, process
from constants import *
from updateDBs import getDatabase 
from updateDBs import printSubstep 

MSGS = {
        'createOrUpdate': 'Create new aliases or update old? [new/line number of old]',
        }

def testFunc():
    print(input())

def inputTest():
    print('yoyoyo')
    return input()

# --------
def addNameInSet(name, namesSet):
    name = name.strip()
    if name == '':
        return
    namesSet.add(name)
    
def getStandardizeAliasesStr(aliasesStr):
    aliases = aliasesStr.split('|')
    namesSet = set()
    for name in aliases:
        addNameInSet(name, namesSet)
    if len(namesSet) == 0:
        return ''
    standardizedStr = '|'
    for name in sorted(namesSet):
        standardizedStr += name + '|'
    return standardizedStr

def standardizeNamesAndSort(DBtype):
    with open(DB_FILES[DBtype]['aliases'], 'r') as f:
        lines = f.readlines()
    finalLines = ''
    for line in sorted(lines):
        assert len(line) > 0
        aliasesStr = line[ALIASES_STR_BEGIN:ALIASES_STR_END]
        finalLines += '- "' +\
            getStandardizeAliasesStr(aliasesStr)+ '"\n'
    with open(DB_FILES[DBtype]['aliases'], 'w') as f:
        f.write(finalLines)
# --------------

def getSimilarEntries(nameInfo):
    aliases = getDatabase(DB_FILES[nameInfo['DBtype']]['aliases'])
    ratios = []
    for i in range(len(aliases)): 
        dist = process.extractOne(nameInfo['name'], aliases[i].split('|'))
        ratios.append({'distance': dist, 'line': i, 'aliases': aliases[i]})
    return sorted(ratios, key = lambda entry: -entry['distance'][1])[:5]

def getSetOfLinesWithSimEnties(nameInfo):
    linesSet = set()
    for entry in nameInfo['simNamesInfo']:
        linesSet.add(str(entry['line']))
    return linesSet

def printNameInfo(nameInfo):
    printSubstep('-'*10)
    print('Whant to add "' + nameInfo['name'] + '" in ' + 
            nameInfo['DBtype'] + ' database? [y/n]')
    print('Occurrence(s):')
    for url in nameInfo['url']:
        print(url)
    print('Similar enties in DB:')
    for sim in nameInfo['simNamesInfo']:
        print('  line: ' + str(sim['line']) + 
                '; distance: ' + str(sim['distance']) + 
                '; aliases: ' + sim['aliases'])
 
def handleInput(validAnsSet):
    while True:
        ans = input()
        if ans in validAnsSet:
            return ans

def getAliasesSet(DBtype, line):
    assert DBtype in {'subjects', 'lecturers'}
    assert len(getDatabase(DB_FILES[DBtype]['aliases'])) > line

    return set(getDatabase(DB_FILES[DBtype]['aliases'])[line].split('|'))

def handleAreYouSureInput(nameInfo, startNamesSet, aliases):
    print('Do you whant to add "' + aliases +'"? [y(es)/r(etry)/n(ot)]')
    ans = handleInput({'y', 'n', 'r'}) 
    if ans == 'r': 
        return handleAliasesInput(nameInfo, startNamesSet)
    elif ans == 'y': 
        return aliases 
    else:
        assert ans == 'n'
        return None

def handleAliasesInput(nameInfo, startNamesSet):
    print('List of additional aliases, separated by comma:')
    aliases = getStandardizeAliasesStr(
        '|'.join(list(startNamesSet) + input().split(',')) + '|')
    if aliases == '':
        print("Error: invalid input. Please repeat.")
        return handleAliasesInput(nameInfo, startNamesSet)
    return handleAreYouSureInput(nameInfo, startNamesSet, aliases)

def processName(nameInfo):
    printNameInfo(nameInfo) 
    if handleInput({'y', 'n'}) == 'n':
        return
    print(MSGS['createOrUpdate'])
    ans = handleInput({'new'}.union(getSetOfLinesWithSimEnties(nameInfo)))
    startNamesSet = {nameInfo['name']}
    if ans != 'new':
        startNamesSet |= getAliasesSet(nameInfo['DBtype'], int(ans))
    aliases = handleAliasesInput(nameInfo, startNamesSet)
    if aliases != '':
        if ans != 'new':
            deleteOldLineEntry(nameInfo, int(ans))
        createNewAliasesLine(nameInfo, aliases)

def deleteOldLineEntry(nameInfo, line):
    with open(DB_FILES[nameInfo['DBtype']]['aliases'], 'r') as f:
        lines = f.readlines()
    print(len(lines))
    del lines[line]
    print(len(lines))
    with open(DB_FILES[nameInfo['DBtype']]['aliases'], 'w') as f:
        f.write(''.join(lines))
    printSubstep(' old line deleted successefully ')

def createNewAliasesLine(nameInfo, aliases):
    with open(DB_FILES[nameInfo['DBtype']]['aliases'], 'a') as f:
        print('- "' + aliases + '"', file=f)
    printSubstep(' new aliases successfully added ')

def processNewNames(DBtype):
    namesList = getDatabase(DB_FILES[DBtype]['newNames'])
    if namesList == None:
        return # there is no new names
    for nameInfo in namesList:
        nameInfo['DBtype'] = DBtype
        nameInfo['simNamesInfo'] = getSimilarEntries(nameInfo)
        if nameInfo['name'] != 'null':
            processName(nameInfo)



def main():
    processNewNames('subjects')
    processNewNames('lecturers')
    standardizeNamesAndSort('subjects')
    standardizeNamesAndSort('lecturers')

if __name__ == "__main__":
    main()

