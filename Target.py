import tkinter as tk
import os
import sqlite3
import time
import webbrowser
import pandas as pd
from datetime import date
from tkinter import ttk
from tkinter import *
from tkinter import Menu
from tkinter import messagebox as mb


#Window
window = Tk()
window.title("Таргет")
window.geometry("320x420+500+500")
window.resizable(width=False, height=False)
window.iconbitmap(r"logo.ico")


#Block
frame_add_data = tk.Frame(window, width = 320, height = 150)
frame_add_statistics = tk.Frame(window, width = 320, height = 250)


frame_add_data.pack()
frame_add_data.place(x = 0, y = 0)
frame_add_statistics.pack()
frame_add_statistics.place(x = 0, y = 150)


#Гиперссылка
def callback(url):
    webbrowser.open_new(url)


#Кнопки
def show_info():
    msg = "Ця програма допомагає підраховувати новий таргет і була зроблена для ***"
    mb.showinfo("Info", msg)


#Refresh
def refresh():
    window.destroy()
    os.popen("target.py")


#Refresh
def refresh_bind(event):
    window.destroy()
    os.popen("target.py")


#exit
def exit_plik():
	window.destroy()


#Блокирование экрана
def block():
    window.attributes("-topmost", True)


#Разблокировка экрана
def unlock():
    window.attributes("-topmost", False)


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


#Добавление
def from_submit():
    SN = sn_rite.get()
    Action = action_box.get()
    Punct = punct_box.get()
    insert_target = (SN, Action, Punct)
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = """ INSERT INTO targets(SN, Action, Punct) 
                                        VALUES (?, ?, ?); """
        cursor.execute(query, insert_target)
        db.commit()

    window.destroy()
    os.popen("target.py")


#Excport
def export():
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        query = """ SELECT * FROM targets """
        cursor.execute(query)

    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(list(data), columns=columns)

    writer = pd.ExcelWriter('Export/Targets.xlsx')
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

    writer = pd.ExcelWriter('Export/Targets.xlsx')
    df.to_excel(writer, sheet_name='bar')
    writer.save()


    msg = "Файл було успішно експортовано до папки Export яка знаходиться в корені програми."
    mb.showinfo("Експорт данних", msg)


#Флажки
r_var = BooleanVar()
r_var.set(0)


#Меню сверху
menu = Menu(window)
new_info = Menu(menu, tearoff = 0)
new_info.add_command(label = 'Info', command = show_info)
new_info.add_separator()
new_info.add_command(label = 'Refresh', command = refresh)
window.bind('<F5>', refresh_bind)
new_info.add_command(label = 'Clear', command = delete_target)
new_info.add_separator()
new_info.add_command(label = 'Export', command = export)
window.bind('<F1>', export_bind)
new_info.add_separator()
new_info.add_command(label = "Exit", command = exit_plik)
menu.add_cascade(label = 'File', menu = new_info)


new_comand = Menu(menu, tearoff = 0)
new_comand.add_command(label ='F5                              Refresh')
new_comand.add_command(label = 'F1                              Export')
new_comand.add_command(label = 'Alt + F4                    Exit')
menu.add_cascade(label = 'Commands', menu = new_comand)
window.config(menu = menu)


new_window = Menu(menu, tearoff=0)
block_men = Menu(menu, tearoff=0)
block_men.add_radiobutton(label = "Lock", variable = r_var, value = 1, command = block)
block_men.add_radiobutton(label = 'Unlock', variable = r_var, value = 0, command = unlock)
new_window.add_cascade(label = 'Заблокувати екран', menu = block_men)
menu.add_cascade(label = 'Window', menu = new_window)
window.config(menu = menu)


#Data
sn = Label(frame_add_data, text = 'SN:', font = ("Sylfaen", 10))
sn.pack()
sn.place(x = 10, y = 10)
sn_rite = Entry(frame_add_data, validate = 'key', font = ("Sylfaen", 9))
sn_rite.pack()
sn_rite.place(x = 60, y = 13)


action = Label(frame_add_data, text = "Action:", font = ("Sylfaen", 10))
action.pack()
action.place(x = 10, y = 40)
action_box = ttk.Combobox(frame_add_data, state="readonly", values=[ "REPAIR",
												"NFF", 
												"BGAPR", 
												"BER1", 
												"HOLD"],
												font = ("Sylfaen", 9))
action_box.pack()
action_box.place(x = 60, y = 43)


punct = Label(frame_add_data, text = 'Punct', font = ("Sylfaen", 10))
punct.pack()
punct.place(x = 10, y = 70)
punct_box = ttk.Combobox(frame_add_data, state = "readonly", values = ['0.5',
                                                                        '1'],
                                                                        font = ("Sylfaen", 9))
punct_box.pack()
punct_box.place(x = 60, y = 73)


add_but = Button(frame_add_data, text = 'Записати', font = ("Sylfaen", 10), command = from_submit)
add_but.pack()
add_but.place(x = 10, y = 110)


#Times
def timing():
    current_time = time.strftime("%H : %M : %S")
    clock.config(text = current_time)
    clock.after(200, timing)

clock=Label(frame_add_data,font=("Sylfaen",16,"bold"))
clock.place(x = 200, y = 6)
timing()


#Data 
current_date = date.today().strftime("%d.%m.%Y")
lbl = Label(frame_add_data, text= current_date, font = ("Sylfaen", 10, "bold"))
lbl.pack()
lbl.place(x = 237, y = 30)


#Table
class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)
  
        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings
  
        for head in headings:
            table.heading(head, text=head, anchor = 'w')
            table.column(head, anchor= 'w', width = 75, stretch = False)
            table.column('ID', width = 20)
            table.column('SN', width = 125)            
  
        for row in rows:
            table.insert('', tk.END, values=tuple(row))
  
        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


data = ()
with sqlite3.connect('db/database.db') as db:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM targets")
    data = (row for row in cursor.fetchall())


table = Table(frame_add_statistics, headings=('ID', 'SN', 'Action', 'Punct'), rows=data)
table.pack(expand=tk.YES, fill=tk.BOTH)


#Подпись
lbl = Label(window, text="by Dmytro Slobodian", font=("Sylfaen", 8))
lbl.pack()
lbl.bind("<Button-1>", lambda e: callback("mailto:dmytro.slobodian@reconext.com"))
lbl.place(x=0, y=378)


lbl = Label(window, text="form Debug | Repair", font=("Sylfaen", 8))
lbl.pack()
lbl.bind("<Button-1>", lambda e: callback("https://www.reconext.com/"))
lbl.place(x=210, y=378)


window.mainloop()