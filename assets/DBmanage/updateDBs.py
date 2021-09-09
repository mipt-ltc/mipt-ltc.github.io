import yaml
from datetime import datetime
from constants import *
import re


# ---------------- creating names sets  ----------------
MIN_TITLE_LENGTH = 2

badNamedNotesAndSubjects = list()
newNames = {'subjects': dict(), 'lecturers': dict()}

def getNotesList():
    printStep(' Extracting notes form the driveTree. ')
    notesList = list()
    for semester in getDatabase(TREE_FILE).values():
        for subject in semester["children"].values():
            for id, note in subject["children"].items():
                newNote = {'id': id, 
                    'semester': re.sub("[^0-9]", "", semester['title']),
                    'subject': subject['title'],
                    'title': note['title']}        
                newNote['subjectName'] = getSubjectOrNull(subject['title'])
                newNote['year'], newNote['lecturer'] = getTitleOrNull(note['title'])
                handleNulls(newNote)
                notesList.append(newNote)
    return notesList

def handleNulls(note):
    if note['subjectName'] == None:
        printNamingWarning(note, 'subject')
    if note['year'] == None:
        printNamingWarning(note, 'note year')
    if note['lecturer'] == None or len(note['lecturer']) < MIN_TITLE_LENGTH:
        printNamingWarning(note, 'note lecturer')

def printNamingWarning(note, item):
    messageHeader = getSubstepMessage(' suspicious naming in ' + item.upper() +
            ' detected ') + '\n'
    messageBody = 'path: ' + note['semester'] + '/' +\
            note['subject'] + '/' + note['title'] + '\n' +\
            'url: ' + getNoteUrl(note['id']) + '\n'
    messageFooter = '-' * len(messageHeader)
    message = messageHeader + messageBody + messageFooter
    print(message)
    badNamedNotesAndSubjects.append(message)

def getNoteUrl(id):
    return DRIVE_PDF_URL + id 

def getSubjectOrNull(title):
    if '|' not in title and len(title) >= MIN_TITLE_LENGTH:
        extractedWords = []
        substrings = title.split('_')
        for substr in substrings:
            extractedWords += camelCaseSplit(substr)
        return ' '.join(extractedWords).lower()
    return None

def getTitleOrNull(title):
    if '|' not in title:
        nameSplit = title.split('_', 1)
        if (len(nameSplit) == 2):
            year = getYearOrNull(nameSplit[0])
            lecturer = getLecturerOrNull(nameSplit[1])
            return year, lecturer
    return None, None

def getYearOrNull(year):
    if year.isnumeric() and int(year) <= datetime.now().year:
        return int(year)
    return None

def getLecturerOrNull(lecturer):
    lecSplit = lecturer.split('.')
    if len(lecSplit) == 2 and lecSplit[1] == 'pdf':
        return lecSplit[0]
    return None

def camelCaseSplit(str):
    return re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', str)).split()
    
def getNamesDics(notesList):
    namesDics = {'subjects': dict(), 'lecturers': dict()}
    for note in notesList:
        addNamesInSets(note, namesDics)
    return namesDics

def addNamesInSets(note, namesDics):
    if note['subjectName'] != None:
        namesDics['subjects'].setdefault(note['subjectName'],[]).append(note)
    if (note['year'] != None and note['lecturer'] != None):
        namesDics['lecturers'].setdefault(note['lecturer'],[]).append(note)

# ---------------- detecting new names ----------------
def detectNewNames(namesSet):
    printStep('='*10 + ' Checking if names in database. ' + '='*10)
    DBs = getDBs()
    for dbKey in DBs:
        printSubstep(' checking ' + dbKey.upper() + ' database ')
        for name, occurrences in namesSet[dbKey].items():
            if getNameAliasesOrNull(name, DBs[dbKey]) == None:
                newNames[dbKey][name] = occurrences
                print('"' + name + '" is not in database.')

def getDatabase(fileName):
    with open(fileName, "r") as f:
        try:
            database = yaml.safe_load(f.read())
        except yaml.YAMLError as exc:
            print(exc)
    return database

def getDBs():
    return {'lecturers': getDatabase(DB_FILES['lecturers']['aliases']),
            'subjects': getDatabase(DB_FILES['subjects']['aliases'])}


def getNameAliasesOrNull(name, database):
    name = name.lower()
    for aliasesStr in database:
        namesSet = set([delCommandSymbFromStr(name) for name in aliasesStr[1:-1].split('|')])
        if name in namesSet:
            return aliasesStr
    return None


def getStepMessage(message):
    diff = (80 - len(message)) // 2
    if diff > 0:
        message = '='*diff + message + '='*diff
    return '\n' + '='*len(message) + '\n' + message + '\n' + '='*len(message)

def printStep(message):
    print(getStepMessage(message))
def getSubstepMessage(message):
    diff = (80 - len(message)) // 2
    if diff > 0:
        message = '-'*diff + message + '-'*diff
    return '\n' + message

def printSubstep(message):
    print(getSubstepMessage(message))
    
def writeLog():
    with open(LOG_FILE, 'w+') as f:
        for message in badNamedNotesAndSubjects:
            print(message, file=f)
    writeNewNamesLog('subjects')
    writeNewNamesLog('lecturers')

def writeNewNamesLog(itemType):
    file = DB_FILES[itemType]['newNames']
    with open(file, 'w+') as f:
        for name, occurrences in newNames[itemType].items():
            print('- name: "' + name + '"', file=f)
            print('  url:', file=f)
            for note in occurrences:
                print('    - "' + getNoteUrl(note["id"]) + '"', file=f)

# ----------------- generating new DBs ----------------------
def getAliasesStr(name, db, default, default2="default"):
    if name == None:
        return default or default2
    aliasesStr = getNameAliasesOrNull(name, db)
    if aliasesStr:
        assert len(aliasesStr) > 2
        aliasesStr = aliasesStr[1:-1]
    return aliasesStr or default or default2

def hasCyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def extractOneName(aliasesStr):
    aliases = aliasesStr.split('|')
    assert len(aliases) > 0
    for name in aliases:
        if name[0] == '$':
            assert len(name) > 1 + MIN_TITLE_LENGTH
            if name[1] == '#':
                return name[2:].upper()
            return name[1:].capitalize()
        if hasCyrillic(name):
            return name.capitalize()
    assert len(aliases) > 0
    print('Warning: "' + aliasesStr +'" have no russian alias (or not in DB)')
    return aliases[0].capitalize()

def delCommandSymbFromStr(name):
    cmdSymbSet = {'$', '#'}
    while name[0] in cmdSymbSet:
        name = name[1:]
    return name

def processAliasesStr(aliasesStr):
    aliases = aliasesStr.split('|')
    namesSet = set()
    for name in aliases:
        name = delCommandSymbFromStr(name)
        namesSet |= {name.lower(), name.upper(), name.capitalize()}
    return '|'.join(sorted(namesSet))


def createNoteEntry(note, DBs):
    subjectsStr = getAliasesStr(note['subjectName'], DBs['subjects'], 
            note['subject'])
    lecturersStr = getAliasesStr(note['lecturer'], DBs['lecturers'], 
            note['lecturer'], note['title']) 
    return '- id: "' + note['id'] + '"\n' +\
    '  semester: "' + note['semester'] + '"\n' +\
    '  subject: "' + subjectsStr + '"\n' +\
    '  subjectTitle: "' + extractOneName(subjectsStr) + '"\n' +\
    '  year: "' + str(note['year'] or '0') + '"\n' +\
    '  lecturer: "' + processAliasesStr(lecturersStr) + '"\n' +\
    '  lecturerTitle: "' + extractOneName(lecturersStr) + '"\n'


def generateNotesDB(notesList, DBs):
    notesListDB = ''
    for note in notesList:
        notesListDB += createNoteEntry(note, DBs)
    with open(DB_FILES['notesList'], 'w+') as f:
        print(notesListDB, file=f)

def createSubjectEntry(subject, occurrences, db):
    semesters = set()
    for note in occurrences:
        semesters.add(note['semester'])
    assert len(semesters) > 0
    semesters = ','.join(sorted(semesters))
    title = extractOneName(getAliasesStr(subject, db, 
        occurrences[0]['subjectName']))
    return '- title: "' + title + '"\n' +\
            '  semesters: "' + semesters + '"\n'

def generateSubjectsDB(subjectsDic, db):
    subjectsListDB = ''
    for subject, occurrences in subjectsDic.items():
        subjectsListDB += createSubjectEntry(subject, occurrences, db)
    with open(DB_FILES['subjects']['list'], 'w+') as f:
        print(subjectsListDB, file=f)

def generateDBs(notesList, namesDics):
    printStep(' generating DBs ')
    generateNotesDB(notesList, getDBs())
    generateSubjectsDB(namesDics['subjects'], getDBs()['subjects'])

def main():
    notesList = getNotesList()
    namesDics = getNamesDics(notesList)
    detectNewNames(namesDics)
    generateDBs(notesList, namesDics)
    writeLog()

if __name__ == "__main__":
    main()

