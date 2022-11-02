import tkinter as tk
import json
import os
from db import DBManager
from tkinter import ttk, filedialog


def load_db_paths():
    if os.path.exists('db_paths.json'):
        json_data = json.load(open('db_paths.json'))
    else:
        path = os.path.expanduser('db_paths.json')
        json_data = {'dbs': []}
        json.dump(json_data, open(path, "w+"))
    return json_data


def add_db_path(db_name, path=os.path.abspath(os.getcwd())):
    if os.path.exists('db_paths.json'):
        json_data = json.load(open('db_paths.json'))
        json_data['dbs'].append(
            {
                'name': db_name,
                'path': os.path.join(path, (db_name + '.json'))
            }
        )
        config_path = os.path.expanduser('db_paths.json')
        json.dump(json_data, open(config_path, "w+"))
    else:
        json_data = {
            'dbs': [
                {
                    'name': db_name,
                    'path': os.path.join(path, (db_name + '.json'))
                }
            ]
        }
        config_path = os.path.expanduser('db_paths.json')
        json.dump(json_data, open(config_path, "w+"))


class CreateWindow:
    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        options = {'padx': 5, 'pady': 5}

        self.label = ttk.Label(top, text="Entry database name")
        self.label.pack(**options)

        self.name_entry = ttk.Entry(top)
        self.name_entry.pack(**options)

        self.label = ttk.Label(top, text="Browse database location")
        self.label.pack(**options)

        self.browse_button = ttk.Button(top, text='Browse')
        self.browse_button['command'] = self.get_path
        self.browse_button.pack(**options)

        self.button = ttk.Button(top, text='Ok', command=self.cleanup)
        self.button.pack(**options)

    def cleanup(self):
        self.name_value = self.name_entry.get()
        try:
            self.path_value = self.path_entry
        except AttributeError:
            self.path_value = os.getcwd()
        self.top.destroy()

    def get_path(self):
        self.path_entry = filedialog.askdirectory()


class LoadWindow:
    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        options = {'padx': 5, 'pady': 5}

        self.label = ttk.Label(top, text="Choose database")
        self.label.pack(**options)

        self.paths = (load_db_paths())['dbs']
        names = tk.Variable(value=[i['name'] for i in self.paths])
        self.dbs_listbox = tk.Listbox(top, listvariable=names)
        self.dbs_listbox.pack(**options)

        self.open_button = ttk.Button(
            top,
            text='Open selected',
            command=self.cleanup
        )
        self.open_button.pack(**options)

    def cleanup(self):
        self.selected_db = self.paths[
            self.dbs_listbox.curselection()[0]
        ]
        self.top.destroy()


class App(tk.Tk):

    def __init__(self, db, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.db = db
        self.tool = container

        self.frames = {}
        for F in [StartPage]:
            page_name = F.__name__
            frame = F(parent=container, container=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def create_frame(self, page_class):
        page_name = page_class.__name__
        frame = page_class(parent=self.tool, container=self)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")


class StartPage(tk.Frame):

    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.db = db
        self.container = container

        self.create_button = ttk.Button(self, text='Create db')
        self.create_button['command'] = self.create_db
        self.create_button.place(x=330, y=200)

        self.load_button = ttk.Button(self, text='Load db')
        self.load_button['command'] = self.load_dbs
        self.load_button.place(x=330, y=235)

        self.pack()

    def create_db(self):
        self.create_window = CreateWindow(self.container)
        self.create_button["state"] = "disabled"
        self.container.wait_window(self.create_window.top)
        self.create_button["state"] = "normal"

        try:
            db_name = self.create_window.name_value
            path = self.create_window.path_value
            self.db.create_db(db_name, path)
        except AttributeError:
            pass
        add_db_path(db_name, path)

    def load_dbs(self):
        self.load_window = LoadWindow(self.container)
        self.load_button["state"] = "disabled"
        self.container.wait_window(self.load_window.top)
        self.load_button["state"] = "normal"

        path = self.load_window.selected_db['path']
        self.db.load_db(path)

        self.container.create_frame(DBPage)
        self.container.show_frame('DBPage')


class DBPage(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.container = container
        self.db = db
        self.tables = self.db.get_tables()

        tables = [table.table_name for table in self.tables]
        tables = tk.Variable(value=tables)
        self.dbs_listbox = tk.Listbox(listvariable=tables)
        self.dbs_listbox.bind("<<ListboxSelect>>", self.load_rows)
        self.dbs_listbox.place(x=20, y=50)

    def load_rows(self, event):
        selection = event.widget.curselection()
        if selection:
            table = self.tables[selection[0]]
            print(table.rows)
            print([i.column_name for i in table.columns])


if __name__ == "__main__":
    db = DBManager()
    app = App(db)
    app.title('My Awesome DBMS')
    app.geometry("720x500")
    app.mainloop()
