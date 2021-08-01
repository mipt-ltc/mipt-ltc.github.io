lines = []
with open('../_data/lecturers.yml', 'r') as f:
    lines = sorted(f.readlines())
with open('../_data/lecturers.yml', 'w') as f:
    f.writelines(lines) 
