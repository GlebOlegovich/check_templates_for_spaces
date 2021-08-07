import os
import sys
from typing import Tuple


BASE_DIR = os.path.dirname(__file__)


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


# Мамкины программисты скажут что глобальные нельзя!
# Нефиг свистеть, отвечу я вам!

# Тэги, которые мы ищим, что бы добавить пробел
TAGS = ['{%', '{{', '}}', '%}']
TAGS_DICT = dict.fromkeys(TAGS, False)
# !!!!!!!!!!

def making_space_in_line(line:str) -> str:
    '''
    Тут делаем пробелы, там, где это надо (в строке HTML кода)
    Не трогайте эту функцию!!!, я з@_б@лсi ее дебажить!!
    '''
    space = ' '

    def add_space(tuple: tuple, tag: str) -> Tuple:
        '''
        Добавляем пробелы
        '''
        out = []

        # Пробел после тэга
        if '{' in tag:
            out.append(tuple[0])
            for count in tuple[1:]:
                if count[0] == space:
                    out.append(count)
                    continue
                else:
                    # Тут у меня закончилась фантазия на названия
                    stroka = space + count
                    out.append(stroka)
                    continue

        # Пробел перед тэгом
        elif tag[-1] == '}':
            for count in tuple[:-1]:
                if count[-1] == space:
                    out.append(count)
                    continue
                else:
                    stroka = count + space
                    out.append(stroka)
                    continue
            out.append(tuple[-1])
        return out

    for tag in TAGS:
        if TAGS_DICT[tag] == True:
            continue
        else:
            if tag in line:
                splited_line = line.split(tag)
                # Добавляем пробелы, если нужны
                splited_line = add_space(splited_line, tag)
                TAGS_DICT[tag] = True
                
                # Похоже, тут без рекурсии никак
                out = f'{tag}'.join(splited_line)
                # Надо проверять, когда перестать уходить в рекурсию!
                if not all(TAGS_DICT.values()):
                    out = making_space_in_line(out)
                return out
            else:
                continue




str = 'раз{{q21 }}два{% ау%}три {{ 12}}{%124414 %}'
print (f'ВОООООТ: {making_space_in_line(str)}')
print (f'А ввели мы {str}')

#asq = ['раз{{ q21 ', 'два{% ау%}три','qwdqwd', 'qwdqdwqdqwddqd']
#print(asq[:-1])

#tuple = ['раз{{q21 }}два', 'ау%}три']
# tag = '{%'
# print (add_space(tuple,tag))



def make_space():
    pass
#print(string.join(map(str, ['two_first_symbols', 111]), ' '))
# def collect_all_html_from_templates_dir(cur_html_file) -> tuple:
    
#     templates = os.path.join(BASE_DIR, 'templates')
#     print(templates) 
#     for i in os.walk(templates):
#         print(i)
#     #print(os.path.join(BASE_DIR, cur_html_file))
#     f = open(f"{os.path.join(templates, cur_html_file)}", 'r')
#     #print(f.read())
def parser_HTML():
    pass
def open_HTML_file(file_name):
    f = open(file_name, 'r')
    print (f.read())
    f.close()
    pass



#if __name__ == '__main__':
#collect_all_html_files()
#take_all_html('index.html')


