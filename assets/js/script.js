---
---

function clearFields() {
    document.getElementById('semester').value = '';
    document.getElementById('subject').value = '';
    document.getElementById('year').value = '';
    document.getElementById('lecturer').value = '';
    document.getElementById('notes-list').innerHTML = '';
}
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}
function getDriveUrl(noteId) {
    return 'https://drive.google.com/file/d/' + noteId;
}

function isIncludes(noteVal, userVal) {
    if (userVal == null || userVal == '') {
        return true;
    } else {
        return userVal.includes(noteVal);
    }
}
function getFuzzyMatchScore(noteVal, userVal) {
    if (userVal == null || userVal == '') {
        return 0;
    } else {
        return userVal.includes(noteVal);
    }
}
function getNoteHTML(id, sem, subj, year, lec) {
    return '<div><a href="' + getDriveUrl(id) + '" class="note-btn">' +
        'Sem: ' + sem + 
        '<hr>Subj: ' + subj + 
        '<hr>Year: ' + year +
        '<hr>Lec: ' + lec + '</a></div>';
}

function search() {
    var semester = document.getElementById('semester').value;
    var subject = document.getElementById('subject').value;
    var year = document.getElementById('year').value;
    var lecturer = document.getElementById('lecturer').value;
    
    var notesList = [];
    {% for note in site.data.autoGenerated.notesList %}
        console.assert('{{ note.semester }}'.length == 1);
        if (isIncludes('{{ note.semester}}', semester) &&
            isIncludes('{{ note.year }}', year) &&
            (lecturer == null || '{{ note.lecturer }}'.includes(lecturer))) {
            let aliases = {'subjects': '{{ note.subject }}'.slice(1, -1).split('|'),
                'lecturers': '{{ note.lecturer }}'.slice(1, -1).split('|')};
            results = fuzzysort.go(subject, aliases['subjects'])
            maxScore = Number.NEGATIVE_INFINITY
            results.forEach(function(item, index, array) {
                maxScore < item['score'] ? maxScore = item['score'] : 0;
            })
            notesList.push([maxScore, noteHTML]);
            var noteHTML = getNoteHTML('{{ note.id }}', '{{ note.semester }}', 
            capitalizeFirstLetter(aliases['subjects'][0]), '{{ note.year }}',
            aliases['lecturers'][0]);
        } 
    {% endfor %}
    notesList.sort(function(first, second) {
        return second[0] - first[0];
    });
    var notesListSection = document.getElementById('notes-list');
    notesListSection.innerHTML = '';
    notesList.forEach(function(item, index, array) {
        notesListSection.innerHTML += item[1];
    })
}

