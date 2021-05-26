from tkinter import messagebox


def month_all_foo():
    """Return list month for Combobox"""
    all_month = [
        'Январь', 'Февраль', 'Март', 'Апрель',
        'Май', 'Июнь', 'Июль', 'Август',
        'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]
    return all_month


def translate_month(widg):
    """
    В качестве аргумента передать обьект Combobox
    Функция переводит название месяцев с русск. на англ. язык
    """
    all_month_dict = {
        'Январь': 'January', 'Февраль': 'February', 'Март': 'March', 'Апрель': 'April',
        'Май': 'May', 'Июнь': 'June', 'Июль': 'July', 'Август': 'August',
        'Сентябрь': 'September', 'Октябрь': 'October', 'Ноябрь': 'November', 'Декабрь': 'December'
    }
    try:
        month = widg.get()
        return all_month_dict[month]
    except KeyError:
        messagebox.showinfo('Исключение!', 'Не выбран месяц!')
