import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    """ Main window.
        This class create toolbar and sticks it on the top of window.
    """
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        """ This function stores and initializes all GUI objects.
            toolbar:
                bg - background color;
                bd - border thickness;
            btn_open_dialog:
                text - name of button;
                command - what will do this button;
                bg - background color;
                bd - border thickness;
                compound - where button will be;
                image - image =)
        """
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='calendar.png')
        btn_open_dialog = tk.Button(toolbar, text='Add event', command=self.open_dialog, bg='#d7d8e0', bd=3,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'date', 'time', 'direction', 'event'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('date', width=60, anchor=tk.CENTER)
        self.tree.column('time', width=60, anchor=tk.CENTER)
        self.tree.column('direction', width=80, anchor=tk.CENTER)
        self.tree.column('event', width=420, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('date', text='Date')
        self.tree.heading('time', text='Time')
        self.tree.heading('direction', text='Direction')
        self.tree.heading('event', text='Event')

        self.tree.pack()

    def records(self, date, time, direction, event):
        """ Intermediate function that calls insert_data() and view_records()"""
        self.db.insert_data(date, time, direction, event)
        self.view_records()

    def view_records(self):
        """Displays information from the database in the main program window"""
        self.db.c.execute('''SELECT * FROM my_events''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        """ Child window call
        """
        Child()

class Child(tk.Toplevel):
    """ Child window inherits from top-level window
    """
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        """ This function stores and initializes all GUI objects.
        """
        self.title('Add event')
        self.geometry('400x200+400+300')
        self.resizable(False, False)

        label_date = tk.Label(self, text='Date:')
        label_date.place(x=15, y=15)
        label_time = tk.Label(self, text='Time:')
        label_time.place(x=15, y=45)
        label_direction = tk.Label(self, text='Direction:')
        label_direction.place(x=15, y=75)
        label_event = tk.Label(self, text='Event:')
        label_event.place(x=15, y=105)

        self.entry_date = ttk.Entry(self)
        self.entry_date.place(x=100, y=15)

        self.entry_time = ttk.Entry(self)
        self.entry_time.place(x=100, y=45)

        self.combobox = ttk.Combobox(self, values=[u'Python', u'JavaScript', u'HTML/CSS', u'C, C++, C#', u'Java',
                                                   u'Other'])
        self.combobox.current(0)
        self.combobox.place(x=100, y=75)

        self.entry_event = ttk.Entry(self, width=45)
        self.entry_event.place(x=100, y=105)

        btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=300, y=160)
        btn_ok = ttk.Button(self, text='Add')
        btn_ok.place(x=210, y=160)
        btn_ok.bind('<Button-1>', lambda happening: self.view.records(self.entry_date.get(),
                                                                      self.entry_time.get(),
                                                                      self.combobox.get(),
                                                                      self.entry_event.get()))

        self.grab_set()
        self.focus_set()

class DB:
    """ DB - Data base
        This class will connects the database with the specified name, or creates, if it does not exist.
    """
    def __init__(self):
        self.connection = sqlite3.connect('my_events.db')
        self.c = self.connection.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS my_events\
            (id integer primary key, date blob, time blob, direction text, event text)''')
        self.connection.commit()

    def insert_data(self, date, time, direction, event):
        """ This function receives values and saves them in the corresponding fields of the database"""
        self.c.execute('''INSERT INTO my_events(date, time, direction, event) VALUES(?, ?, ?, ?)''',
                       (date, time, direction, event))
        self.connection.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('My Reminder')
    root.geometry('650x450+300+200')
    root.resizable(False, False)
    root.mainloop()