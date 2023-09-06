import tkinter as tk
from tkinter import filedialog
import webbrowser
from config.config import *

class MenuApp():
    def __init__(self, app):
        self.app = app
        self.root = app.root

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.create_file_menu()

        # self.text = tk.Text(root)
        # self.text.pack()

    def create_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau", command=self.new_file)
        file_menu.add_command(label="Ouvrir", command=self.open_file)
        file_menu.add_command(label="Enregistrer", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.exit_app)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="A propos", command=self.a_propos)
        help_menu.add_command(label="Documentation de l'API Notion", command=self.notion_api_info)

    def new_file(self) -> None:
        self.text.delete("1.0", tk.END)

    def open_file(self)-> None:
        file_path = filedialog.askopenfilename()
        self.app.config= Config(file_path)
        if self.app.config.load_valid_config():
            print("Config valide")
        else:
            print("Config non valide")
        # if file_path:
        #     with open(file_path, "r") as file:
        #         content = file.read()

    def save_file(self)-> None:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                content = self.text.get("1.0", tk.END)
                file.write(content)

    def exit_app(self)-> None:
        self.root.destroy()

    def a_propos(self)-> None:
        self.app.reset_frame(self.app.title_frame)
        self.app.reset_frame(self.app.content_frame)
        self.app.change_title("A propos")
        
    def notion_api_info(self)-> None:
        url = "https://developers.notion.com/"
        webbrowser.open_new_tab(url)