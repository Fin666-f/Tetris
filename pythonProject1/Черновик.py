def language(change_language=False, change_record=False):
    with open('Tetris_data.txt', 'r', encoding='utf8') as f:
        data = ''.join(f.readlines()).split('\n')
    print(data)
    language = data[0]
    record = data[1]
    f.close
    if change_language:
        if language == 'english':
            language = 'russian'
        else:
            language = 'english'
    if change_record:
        pass
    f1 = open('Tetris_data.txt', 'w', encoding='utf8')
    f1.write('\n'.join([language, record]))

language(True)