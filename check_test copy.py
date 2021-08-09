import os
import sys
from typing import Dict, Tuple, Union


BASE_DIR = os.path.dirname(__file__)

# Мамкины программисты скажут что глобальные нельзя!
# Нефиг свистеть, отвечу я вам!

# Тэги, которые мы ищим, чтобы добавить пробел
TAGS = ['{%', '{{', '}}', '%}', '{#', '#}']
# !!!!!!!!!!
def tags_in_str(str) -> Dict:
    '''
    Смотрим какие теги есть в нашей строке
    '''
    tmp = []
    for tag in TAGS:
        if tag in str:
            tmp.append(tag)
    tags_dict = dict.fromkeys(tmp, False)
    return tags_dict


def selected_templates_dir() -> str:
    '''
    Проверяем есть ли папка templates, если нету - просим ввести папку с шаблонами HTML
    '''
    templates_dir = os.path.join(BASE_DIR, 'templates')
    if os.path.isdir(templates_dir):
        print(f'Найдена папка templates, мне плевать,что ты разместил их не'
              f'там, кожаный ты мешок!\n Буду искать шаблоны в ней!\n\n'
              f'А если все таки ты расположил все в ней, то жди, я работаю,'
              f'пока ты в потолок плюешь!')
    else:
        print(f'В папке {BASE_DIR}, где лежит {os.path.basename(__file__)}, нету каталога templates')
        print(f'Хотите ввести свое название директории (введите любое значение)?\n'
                f'Если не хотите, просто нажмите Enter\n Так что там с вводом,а кожаный мешок ?\n')
        input = input("Ввод: ")
        if input:
            templates_dir = os.path.join(BASE_DIR, input)
            print(f"Ну, давай создадим\n Теперь путь до папки с html шаблонами: {templates_dir}")

        else:
            print(f'Нет, так нет, тогда создайте директорию templates, поместите в нее HTML файлы,'
                    f'и запустити меня вновь, а я подумаю, помогать тебе или нет!')
            sys.exit()
    return templates_dir

def collect_all_html_files(templates_dir: str) -> Tuple:
    '''
    Собираем все файлы html из templates_dir в кортеж
    '''
    path_html_files=[]
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith(".html"):
                path_html_files.append(os.path.join(root, file))
    return path_html_files




# str = '   {{q21 }}'
# print(tags_in_str(str))
def look_line(str):
    space = ' '
    tags = []
    TAGS_DICT = tags_in_str(str)
    for tag in TAGS_DICT:
        tags.append(tag)
    # print(f'Тэги которые у нас есть {tags}')

    def making_space_in_line(line: str) -> str:
        '''
        Тут делаем пробелы, там, где это надо (в строке HTML кода)
        Не трогайте эту функцию!!!, я з@_б@лсi ее дебажить!!
        '''
        def add_space(tuple: tuple, tag: str) -> Tuple:
            '''
            Добавляем пробелы
            '''
            out = []
            # print(f'в add_space предано: {tuple}')
            # Пробел после тэга
            if '{' in tag:
                out.append(tuple[0])
                if tuple[1:]:
                    for count in tuple[1:]:
                        if count.startswith(space):
                            out.append(count)
                            # print(f'принт из if {out}')
                        else:
                            # Тут у меня закончилась фантазия на названия
                            stroka = space + count
                            out.append(stroka)
                            # print(f'принт из элс {out}')
                # else: print(f'ну мы просто пропустили {tag}')
            # Пробел перед тэгом
            elif tag[-1] == '}':
                for count in tuple[:-1]:
                    if count.endswith(space):
                        out.append(count)
                        # print(f'принт из if в elif{out}')
                    else:
                        stroka = count + space
                        out.append(stroka)
                        # print(f'принт из else в elif{out}')
                out.append(tuple[-1])
                # print(f'out в конце elif {out}')
            # print(f'out в конце САМОМ {out}')
            return out
        if tags: 
            for tag in TAGS_DICT:
                # print(f'Тэг который щас {tag}, значение: {TAGS_DICT[tag]}')
                if TAGS_DICT[tag] == False:
                    if tag in line:
                        splited_line = line.split(tag)
                        # print(f'splited_line, до вызова функции {splited_line}')
                        # Добавляем пробелы, если нужны
                        splited_line = add_space(splited_line, tag)
                        # print(f'splited_line, ПОСЛЕ! вызова функции {splited_line}')
                        TAGS_DICT[tag] = True
                        
                        # Похоже, тут без рекурсии никак
                        out = f'{tag}'.join(splited_line)
                        # print(f'tmp: {out}')
                        # Надо проверять, когда перестать уходить в рекурсию!
                        if not all(TAGS_DICT.values()):
                            out = making_space_in_line(out)
                        # print(f'out: {out}')
                        return out
                # else: print('НЕопознаный тег')
        else:   
            return False
    return making_space_in_line(str)




# str = '   {{q21 }}'
# print (f'ВОООООТ: {look_line(str)}')
# print (f'А ввели мы {str}')



# str = "{{post_count.text|linebreaks }}"
# print (f'ВОООООТ: {look_line(str)}')
# print (f'А ввели мы {str}')


def change_line_or_not(line: str, new_line: Union[str, bool]):
    if new_line and not (line == new_line):
        return True
    else:
        return False

def print_fails(errors: Dict):
    if errors.values():
        print(f'\nЭх ты, кожаный ты мой мешок!\n'
               f'У тебя есть ошибки, сейчас покажу тебе их в формате:\n'
               f'Путь к файлу ............... Ошибка\n')
        for file in errors:
            print (file)
            for line in errors[file]:
                print(f'{" "*len(file)}{line}')
    else:
        print (f'\nПо такому случаю, даже не буду назыать тебя '
               f'кожанным мешком!\nТЫ молодец!, у тебя нет '
               f'ошибок! Везде расставил пробелы.')

def checking_templates():
    '''
    Проверяем все наши шаблоны
    '''
    templates_dir = selected_templates_dir()
    all_HTML_files = collect_all_html_files(templates_dir)
    #errors = {'Путь': ['список','твоих', 'косяков']}
    errors = dict()
    #print(errors)

    for file in all_HTML_files:
        f = open(file, "r")
        out_file_name = file + '.correct'
        out_file = open(out_file_name,"a")

        lines_with_errors = []
        while True:
            # считываем строку
            line = f.readline()
            print('Взяли')
            print(line)
            new_line = look_line(line)
            print('Получили')
            print(new_line)
            if change_line_or_not(line, new_line):
                print('До')
                print(lines_with_errors)
                lines_with_errors.append(line)
                print('После')
                print(lines_with_errors)
                # if file in errors:
                #     errors[file] .append(1)
                # errors[file] = list(line)
                print('Реплэйсим')
                out_file.write(new_line)
                #f.replace(line, new_line)
            else: 
                out_file.write(line)
            # прерываем цикл, если строка пустая
            if not line:
                if lines_with_errors:
                    errors[file] = lines_with_errors
                break
        
        print ('fqwqqwf!!!!!!!!!GGWGG')
        print(lines_with_errors)
        #errors[file] = lines_with_errors
        print_fails(errors)
        f.close()
        out_file.close()
        os.rename(out_file_name, file)
    print(errors)

checking_templates()




#if __name__ == '__main__':
#collect_all_html_files()
#take_all_html('index.html')


