---
---
function search() {
    var semester = document.getElementById('semester').value;
    var subject = document.getElementById('subject').value;
    var year = document.getElementById('year').value;
    var lecturer = document.getElementById('lecturer').value;

    window.location.href = 'notes?semester=' + semester + 
        '&subject=' + subject + 
        '&year=' + year + 
        '&lecturer=' + lecturer;
}

function clearFields() {
    document.getElementById('semester').value = '';
    document.getElementById('subject').value = '';
    document.getElementById('year').value = '';
    document.getElementById('lecturer').value = '';
}

var noteElement;
function addFilteredNotes() {
    var url = new URL(window.location.href);
    var semester = url.searchParams.get("semester");
    var subject = url.searchParams.get("subject");
    var year = url.searchParams.get("year");
    var lecturer = url.searchParams.get("lecturer");

    document.getElementById('semester').value = semester;
    document.getElementById('subject').value = subject;
    document.getElementById('year').value = year;
    document.getElementById('lecturer').value = lecturer;

    {% for note in site.data.test %}
        if ((semester == null || semester == "" || '{{ note.semester }}' == semester) &&
            (year == null || year == "" || {{ note.year }} == year) &&
            (lecturer == null || '{{ note.lecturer }}'.includes(lecturer))) {
            noteElement = document.getElementById('{{ note.id }}');
            noteElement.innerHTML = '{{note.year}}, {{note.semester}}';
            console.log('yay');
        }
            noteElement = document.getElementById('{{ note.id }}');
            //noteElement.innerHTML = '{{note.lecturer}}~' + lecturer + '~';
        //console.log('{{ note.lecturer }}'.includes(lecturer));
        console.log(lecturer == null || '{{ note.lecturer }}'.includes(lecturer));
    {% endfor %}
}
