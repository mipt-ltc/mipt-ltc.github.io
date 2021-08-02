def main():
    for dbKey in ['lecturers', 'subjects']:
        with open('../_data/'+ dbKey + '.yml', 'r') as f:
            lines = sorted(f.readlines())
        with open('../_data/'+ dbKey + '.yml', 'w') as f:
            f.writelines(lines) 


if __name__ == "__main__":
    main()

