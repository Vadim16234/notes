import datetime
import json
from os import name,system
from copy import deepcopy


class Note:
    __id = []
    def __new__(cls):
        cls.__id.append(get_new_id())
        if len(cls.__id)>=2 and cls.__id[-2] >= cls.__id[-1]:
            cls.__id[-1] = cls.__id[-2] + 1
        return super().__new__(cls)

    def __init__(self):
        self.id = self.get_id()
        self.date = None
    
    @classmethod
    def get_id(cls):
        return cls.__id[-1]
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self,d):
        self._data = d

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self,t):
        self._title = t


class ListNotes:
    def __init__(self):
        self.notes = {}

    def edit(self,mode = 'notes',obj = None):
        if mode == 'json':
            note = obj
        else:
            id = ''
            while not id.isdigit():
                id = input('''Введите id заметки которую хотите изменить либо print для вывода всех заметок в буффере
                Ваш выбор: ''')
                if id == 'print':
                    self.print()
            try:
                note = self.notes[int(id)]
            except KeyError:
                print('Такой записки нет')
                return

        choose = input(
        '''Что вы хотите изменить?
        0 - заголовок
        1 - тело заметки
        2 - всю заметку(и заголовок и тело)
        Любой другой символ - если хотите выйти без изменений
        Ваш выбор: ''')
        if choose == '0':
            print(f'Ваш текущий заголовок:\n{note.title}')
            tmp = note.title
            note.title = input('Введите новый(если хотите отменить,то введите 9): ')
            if note.title == '9':
                note.title = tmp
        elif choose == '1':
            print(f'Ваши текущие записи:\n{note.data}')
            tmp = note.data
            note.data = input('Введите новые записи(если хотите отменить,то введите 9): ')
            if note.data == '9':
                note.data = tmp
        elif choose == '2':
            print(f'Ваша текущая заметка:\n{note.title}\n{note.data}')
            tmp = (note.title,note.data)
            note.title = input('Введите новый заголовок(если хотите отменить,то введите 9): ')
            if note.title == '9':
                note.title = tmp[0]
            note.data = input('Введите новые записи(если хотите отменить,то введите 9): ')
            if note.data == '9':
                note.data = tmp[1]
        else:
            print('Выход без изменений...')
        if choose in ('0','1','2'):
            note.date = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
            return note

    def add(self):
        tmp = Note()
        tmp.title = input('Введите заголовок: ')
        tmp.data = input('Введите тело заметки: ')
        tmp.date = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
        self.notes[tmp.id] = tmp
        print('Заметка сохранена')

    def rm(self):
        id = ''
        while not id.isdigit():
            if id != 'print' and id != '':
                print('Выход без изменений...')
                return
            id = input('''Введите id заметки которую хотите удалить 
            либо print для вывода всех заметок в буффере
            либо другой символ чтобы выйти без изменений
            Ваш выбор: ''')
            if id == 'print':
                self.print()
        res = self.notes.pop(id:=int(id),f'Заметка №{id} не найдена')
        if type(res)==str and not res.isdigit():
            print(res)
        else:
            print(f'Заметка ({res}) удалена')
    
    def output(self):
        mode = input('''Вы хотите добавить в файл новые заметки или полностью перезаписать файл?
        (будут внесены только текущие заметки. Какие именно - команда print)
        1 - добавить
        0 - перезаписать
        print - посмотреть текущие заметки
        Любой другой символ - выйти без изменений\nВаш выбор: ''')
        while mode not in ('1','0'):
            if mode == 'print':
                clear()
                self.print()
            else:
                return
            mode = input('''Вы хотите добавить в файл новые заметки или полностью перезаписать файл?
        (будут внесены только текущие заметки. Какие именно - команда print)
        1 - добавить
        0 - перезаписать
        print - посмотреть текущие заметки
        Любой другой символ - выйти без изменений\nВаш выбор: ''')
            
        out = {}
        for i in self.notes.items():
            c = i[1]
            out[i[0]]={'id':c.id,
                       'Заголовок':c.title,
                       'Тело':c.data,
                       'Последнее изменение':c.date}
        if bool(int(mode)):
            mode = 'a'
        else:
            mode = 'w'

        with open('NOTES.json',mode,encoding='UTF-8') as dt:
            res = []
            if mode == 'a':
                try:
                    dat = open('NOTES.json','r',encoding='UTF-8')
                    tmp = json.load(dat)
                    open('NOTES.json','w').close()
                    if len(tmp) > 0:
                        for i in tmp:
                            res.append(i)
                    else:
                        res.append(tmp[0])
                    dat.close()
                except:
                    pass
            open('NOTES.json','w').close()
            if len(out) != 0:
                res.append(out)
            json.dump(res,dt,ensure_ascii=False,indent=4)
            
        
    def input(self):
        with open('NOTES.json','r',encoding='UTF-8') as dt:
            try:
                item = json.load(dt)
                for i in item:
                    for _,j in i.items():
                        print('-------------')
                        for k in j.items():
                            print(f'{k[0]} - {k[1]}')
                print('-------------')
            except:
                print('Файл json пуст')

    def print(self):
        if len(self.notes)>0:
            for item in self.notes.items():
                print('----------------------')
                print(f'id:{item[0]}')
                print(item[1].title)
                print(item[1].data)
                print(f'Последняя дата изменения: {item[1].date}')
                print('----------------------\n')
        else:
            print('Ваш список заметок пустой')
        
    def clear(self):
        tmp = input('   вы уверены что хотите удалить ВСЕ заметки?\n1 - да\n0 - нет\nВаш выбор: ')
        if int(tmp):
            open('NOTES.json','w').close()
        else:
            print('Вы ничего не удалили')

    def edit_json(self):
        id = input('''Введите id заметки которую хотите отредактировать из файла json 
            либо im для вывода всех заметок в файле json
            либо другой символ чтобы выйти без изменений
            Ваш выбор: ''')
        while not id.isdigit():
            if id == 'im':
                self.input()
            else:
                return
            id = input('''Введите id заметки которую хотите отредактировать из файла json 
            либо im для вывода всех заметок в файле json
            либо другой символ чтобы выйти без изменений
            Ваш выбор: ''')

        with open('NOTES.json','r',encoding='UTF-8') as data:
            try:
                js = json.load(data)
            except:
                print('Файл json пуст')
                return
            break_flag = False
            find_flag = False
            open('NOTES.json','w').close()
            tmp_note = Note()

            for i in js:
                if break_flag:
                    break

                for _,j in i.items():
                    if break_flag:
                        break

                    for k in j.items():
                        if str(k[1]) == id or find_flag:
                            break_flag = True
                            tmp_note.id = k[1]
                            find_flag = True
                            if k[0] == 'Заголовок':
                                tmp_note.title = k[1]
                            if k[0] == 'Тело':
                                tmp_note.data = k[1]
            
            if find_flag:
                reserv_tmp_note = deepcopy(tmp_note)
                tmp_note = self.edit('json',tmp_note)
                if tmp_note == None:
                    tmp_note = reserv_tmp_note
            else:
                print(f'Такого id({id}) не существует')
            
        with open('NOTES.json','a',encoding='UTF-8') as data:
            break_flag = False
            find_flag = False
            for i in enumerate(js):
                if break_flag:
                    break
                for _,j in enumerate(i[1].items()):
                    if break_flag:
                        break
                    for k in j[1].items():
                        if str(k[1]) == id or find_flag:
                            break_flag = True
                            find_flag = True
                            if k[0] == 'id':
                                js[i[0]][j[0]]['id'] = k[1]
                            if k[0] == 'Заголовок':
                                js[i[0]][j[0]]['Заголовок'] = tmp_note.title
                            if k[0] == 'Тело':
                                js[i[0]][j[0]]['Тело'] = tmp_note.data
                            if k[0] == 'Последнее изменение':
                                js[i[0]][j[0]]['Последнее изменение'] = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
            json.dump(js,data,ensure_ascii=False,indent=4)

    def del_from_json(self):
        id = input('''Введите id заметки которую хотите удалить из файла json 
            либо im для вывода всех заметок в файле json
            либо другой символ чтобы выйти без изменений
            Ваш выбор: ''')
        while not id.isdigit():
            if id == 'im':
                self.input()
            else:
                return
            id = input('''Введите id заметки которую хотите удалить из файла json 
            либо im для вывода всех заметок в файле json
            либо другой символ чтобы выйти без изменений
            Ваш выбор: ''')

        with open('NOTES.json','r',encoding='UTF-8') as data:
            try:
                js = json.load(data)
            except:
                print('Файл json пуст')
                return
            break_flag = False
            find_flag = False
            open('NOTES.json','w').close()

            for i in js:
                if break_flag:
                    break

                for _,j in i.items():
                    if break_flag:
                        break

                    for k in j.items():
                        if str(k[1]) == id or find_flag:
                            break_flag = True
                            find_flag = True

            if find_flag:
                link = deepcopy(js)
                with open('NOTES.json','a',encoding='UTF-8') as data:
                    break_flag = False
                    find_flag = False
                    for i in enumerate(link):
                        if break_flag:
                            break
                        for _,j in enumerate(i[1].items()):
                            if break_flag:
                                break
                            for k in j[1].items():
                                if str(k[1]) == id:
                                    break_flag = True
                                    del js[i[0]][j[0]]
                                    if len(js[i[0]]) == 0:
                                        del js[i[0]]
                                    break
                    if len(js) != 0:
                        json.dump(js,data,ensure_ascii=False,indent=4)
                    else:
                        pass
            else:
                print(f'Такого id({id}) не существует')
            
                

def clear():  
    if name == 'nt':  
        _ = system('cls')
    else:  
        _ = system('clear')

def get_new_id():
    with open('NOTES.json','r',encoding='UTF-8') as data:
        try:
            tmp = json.load(data)
            res = tmp[-1]
            return res[str(max(map(int,res.keys())))]['id'] + 1
        except:
            return 1

def commands():
    print('''Доступные команды:
    add - создать заметку
    edit - редактировать заметку
    edjs - редактировать заметку из файла json
    rm - удалить заметку
    rmjs - удалить элемент из файла json
    ex - отправить все ваши заметки в json файл
    im - вывести в консоль все заметки из json файла
    clear - очистить json файл
    print - вывести все ваши заметки в консоль
    exit - закрыть приложение "Заметки"''')


prog = True
print('Здравствуйте! Это приложение "Заметки"')
List = ListNotes()
while prog:
    commands()
    print('Введите команду: ')
    tmp = input()
    clear()
    match tmp:
        case 'add':
            List.add()
        case 'edit':
            List.edit()
        case 'edjs':
            List.edit_json()
        case 'rm':
            List.rm()
        case 'rmjs':
            List.del_from_json()
        case 'ex':
            List.output()
        case 'im':
            List.input()
            print('-------------')
        case 'clear':
            List.clear()
        case 'print':
            List.print()
        case 'exit':
            prog = False
        case _:
            print('Неверная команда')
clear()
print('Пока-пока))')