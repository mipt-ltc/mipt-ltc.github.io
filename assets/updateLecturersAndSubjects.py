import json
import yaml
from datetime import datetime
import re


# ---------------- creating names sets  ----------------
MIN_TITLE_LENGTH = 2

badNamedNotesAndSubjects = list()
newNames = {'subjects': dict(), 'lecturers': dict()}

def getNotesList():
    printStep('='*10 + ' Extracting notes form the driveTree. ' + '='*10)
    notesList = list()
    for semester in getDriveTree().values():
        for subject in semester["children"].values():
            for id, note in subject["children"].items():
                newNote = {'id': id, 
                    'semester': semester['title'],
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
    with open("../_data/autoGenerated/notesTree.json", "r") as notes:
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
    databases = {'lecturers': getDatabase('../_data/lecturers.yml'),
            'subjects': getDatabase('../_data/subjects.yml')}
    for dbKey in databases:
        printSubstep(' checking ' + dbKey.upper() + ' database ')
        for name, occurrences in namesSet[dbKey].items():
            if not isNameInDatabase(name, databases[dbKey]):
                newNames[dbKey][name] = occurrences
                print('"' + name + '" is not in database.')

def getDatabase(fileName):
    with open(fileName, "r") as f:
        try:
            database = yaml.safe_load(f.read())
        except yaml.YAMLError as exc:
            print(exc)
    return database

def isNameInDatabase(name, database):
    for aliasesStr in database:
        if ('|' + name + '|') in aliasesStr:
            return True
    return False
    
def printStep(message):
    print('\n' + '='*len(message) + '\n' + message + '\n' + '='*len(message))
def printSubstep(message):
    print('\n' + '-'*10 + message + '-'*10)
    
def writeLog():
    with open('../_data/autoGenerated/badNamedNotesAndSubjects.log', 'w+') as f:
        for message in badNamedNotesAndSubjects:
            print(message, file=f)
    writeNewNamesLog('subjects')
    writeNewNamesLog('lecturers')

def writeNewNamesLog(itemType):
    file = '../_data/autoGenerated/new' + itemType.capitalize() + '.yml'
    with open(file, 'w+') as f:
        for name, occurrences in newNames[itemType].items():
            print('- name: "' + name + '"', file=f)
            print('  url:', file=f)
            for note in occurrences:
                print('    - "' + getNoteUrl(note["id"]) + '"', file=f)

def main():
    notesList = getNotesList()
    namesDics = getNamesDics(notesList)
    detectNewNames(namesDics)
    writeLog()


if __name__ == "__main__":
    main()

