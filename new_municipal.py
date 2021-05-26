import tkinter as tk
from tkinter import Menu, mainloop, ttk
from tkinter import messagebox
import sqlite3
import time
import servise
import helper_sql as hs
import parse


class MainWindow(tk.Tk):
    """Main window class"""

    def __init__(self):
        super().__init__()
        self.title("Municipal Pay 1.1")
        self.geometry('580x620')
        self.minsize(1050, 620)
        self.create_frame_entry()
        self.create_frame_story()
        self.create_menu()

    def create_menu(self):
        """
        Вызываем метод config при содании меню
        Это метод главного класса 
        Принимает аргументом menu= КлассМеню(себя)
        Это аналог grid, pack, place в других виджетах
        """
        self.config(menu=MainMenu(self))

    def create_frame_entry(self):
        """Create frame with Entry field"""
        self.fr_entry = AddEntry()
        self.fr_entry.place(relx=0, rely=0, relwidth=1, relheight=0.5)

    def create_frame_story(self):
        """Create frame with info from database"""
        self.fr_story = AddStory()
        self.fr_story.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

    def run(self):
        """Подсчёт без сохранения"""
        self.fr_entry.water_diffrnt_entry.delete(0, 'end')
        self.fr_entry.water_price_entry.delete(0, 'end')
        self.fr_entry.elerctro_diffrnt_entry.delete(0, 'end')
        self.fr_entry.elerctro_price_entry.delete(0, 'end')
        w_n = self.fr_entry.water_now_entry.get()
        w_pr = self.fr_entry.water_prev_entry.get()
        el_n = self.fr_entry.elerctro_now_entry.get()
        el_pr = self.fr_entry.elerctro_prev_entry.get()
        try:
            dffrnt_water = int(w_n) - int(w_pr)
            self.fr_entry.water_diffrnt_entry.insert(0, dffrnt_water)
            water_prc = dffrnt_water*parse.take_tariff_water()
            self.fr_entry.water_price_entry.insert(0, round(water_prc, 1))

            dffrnt_electro = int(el_n) - int(el_pr)
            self.fr_entry.elerctro_diffrnt_entry.insert(0, dffrnt_electro)
            electro_prc = dffrnt_electro*parse.take_tariff_electro()
            self.fr_entry.elerctro_price_entry.insert(0, round(electro_prc, 1))
        except ValueError:
            messagebox.showinfo('Баран!', 'Нужно вводить целые числа!!!!')
            self.fr_entry.water_now_entry.delete(0, 'end')
            self.fr_entry.water_prev_entry.delete(0, 'end')
            self.fr_entry.elerctro_now_entry.delete(0, 'end')
            self.fr_entry.elerctro_prev_entry.delete(0, 'end')
            self.fr_entry.insert_previous_counter()

    def run_and_save(self):
        """Подсчёт с сохранением в БД"""
        self.run()
        paym = [
            (
                time.strftime('%B'),
                self.fr_entry.water_now_entry.get(),
                self.fr_entry.elerctro_now_entry.get(),
                self.fr_entry.water_price_entry.get(),
                self.fr_entry.elerctro_price_entry.get(),
            )
        ]
        hs.create_or_insert("MunicipalPaymant_v1.1", paym)
        self.fr_story.destroy()
        self.create_frame_story()

    def prnt(self):
        """Удаляет выделеную запись о данных за месяц"""
        try:
            ask = messagebox.askyesno(
                title="Внимание!", message="Удалить запись об этом месяце?")
            if ask:
                dct = self.fr_story.tablepay.item(
                    self.fr_story.tablepay.selection())
                hs.delete_data("MunicipalPaymant_v1.1", dct['values'][0])
                self.fr_story.destroy()
                self.create_frame_story()
            else:
                self.fr_story.destroy()
                self.create_frame_story()
        except IndexError:
            messagebox.showinfo('Внимание!', 'Не выбрана запись!')

    def show_lbl_info_month(self):
        """
        Создаёт метки: Месяц, показатели, оплата за выбранный месяц
        Не выводит их
        """
        self.new_lbl_m = tk.Label(
            self.fr_entry, text='Месяц:', bg='#eef3f8', font=('Comic Sans MS', 10))
        self.new_lbl_m.grid(row=2, column=3, padx=5, pady=3, sticky="w")
        self.new_lbl_w = tk.Label(
            self.fr_entry, text='Вода, показатели:', bg='#eef3f8', font=('Comic Sans MS', 10))
        self.new_lbl_w.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        self.new_lbl_el = tk.Label(
            self.fr_entry, text='Ел-во, показатели:', bg='#eef3f8', font=('Comic Sans MS', 10))
        self.new_lbl_el.grid(row=4, column=3, padx=5, pady=5, sticky="w")
        self.new_lbl_w_price = tk.Label(
            self.fr_entry, text='Вода, $$:', bg='#eef3f8', font=('Comic Sans MS', 10))
        self.new_lbl_w_price.grid(row=5, column=3, padx=5, pady=5, sticky="w")
        self.new_lbl_el_price = tk.Label(
            self.fr_entry, text='Електр-во, $$:', bg='#eef3f8', font=('Comic Sans MS', 10))
        self.new_lbl_el_price.grid(row=6, column=3, padx=5, pady=5, sticky="w")

    def show_month_info(self):
        """
        Возвращает данные о показателях и оплате за выбранный месяц
        Не отображает их
        """
        res = hs.choose_into_sqlite(
            "MunicipalPaymant_v1.1",
            servise.translate_month(self.fr_entry.combo_month)
        )
        for x in res:
            for y in x:
                self.month_info = tk.Label(
                    self.fr_entry, text=y, bg='#eef3f8', font=('Comic Sans MS', 10), anchor=tk.E, bd=6
                )
                self.month_info.grid(row=x.index(y)+2, column=4)

    def detail_info_month(self):
        """
        Отображает метки для выбранного месяца
        Выводит инфо об оплате и показателях за выбранный месяц
        """
        self.show_lbl_info_month()
        self.show_month_info()


class MainMenu(tk.Menu):
    """
    Создание класса меню
    для отображения навигационного меню приложения
    В конструкторе указывать главное окно(mainwindow) и вызывать конструктор род. класса
    """

    def __init__(self, mainwindow):
        super().__init__(mainwindow)
        # Сами списки навигационного меню
        menu_file = tk.Menu(self, tearoff=0)
        menu_file.add_command(label="Меню 1")
        menu_file.add_command(label="Меню 2")
        menu_file.add_command(label="Меню 3")

        settings_file = tk.Menu(self, tearoff=0)
        settings_file.add_command(label="Настройки 1")
        settings_file.add_command(label="Настройки 2")
        settings_file.add_command(label="Настройки 3")

        info_file = tk.Menu(self, tearoff=0)
        info_file.add_command(label="Инфо 1")
        info_file.add_command(label="Инфо 2")
        info_file.add_command(label="Инфо 3")

        # Указываем какие выпадющие списки настроек будут в меню
        self.add_cascade(label="Файл", menu=menu_file)
        self.add_cascade(label="Настройки", menu=settings_file)
        self.add_cascade(label="Инфо", menu=info_file)


class AddEntry(tk.Frame):
    """
    Frame whith Entry and Label fields
    And two Buttons
    """

    def __init__(self):
        super().__init__()
        self['background'] = '#eef3f8'
        self.create_widget()
        self.insert_previous_counter()

    def create_widget(self):
        self.new_lbl_1 = tk.Label(
            self, text='Вода предыдущие:', bg='#eef3f8', font=('Comic Sans MS', 10), bd=3)
        self.new_lbl_1.grid(row=0, column=0, padx=10, pady=3)
        self.new_lbl = tk.Label(
            self, text='Вода поточные:', bg='#eef3f8', font=('Comic Sans MS', 10), bd=3)
        self.new_lbl.grid(row=2, column=0, padx=10, pady=3)
        self.new_lbl = tk.Label(
            self, text='Вода разница:', bg='#eef3f8', font=('Comic Sans MS', 10), bd=3)
        self.new_lbl.grid(row=4, column=0, padx=10, pady=3)
        self.new_lbl = tk.Label(
            self, text='Вода сумма, $$:', bg='#eef3f8', font=('Comic Sans MS', 10), bd=3)
        self.new_lbl.grid(row=6, column=0, padx=10, pady=3)
        self.new_lbl = tk.Label(
            self, text='Выбор месяца:', bg='#eef3f8', font=('Comic Sans MS', 10))
        self.new_lbl.grid(row=0, column=3, padx=10, pady=3)

        self.new_lbl = tk.Label(
            self, text='Електр-во предыдущие:', bg='#eef3f8', font=('Comic Sans MS', 10), bd=3)
        self.new_lbl.grid(row=0, column=1, padx=10, pady=3)
        self.new_lbl = tk.Label(
            self, text='Електр-во поточные:', bg='#eef3f8', font=('Comic Sans MS', 10), bd=3)
        self.new_lbl.grid(row=2, column=1, padx=10, pady=3)
        self.new_lbl = tk.Label(
            self, text='Електр-во разница:', bg='#eef3f8', font=('Comic Sans MS', 10), bd=3)
        self.new_lbl.grid(row=4, column=1, padx=10, pady=3)
        self.new_lbl = tk.Label(
            self, text='Електр-во сумма, $$:', bg='#eef3f8', font=('Comic Sans MS', 10), bd=3)
        self.new_lbl.grid(row=6, column=1, padx=10, pady=3)

        self.water_prev_entry = tk.Entry(self, font=(
            'Arial', 14), justify=tk.CENTER, width=25)
        self.water_prev_entry.grid(row=1, column=0, padx=5, pady=5)
        self.water_now_entry = tk.Entry(self, font=(
            'Arial', 14), justify=tk.CENTER, width=25)
        self.water_now_entry.grid(row=3, column=0, padx=5, pady=5)
        self.water_diffrnt_entry = tk.Entry(
            self, font=('Arial', 14), justify=tk.CENTER, width=25)
        self.water_diffrnt_entry.grid(row=5, column=0, padx=5, pady=5)
        self.water_price_entry = tk.Entry(self, font=(
            'Arial', 14), justify=tk.CENTER, width=25)
        self.water_price_entry.grid(row=7, column=0, padx=5, pady=5)

        self.elerctro_prev_entry = tk.Entry(
            self, font=('Arial', 14), justify=tk.CENTER, width=25)
        self.elerctro_prev_entry.grid(row=1, column=1, padx=5, pady=5)
        self.elerctro_now_entry = tk.Entry(self, font=(
            'Arial', 14), justify=tk.CENTER, width=25)
        self.elerctro_now_entry.grid(row=3, column=1, padx=5, pady=5)
        self.elerctro_diffrnt_entry = tk.Entry(
            self, font=('Arial', 14), justify=tk.CENTER, width=25)
        self.elerctro_diffrnt_entry.grid(row=5, column=1, padx=5, pady=5)
        self.elerctro_price_entry = tk.Entry(
            self, font=('Arial', 14), justify=tk.CENTER, width=25)
        self.elerctro_price_entry.grid(row=7, column=1, padx=5, pady=5)
        self.combo_month = ttk.Combobox(self, values=servise.month_all_foo())
        self.combo_month.grid(row=1, column=3, padx=10, pady=5)
        self.not_save_bttn = tk.Button(self, text='Подсчитать без сохранения', command=self.master.run, font=(
            'Comic Sans MS', 8), justify=tk.LEFT, foreground='navy')
        self.not_save_bttn.grid(row=8, column=0, padx=5, pady=5, sticky="e")
        self.save_bttn = tk.Button(self, text='Подсчитать&Сохранить', command=self.master.run_and_save, font=(
            'Comic Sans MS', 8), justify=tk.LEFT, foreground='navy')
        self.save_bttn.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        self.show_bttn = tk.Button(self, text='Найти', command=self.master.detail_info_month, font=(
            'Comic Sans MS', 8), foreground='#0ab1f7')
        self.show_bttn.grid(row=1, column=4, padx=5, pady=5)

    def insert_previous_counter(self):
        """Устанавливает предыдущие показатели с последнего месяца"""
        last_note = hs.choose_last_into_sqlite("MunicipalPaymant_v1.1")
        self.water_prev_entry.insert(0, int(last_note[0][1]))
        self.elerctro_prev_entry.insert(0, int(last_note[0][2]))


class AddStory(tk.Frame):
    """Show info from database"""

    def __init__(self):
        super().__init__()
        self['background'] = '#c6f7f7'
        self.my_name_header = [
            'Месяц', 'Показатели воды', 'Показатели електр-во', 'Цена за воду', 'Цена за електр-во'
        ]
        self.create_widget()

    def set_column(self):
        try:
            for x in hs.salect_all("MunicipalPaymant_v1.1"):
                self.tablepay.insert('', 'end', values=x)
            for x in self.my_name_header:
                self.tablepay.heading(x, text=x, anchor=tk.CENTER)
                self.tablepay.column(x, anchor=tk.CENTER)
        except sqlite3.OperationalError:
            for x in self.my_name_header:
                self.tablepay.heading(x, text=x, anchor=tk.CENTER)
                self.tablepay.column(x, anchor=tk.CENTER)

    def create_widget(self):
        self.tablepay = ttk.Treeview(self, show='headings')
        self.tablepay['columns'] = self.my_name_header
        self.tablepay['displaycolumns'] = self.my_name_header
        self.set_column()
        self.scrl = ttk.Scrollbar(self, command=self.tablepay.yview)
        self.scrl.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.tablepay.pack(expand=tk.YES, fill=tk.BOTH)
        self.show_bttn = tk.Button(self, text='Удалить запись', command=self.master.prnt, font=(
            'Comic Sans MS', 8), foreground='red')
        self.show_bttn.pack(fill=tk.BOTH)


winow = MainWindow()
winow.mainloop()
