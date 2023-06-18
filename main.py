import sqlite3
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QMessageBox
import avtoriz2_ui
import registrasia_ui
from clienti2_ui import Ui_clienti2_ui
from menu_ui import Ui_menu_ui
from sotrudniki2_ui import Ui_sotrudniki2_ui
from tariffPlan2_ui import Ui_tariffPlan2_ui
from uslugi_ui import Ui_uslugi_ui

# Подключаемся к базе данных
db = sqlite3.connect('kursovaia.db')
cursor = db.cursor()



class Registrasia(QtWidgets.QMainWindow, registrasia_ui.Ui_registrasia_ui):
    def __init__(self):
        super(Registrasia, self).__init__()
        self.setupUi(self)
        self.lineEdit_login.setPlaceholderText('Введите логин')
        self.lineEdit_parol.setPlaceholderText('Введите пароль')
        self.pushButton_zaregestr.pressed.connect(self.reg)
        self.pushButton_voiti.pressed.connect(self.login)

    def login(self):
        self.login_window = Login()
        self.login_window.show()
        self.hide()

    def reg(self):
        try:
            user_login = self.lineEdit_login.text()
            user_parol = self.lineEdit_parol.text()

            if len(user_login) == 0:
                return
            if len(user_parol) == 0:
                return
            cursor.execute(f'SELECT login FROM users WHERE login = "{user_login}" ')
            if cursor.fetchone() is None:
                cursor.execute(f'INSERT INTO users VALUES("{user_login}","{user_parol}")')
                self.label_pustoi.setText(f'Аккаунт {user_login} успешно зарегистрирован')
                db.commit()
            else:
                self.label_pustoi.setText('Такая запись уже существует')
        except Exception as e:
            self.label_pustoi.setText(f'Ошибка авторизации: {user_login}')

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.ui = avtoriz2_ui.Ui_avtoriz2_ui()
        self.ui.setupUi(self)
        self.ui.lineEdit_Login.setPlaceholderText('Введите логин')
        self.ui.lineEdit_Parol.setPlaceholderText('Введите пароль')
        self.ui.pushButton_vioti.clicked.connect(self.login)
        self.ui.pushButton_zaregestr.clicked.connect(self.reg)

    def reg(self):
        self.reg_window = Registrasia()
        self.reg_window.show()
        self.hide()

    def login(self):
        try:
            user_login = self.ui.lineEdit_Login.text()
            user_parol = self.ui.lineEdit_Parol.text()

            if len(user_login) == 0:
                return
            if len(user_parol) == 0:
                return

            cursor.execute(f'SELECT parol FROM users WHERE login = "{user_login}"')
            check_par = cursor.fetchall()

            cursor.execute(f'SELECT login FROM users WHERE login = "{user_login}"')
            check_login = cursor.fetchall()

            if check_par and check_login and check_par[0][0] == user_parol and check_login[0][0] == user_login:
                self.open_menu()
            else:
                self.ui.label_pustaia.setText(f'Неверный логин или пароль')
        except Exception as e:
            print(f'Ошибка при авторизации: {e}')
            self.ui.label_pustaia.setText(f'Ошибка при авторизации')

    def open_menu(self):
        self.menu_ui = Menu_ui()
        self.menu_ui.show()
        self.hide()


class Menu_ui(QtWidgets.QMainWindow, Ui_menu_ui):
    def __init__(self):
        super(Menu_ui, self).__init__()
        self.setupUi(self)
        self.pushButton_sotrudniki.clicked.connect(self.open_sotrudniki)
        self.pushButton_clienti.clicked.connect(self.open_clienti)
        self.pushButton_tariffPlan.clicked.connect(self.open_tariff_plan)
        self.pushButton_uslugi.clicked.connect(self.open_uslugi)
        self.pushButton_vihod.clicked.connect(self.exit_application)

    def open_sotrudniki(self):
        self.sotrudniki_window = Sotrudniki2_ui()
        self.sotrudniki_window.show()

    def open_clienti(self):
        self.clienti_window = Clienti2_ui()
        self.clienti_window.show()

    def open_tariff_plan(self):
        self.tariff_plan_window = TariffPlan2_ui()
        self.tariff_plan_window.show()

    def open_uslugi(self):
        self.uslugi_window = Uslugi_ui()
        self.uslugi_window.show()

    def exit_application(self):
        QApplication.quit()

class Clienti2_ui(QWidget, Ui_clienti2_ui):
    def __init__(self):
        super(Clienti2_ui, self).__init__()
        self.setupUi(self)
        self.pushButton_open.clicked.connect(self.open_clienti)
        self.pushButton_delete.clicked.connect(self.delete_clienti)
        self.pushButton_insert.clicked.connect(self.insert_clienti)
        self.conn = sqlite3.connect('kursovaia.db')
        self.update()

    def open_clienti(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM Subscriber")
            data = cur.fetchall()
            col_name = [i[0] for i in cur.description]
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)
            return

        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def update(self, query="SELECT * FROM Subscriber"):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            data = cur.fetchall()
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)
            return

        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def insert_clienti(self):  # кнопка добавить
        row = [
            self.lineEdit_Imia.text(),
            self.lineEdit_Familia.text(),
            self.lineEdit_Otchestvo.text(),
            self.lineEdit_id_abonenta.text(),
            self.lineEdit_id_sotr.text(),
            self.lineEdit_id_tariff.text(),
            self.lineEdit_telefon.text(),
            self.lineEdit_email.text(),
            self.lineEdit_id_usl.text()
            ]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Subscriber(first_name, surname, last_name, id_subscriber, id_employees, 
            id_tariff_plan, phone_number, email, id_additional_services)
                        values('{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}',
                        '{row[7]}','{row[8]}')""")

            self.conn.commit()
            cur.close()
        except Exception as r:
            print("Не смогли добавить запись:", r)
            return r

        self.update()




    def delete_clienti(self):
        id = self.lineEdit_delet1.text()
        conn = sqlite3.connect('kursovaia.db')
        c = conn.cursor()
        c.execute("DELETE FROM Subscriber WHERE id_subscriber=?", (id,))
        conn.commit()
        conn.close()
        self.update()





class TariffPlan2_ui (QWidget, Ui_tariffPlan2_ui):
    def __init__(self):
        super(TariffPlan2_ui, self).__init__()
        self.setupUi(self)
        self.pushButton_open.clicked.connect(self.open_tariffPlan)
        self.pushButton_insert.clicked.connect(self.insert_tariffPlan)
        self.pushButton_delete.clicked.connect(self.delete_tariffPlan)
        self.conn = sqlite3.connect('kursovaia.db')
        self.update()

    def open_tariffPlan(self):  # кнопка добавить
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM Tariff_Plan")
            data = cur.fetchall()
            col_name = [i[0] for i in cur.description]
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)
            return

        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()


    def update(self, query="SELECT * FROM Tariff_Plan"):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            data = cur.fetchall()
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)
            return

        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def insert_tariffPlan(self):  # кнопка добавить
        row = [
            self.lineEdit_id.text(),
            self.lineEdit_tariff.text(),
            self.lineEdit_stoimost.text(),
            self.lineEdit_minut.text(),
            self.lineEdit_internet.text()
            ]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Tariff_Plan(id_tariff_plan, name_tariff_plan, 'price(rub)', 'tariff_data(phone)', 
            'tariff_data(internet)')
                            values('{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}')""")
            self.conn.commit()
            cur.close()
        except Exception as r:
            print("Не смогли добавить запись:", r)
            return r
        self.update()  # обращаемся к update чтобы сразу увидеть изменения в БД



    def delete_tariffPlan(self):
        id = self.lineEdit_id_delete.text()
        conn = sqlite3.connect('kursovaia.db')
        c = conn.cursor()
        c.execute("DELETE FROM Tariff_Plan WHERE id_tariff_plan=?", (id,))
        conn.commit()
        conn.close()
        self.update()


class Sotrudniki2_ui(QWidget, Ui_sotrudniki2_ui):
    def __init__(self):
        super(Sotrudniki2_ui, self).__init__()
        self.setupUi(self)
        self.pushButton_open.clicked.connect(self.open_sotrudniki)
        self.pushButton_insert.clicked.connect(self.insert_sotrudniki)
        self.pushButton_delete.clicked.connect(self.delete_sotrudniki)
        self.conn = sqlite3.connect('kursovaia.db')
        self.update()

    def open_sotrudniki(self):  # кнопка добавить
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM Employees")
            data = cur.fetchall()
            col_name = [i[0] for i in cur.description]
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)
            return

        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def update(self, query="SELECT * FROM Employees"):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            data = cur.fetchall()
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)
            return

        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def insert_sotrudniki(self):  # кнопка добавить
        row = [
            self.lineEdit_id.text(),
            self.lineEdit_Imia.text(),
            self.lineEdit_Familia.text(),
            self.lineEdit_Otchestvo.text(),
            self.lineEdit_telefon.text(),
            self.lineEdit_email.text(),
            self.lineEdit_dolzhnost.text()
        ]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Employees(id_employees, first_name, surname, last_name, 
                 phone_number, email, post)
                 values('{row[0]}','{row[1]}','{row[2]}','{row[3]}','{row[4]}','{row[5]}','{row[6]}')""")

            self.conn.commit()
            cur.close()
        except Exception as r:
            print("Не смогли добавить запись:", r)
            return r
        self.update()

    def delete_sotrudniki(self):
        id = self.lineEdit_id_delete.text()
        conn = sqlite3.connect('kursovaia.db')
        c = conn.cursor()
        c.execute("DELETE FROM Employees WHERE id_employees=?", (id,))
        conn.commit()
        conn.close()
        self.update()




class Uslugi_ui(QWidget, Ui_uslugi_ui):
    def __init__(self):
        super(Uslugi_ui, self).__init__()
        self.setupUi(self)
        self.pushButton_open.clicked.connect(self.open_uslugi)
        self.pushButton_insert.clicked.connect(self.insert_uslugi)
        self.pushButton_delete.clicked.connect(self.delete_uslugi)
        self.conn = sqlite3.connect('kursovaia.db')
        self.update()

    def open_uslugi(self):  # кнопка добавить
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM Additional_Services")
            data = cur.fetchall()
            col_name = [i[0] for i in cur.description]
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)
            return

        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def update(self, query="SELECT * FROM Additional_Services"):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            data = cur.fetchall()
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)
            return

        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elen in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elen)))
        self.tableWidget.resizeColumnsToContents()

    def insert_uslugi(self):  # кнопка добавить
        row = [
            self.lineEdit_id_usl.text(),
            self.lineEdit_usluga.text(),
            self.lineEdit_stoimUsl.text(),
            self.lineEdit_id_opl.text()
        ]
        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into Additional_Services(id_additional_services, name_additional_services, price, 
                 id_payment_frequency)
                 values('{row[0]}','{row[1]}','{row[2]}','{row[3]}')""")

            self.conn.commit()
            cur.close()
        except Exception as r:
            print("Не смогли добавить запись:", r)
            return r
        self.update()  # обращаемся к update чтобы сразу увидеть изменения в БД



    def delete_uslugi(self):
        id = self.lineEdit_id.text()
        conn = sqlite3.connect('kursovaia.db')
        c = conn.cursor()
        c.execute("DELETE FROM Additional_Services WHERE id_additional_services=?", (id,))
        conn.commit()
        conn.close()
        self.update()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())




