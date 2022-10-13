import webbrowser
import sqlite3
import pandas as pd
import time
from tkinter import messagebox as mb



def callback(url):
    webbrowser.open_new(url)


#Кнопки
def show_info():
    msg = "Ця програма допомагає підраховувати новий таргет і була зроблена для техніків з відділу Debug/Repair"
    mb.showinfo("Info", msg)


#Clear
def delete_target():
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = """ DELETE FROM targets """
        query1 = """ DELETE FROM sqlite_sequence """
        cursor.execute(query)
        cursor.execute(query1)
        db.commit()

    window.destroy()
    os.popen("target.py")
    
    msg = "Всі дані були успішно видалені."
    mb.showinfo("Очистка данних", msg)


#Excport
def export():
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = """ SELECT * FROM targets """
        cursor.execute(query)

    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(list(data), columns=columns)

    date_string = time.strftime("%Y-%m-%d")
    writer = pd.ExcelWriter('Export/Targets-' + date_string + '.xlsx')
    df.to_excel(writer, sheet_name='bar')
    writer.save()


    msg = "Файл було успішно експортовано до папки Export яка знаходиться в корені програми."
    mb.showinfo("Експорт данних", msg)


def export_bind(event):
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = """ SELECT * FROM targets """
        cursor.execute(query)

    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(list(data), columns=columns)

    date_string = time.strftime("%d.%m.%Y")
    writer = pd.ExcelWriter('Export/Targets ' + date_string + '.xlsx')
    df.to_excel(writer, sheet_name='bar')
    writer.save()


    msg = "Файл було успішно експортовано до папки Export яка знаходиться в корені програми."
    mb.showinfo("Експорт данних", msg)


with sqlite3.connect('db/database.db') as db:
    cursor = db.cursor()
    query = """ SELECT SUM(Punct) FROM targets """
    cursor.execute(query)
    target_stat = cursor.fetchone()