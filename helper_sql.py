import sqlite3
import servise
from tkinter import messagebox


def create_or_insert(name_db, col_list):
    """
    Создаёт БД, если её нет
    Добавляет запись в БД, если таблица уже существует
    Первый аргумент это имя БД
    Второй аргумент это список данных для сохранения в БД
    Порядок в списке должен строго соответствовать:
    месяц, показ-ли воды, показ-ли електро, цена за воду, цена за електро
    """
    try:
        with sqlite3.connect(f"{name_db}.sqlite") as mdb:
            cursor = mdb.cursor()
            cursor.execute(
                """CREATE TABLE municipal (
                    month text, now_water text, now_electro text, price_water text, price_electro text,
                    PRIMARY KEY (month)
                    )
                """
            )
            cursor.executemany(
                """INSERT INTO municipal VALUES (?, ?, ?, ?, ?)""", col_list)
    except sqlite3.OperationalError:
        try:
            with sqlite3.connect(f"{name_db}.sqlite") as mdb:
                cursor = mdb.cursor()
                cursor.executemany(
                    """INSERT INTO municipal VALUES (?, ?, ?, ?, ?)""", col_list)
        except sqlite3.IntegrityError:
            messagebox.showinfo(
                'Исключение!', 'Запись на данный месяц уже существует!')
    mdb.commit()


def salect_all(name_db):
    """
    Вносит данные в БД
    Имя БД указываем в аргументе функции
    Возвращает записи в БД
    """
    with sqlite3.connect(f"{name_db}.sqlite") as mdb:
        cursor = mdb.cursor()
        query = """SELECT * FROM municipal"""
        cursor.execute(query)
        return cursor.fetchall()
    mdb.commit()


def choose_into_sqlite(name_db, result):
    """
    Выбирает данные из БД
    Принимает имя БД, в качестве аргумента
    И название месяца для вибора записи из БД
    """

    with sqlite3.connect(f"{name_db}.sqlite") as mdb:
        cursor = mdb.cursor()
        sq = """SELECT * FROM municipal WHERE month=?"""
        cursor.execute(sq, [(result)])
        return cursor.fetchall()
    mdb.commit()


def choose_last_into_sqlite(name_db):
    """
    Выбирает последнюю запись из БД
    Принимает имя БД, в качестве аргумента
    """

    with sqlite3.connect(f"{name_db}.sqlite") as mdb:
        cursor = mdb.cursor()
        sq = """SELECT * FROM municipal ORDER BY rowid DESC LIMIT 1"""
        cursor.execute(sq)
        return cursor.fetchall()
    mdb.commit()


def delete_data(name_db, month_specific):
    """
    Удаляет выбранную запись из БД
    Принимает имя БД, в качестве аргумента и месяц по которому нужно удалить запись
    """
    with sqlite3.connect(f"{name_db}.sqlite") as mdb:
        cursor = mdb.cursor()
        sq = """DELETE FROM municipal WHERE month=?"""
        cursor.execute(sq, [(month_specific)])
    mdb.commit()
