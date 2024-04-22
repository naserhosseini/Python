xml_file_path='./Docs/test.xml'
i = 0
with open(xml_file_path, 'r') as f:
    line = f.readline().strip()
    while(line):
        print(line)
        if line[1] == '/':
            i += 1
        line = f.readline().strip()

print(i)

