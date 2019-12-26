import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import sqlite3
from random import choice


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_menu.ui', self)
        self.new_game.clicked.connect(self.start_new)
        self.continue_.clicked.connect(self.start)
        con = sqlite3.connect('dat.db')
        cur = con.cursor()
        self.day = cur.execute("""SELECT num from data 
                            where name = 'day'""").fetchall()[0][0]
        con.close()
        self.game = Game(self.day)

    def start(self):
        if self.day == 0:
            self.continue_.setText("Вы еще не начинали игру.")
        else:
            self.game.start_game(0)
            self.close()

    def start_new(self):
        self.day = 0
        self.game.start_game(0)
        self.close()


class Preview(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('preview.ui', self)
        self.ok.clicked.connect(self.close)


class Game(QWidget):
    def __init__(self, day):
        super().__init__()
        uic.loadUi('game_menu.ui', self)
        con = sqlite3.connect('dat.db')
        cur = con.cursor()
        self.money = cur.execute("""SELECT num from data 
                    where name = 'money'""").fetchall()[0][0]
        self.free_error_a = cur.execute("""SELECT num from data 
                    where name = 'a'""").fetchall()[0][0]
        self.free_error_d = cur.execute("""SELECT num from data 
                    where name = 'd'""").fetchall()[0][0]
        con.close()
        self.choice = ''
        self.weight_menu = Weight()
        self.arrest.clicked.connect(self.arrest_pass)
        self.no.clicked.connect(self.not_pass)
        self.ye.clicked.connect(self.yes_pass)
        self.day = 4
        self.info = Info()
        self.txt = ''
        self.pre = Preview()
        self.passport = Passport()
        self.preview = Preview()
        self.pass_ = Pass()
        self.count = 0
        self.scanner = Scanner()
        self.name_list = [["Алексей", "Валера", "Николай", "Артем"], ["Елена", "Анна", "Елизавета", "Александра"]]
        self.second_name_list = [" Cмычко", " Дружко", " Хайпбист", " Абаченко"]
        self.country = ['Экситус', 'Лапландия', 'ГДР', 'Чехословакия']
        self.hi = [': Привет!', ': Здравствуйте!', ': Салам!']
        self.give = [': На!', ': Держите', ': Забирай!']
        self.face = ['( ͡° ͜ʖ ͡°)', 'ʕ•ᴥ•ʔ', '◉_◉', '(¬‿¬)']
        self.error = ['n', 'n', 'n', 'n', 'd', 'd', 'd', 'a', 'a', 'a']
        self.weight = [i for i in range(50, 90)]
        self.date_1 = [i for i in range(self.day + 1, 31)]
        self.date_2 = [i for i in range(1, 10)]

    def generate(self):
        self.er = choice(self.error)
        print(self.er)
        p = choice([0, 1])
        if p:
            gender = 'Ж'
        else:
            gender = 'М'
        a = choice(self.face), gender, choice(self.name_list[p]) + choice(self.second_name_list), choice(
            self.country), 'ϒ'
        return a

    def start_game(self, wrong):
        self.show()
        self.info.show()
        if self.count == 10:
            self.day += 1
            self.count = 0
        if self.day == 0:
            inf = 'Дата: 2.1.83\nПечать паспорта: ϒ\nПечать разрешения на въезд: ψ'
            self.info.change(inf)
            if self.count == 0:
                if wrong == 1:
                    self.change('*Документы приезжего в порядке*')
                else:
                    self.er = 'n'
                    self.passport.show()
                    face = choice(self.face)
                    self.passport.change(face, 'M', choice(self.name_list[0]) + choice(self.second_name_list),
                                         'Экситус', 'ϒ', '20.1.83', 57)
                    self.preview.show()
                    self.change('*Это ваш первый рабочий день. Приступим!*')
                    self.change('Вы: Здравствуйте!')
                    self.change(face + ': Приветствую')
                    self.change('Вы: Документы, пожалуйста')
                    self.change(face + ': Вот, держите')
            if self.count == 1:
                if wrong == 1:
                    self.change('*Документы приезжего просрочены*')
                else:
                    self.er = 'd'
                    self.passport.show()
                    name_local = choice(self.name_list[1]) + choice(self.second_name_list)
                    self.passport.change('ʕ•ᴥ•ʔ', 'Ж', name_local, 'Лапландия', 'ϒ', '1.4.83', 72)
                    self.pass_.change(name_local, 'Лапландия', 'ψ', '1.1.83')
                    self.pass_.show()
                    self.change('Вы: Здравствуйте!')
                    self.change('ʕ•ᴥ•ʔ' + ': Хай')
                    self.change('Вы: Документы, пожалуйста')
                    self.change('ʕ•ᴥ•ʔ' + ': Так, вот')
            if self.count == 2:
                if wrong == 0:
                    self.pass_.show()
                    self.change('ʕ•ᴥ•ʔ: Нет, стоп, пустите, прошел всего лишь один день!')
                if wrong == 1:
                    self.change('*Документы приезжего просрочены*')
            if self.count == 3:
                if wrong == 1:
                    if self.choice == 'd':
                        self.change("*'Необходимо задержать приезжего для выяснения обстоятельств'*")
                    else:
                        self.change(
                            'Вы: Проходите\n{}: Благодарю\n*Приезжий проходит границу, начинает бежать к блокпосту*\n*ВЗРЫВ!!!*\n*В результате вашего халатного отношения к работе пострадали четверо сотрудников пограничной охраны, вам будет выписан выговор.*'.format(
                                '◉_◉'))
                        self.count += 2
                        self.start_game(0)
                else:
                    self.er = 'a'
                    self.passport.show()
                    name_local = choice(self.name_list[0]) + choice(self.second_name_list)
                    self.passport.change('◉_◉', 'М', name_local, 'ГДР', 'ϒ', '11.2.83', 60)
                    self.pass_.change(name_local, 'гдр', 'ζ', '5.1.83')
                    self.pass_.show()
            if self.count == 4:
                self.choice = ''
                self.change("*Вы вызвали охрану*\n*Приезжий был задержан*")
                self.count += 1
                self.start_game(0)
            if self.count == 5:
                self.day = 1
                self.count = 0
                self.start_game(0)

        else:
            if self.count == 0 and self.day == 1:
                self.change("*День второй*")
            if self.count == 0 and self.day == 2:
                self.change("*День третий*")
            if self.count == 0 and self.day == 3:
                self.change("*День четвертый*")
            if self.count == 0 and self.day == 4:
                self.change("*День пятый*")
            if wrong == 1:
                pass
            else:
                inf = 'Дата: 3.1.83\nПечать паспорта: ϒ\nПечать разрешения на въезд: ψ'
                self.info.change(inf)
                gen = list(self.generate())
                self.change('Вы: Здравствуйте!')
                self.change(gen[0] + choice(self.hi))
                self.change('Вы: Документы, пожалуйста')
                self.change(gen[0] + choice(self.give))
                mark = 'ψ'
                mark_2 = 'τ'
                if self.er == 'd':
                    a = choice(['', 1])
                    if a:
                        data_pass = self.generate_date(1)
                        data_prp = self.generate_date(0)
                    else:
                        data_pass = self.generate_date(1)
                        data_prp = self.generate_date(1)
                else:
                    data_pass = self.generate_date(0)
                    data_prp = self.generate_date(0)
                if self.er == 'd':
                    a = choice(['', 1])
                    if a:
                        data_pass = self.generate_date(1)
                        data_prp = self.generate_date(0)
                    else:
                        data_pass = self.generate_date(1)
                        data_prp = self.generate_date(1)
                weight = choice(self.weight)
                weight_2 = weight
                scan = 1
                if self.er == 'a':
                    gen, mark, mark_2, weight_2, scan = self.create_error(gen, weight)
                if self.day >= 2:
                    self.weight_menu.show()
                self.passport.show()
                self.pass_.change(*gen[2:4], mark, data_prp)
                self.passport.change(*gen, data_pass, weight)
                self.weight_menu.change(*gen[2:4], mark_2, weight_2)
                if self.day < 3:
                    if gen[-2] != 'Экситус':
                        self.pass_.show()
                else:
                    self.pass_.show()
                if self.day == 4:
                    self.scanner.info(scan)
                    self.scanner.show()
    def generate_date(self, flag):
        data = str(choice(self.date_1)) + '.' + str(choice(self.date_2))
        if flag == 1:
            a = choice(['', 1, 1])
            if a:
                data = data + '.82'
            else:
                data = str(self.day) + '.1'
                data = data + '.83'
        else:
            data = data + '.83'
        return data

    def create_error(self, gen, v):
        scan = 1
        w = v
        a = choice(['', 1, 2])
        if self.day >= 2:
            a = choice([a, a, 'v'])
        if self.day == 4:
            a = choice([a, a, 's'])
        mark = 'ψ'
        mark_2 = 'τ'
        if gen[-2] == 'Экситус':
            a = 1
        if a == 1:
            a = choice(['', 1])
            if a:
                gen[-1] = 'ξ'
            else:
                gen[-1] = 'ζ'
        if a == 2:
            mark = 'ζ'
        if a == 's':
            scan = 0
        if a == 2 and self.day >= 2:
            mark_2 = 'ζ'
        if a == '':
            name = gen[-3].split()
            num = name[0].find('а')
            name_1 = list(name[0].lower())
            name_1[num] = 'о'
            name[0] = ''.join(name_1).title()
            gen[-3] = ' '.join(name)
        if a == 'v':
            w = v + int(choice([-1, 1, 2, 3]))

        return gen, mark, mark_2, w, scan

    def yes_pass(self):
        if self.er == 'n':
            self.pass_.close()
            self.count += 1
            self.change('Вы: Следующий!')
            self.start_game(0)
        else:
            self.choice = 'n'
            self.start_game(1)

    def not_pass(self):
        if self.er == 'd':
            self.pass_.close()
            self.count += 1
            self.change('Вы: Следующий!')
            self.start_game(0)
        else:
            self.choice = 'd'
            self.start_game(1)

    def arrest_pass(self):
        if self.er == 'a':
            self.pass_.close()
            self.count += 1
            self.change('Вы: Следующий!')
            self.start_game(0)
        else:
            self.choice = 'a'
            self.start_game(1)

    def change(self, txt):
        self.txt = self.txt + '\n' + txt
        self.dialog.setText(self.txt)

    def clear(self):
        self.txt = ''
        self.textBrowser.setText(self.txt)


class Info(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('info.ui', self)
        self.txt = ''

    def change(self, txt):
        self.textBrowser.setText(txt)


class Passport(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('passport.ui', self)

    def change(self, face, name, gender, country, pechat, data, v):
        self.pas.setText(
            'PASSPORT\n{}\nФИО: {}\nПол: {}\nСтрана: {}\nПечать: {}\nДействительно до: {}\nВес: {}'.format(face, gender,
                                                                                                           name,
                                                                                                           country,
                                                                                                           pechat,
                                                                                                           data, v))


class Pass(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('pass.ui', self)

    def change(self, gender, country, pechat, data):
        self.pas.setText(
            'Разрешение на въезд\nФИО: {}\nСтрана: {}\nПечать: {}\nДействительно до: {}'.format(gender, country, pechat,
                                                                                                data))


class Weight(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('weight.ui', self)

    def change(self, gender, country, pechat, v):
        self.textBrowser.setText(
            'Весовая карта\nФИО: {}\nСтрана: {}\nПечать: {}\nВес: {}'.format(gender, country, pechat, v))


class Scanner(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('touch.ui', self)
        self.txt = 'Приложите палец'
        self.pushButton.clicked.connect(self.touch)

    def info(self, flag):
        if flag == 1:
            self.txt = 'Да'
        else:
            self.txt = 'Нет'

    def touch(self):
        self.pushButton.setText(self.txt)


app = QApplication(sys.argv)
ex = MainMenu()
ex.show()
sys.exit(app.exec_())
