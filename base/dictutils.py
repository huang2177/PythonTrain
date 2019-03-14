with open('1-intext.txt', 'r') as reader:
    for line in reader.readlines():
        if line.startswith(':'):
            line = line[1:]
        if line.endswith(':'):
            line = line[-1]
        array = line.strip('  \n \t \r').split(":")
        with open('1-outdict.txt', 'a') as writer:
            writer.write(f"'{array[0]}'" + ':' + f"'{array[1]}',\n")
