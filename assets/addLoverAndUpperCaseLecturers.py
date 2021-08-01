lines = []
with open('../_data/lecturers.yml', 'r') as f:
    lines = f.readlines()

with open('../_data/lecturers.yml', 'w') as f:
    for line in lines:
        names = line[4:-3].split('|')
        namesSet = set()
        for name in names:
            assert len(name) > 0
            namesSet.add(name.capitalize())
            namesSet.add(name.lower())
        newLine = '- "|'
        for name in sorted(namesSet):
            newLine += name + '|'
        newLine += '"\n'

        f.write(newLine)
    
