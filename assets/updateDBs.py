import json
import yaml
from datetime import datetime
import re


# ---------------- creating names sets  ----------------
MIN_TITLE_LENGTH = 2
TREE_FILE = '../_data/autoGenerated/notesTree.json'
DB_FILES = {'subjects': '../_data/subjects.yml',
        'lecturers': '../_data/lecturers.yml',
        'newSubjects': '../_data/autoGenerated/newSubjects.yml',
        'newLecturers': '../_data/autoGenerated/newLecturers.yml',
        'notesList': '../_data/autoGenerated/notesList.yml',
        'subjectsList': '../_data/autoGenerated/subjectsList.yml'}
LOG_FILE = '../_data/autoGenerated/badNamedNotesAndSubjects.log'

badNamedNotesAndSubjects = list()
newNames = {'subjects': dict(), 'lecturers': dict()}

def getNotesList():
    printStep('='*10 + ' Extracting notes form the driveTree. ' + '='*10)
    notesList = list()
    for semester in getDriveTree().values():
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
    if note['lecturer'] == None:
        printNamingWarning(note, 'note lecturer')

def printNamingWarning(note, item):
    messageHeader = '-'*10 + ' suspicious naming in ' + item.upper() + ' detected ' + '-'*10 + '\n'
    messageBody = 'path: ' + note['semester'] + '/' +\
            note['subject'] + '/' + note['title'] + '\n' +\
            'url: ' + getNoteUrl(note['id']) + '\n'
    messageFooter = '-' * len(messageHeader)
    message = messageHeader + messageBody + messageFooter
    print(message)
    badNamedNotesAndSubjects.append(message)

def getNoteUrl(id):
    return 'https://drive.google.com/file/d/' + id 

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
    if len(lecSplit) == 2 and \
        len(lecSplit[0]) >= MIN_TITLE_LENGTH and lecSplit[1] == 'pdf':
        return lecSplit[0]
    return None

def camelCaseSplit(str):
    return re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', str)).split()
    
def getDriveTree():
    with open(TREE_FILE, "r") as notes:
        return json.loads(notes.read())  

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
            if getNameAliasesOrNull(name,DBs[dbKey]) == None:
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
    return {'lecturers': getDatabase(DB_FILES['lecturers']),
            'subjects': getDatabase(DB_FILES['subjects'])}


def getNameAliasesOrNull(name, database):
    for aliasesStr in database:
        if ('|' + name + '|') in aliasesStr:
            return aliasesStr
    return None

    
def printStep(message):
    print('\n' + '='*len(message) + '\n' + message + '\n' + '='*len(message))
def printSubstep(message):
    print('\n' + '-'*10 + message + '-'*10)
    
def writeLog():
    with open(LOG_FILE, 'w+') as f:
        for message in badNamedNotesAndSubjects:
            print(message, file=f)
    writeNewNamesLog('subjects')
    writeNewNamesLog('lecturers')

def writeNewNamesLog(itemType):
    file = DB_FILES['new' + itemType.capitalize()]
    with open(file, 'w+') as f:
        for name, occurrences in newNames[itemType].items():
            print('- name: "' + name + '"', file=f)
            print('  url:', file=f)
            for note in occurrences:
                print('    - "' + getNoteUrl(note["id"]) + '"', file=f)

# ----------------- generating new DBs ----------------------
def getAliasesStr(name, db, default, default2="default"):
    return (name and getNameAliasesOrNull(name, db)) or default or default2

def createNoteEntry(note, DBs):
    return '- id: "' + note['id'] + '"\n' +\
    '  semester: "' + note['semester'] + '"\n' +\
    '  subject: "' +\
      getAliasesStr(note['subjectName'], DBs['subjects'], note['subject']) + '"\n' +\
    '  year: "' + str(note['year'] or '0') + '"\n' +\
    '  lecturer: "' +\
      getAliasesStr(note['lecturer'], DBs['lecturers'], note['lecturer'], note['title']) + '"\n'


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
    aliases = getAliasesStr(subject, db, occurrences[0]['subjectName']).split('|') 
    assert len(aliases) > 0
    title = (aliases[0] if len(aliases) == 1 else aliases[1])
    return '- title: "' + title + '"\n' +\
            '  semesters: "' + semesters + '"\n'

def generateSubjectsDB(subjectsDic, db):
    subjectsListDB = ''
    for subject, occurrences in subjectsDic.items():
        subjectsListDB += createSubjectEntry(subject, occurrences, db)
    with open(DB_FILES['subjectsList'], 'w+') as f:
        print(subjectsListDB, file=f)

def main():
    notesList = getNotesList()
    namesDics = getNamesDics(notesList)
    detectNewNames(namesDics)
    writeLog()
    generateNotesDB(notesList, getDBs())
    generateSubjectsDB(namesDics['subjects'], getDBs()['subjects'])

if __name__ == "__main__":
    main()

