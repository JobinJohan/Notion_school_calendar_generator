import os
import tkinter as tk
from tkinter import *
from typing import Callable
from config.config import *
from notion.notion_page import NotionPage
from jsoneditor.editor import JsonEditor
from ui.menu import MenuApp
import requests
from dotenv import load_dotenv

class AppUI():
    """Class that creates the main window of the app"""

    def __init__(self) -> None:
        # Create root window
        self.root = Tk()
        self.root.title(
            "Application de génération de calendrier Notion pour le Collège du Sud")
        self.window_width = 1080
        self.window_height = 720
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.configure(background='white')

        # Add window logo
        p1 = PhotoImage(file='./img/favicon_csud.png')
        self.root.iconphoto(False, p1)

        # Create the top menu
        self.menu = MenuApp(self)

        # Fonts
        self.font_title = ("Inter", 36)
        self.font_content = ("Inter", 16)

        # Color palettes
        self.blue = "#274599"
        self.white = "#ffffff"
        self.violet = "#6CsB7B"
        self.malllow = "#C06C84"
        self.red = "#F67280"
        self.orange = "#F8B195"

        # Buttons width
        self.button_width = 30

        # The window is split into two frames (TITLE - CONTENT) (20% - 80% of window height)
        self.title_frame = Frame(
            self.root, bg=self.blue, width=self.window_width, height=self.window_height*0.2)
        self.title_frame.pack(side=TOP)
        self.margin_bottom_title = 50

        # Config
        self.config = Config()

        # Content frame
        self.content_frame = Frame(
            self.root, bg=self.white, width=self.window_width, height=self.window_height*0.8)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side=TOP)
        self.display_content("landing_page")

        self.root.mainloop()

    def change_title(self, title: str) -> None:
        """Change the title of the frame
        :param title: str: title of the frame
        """
        self.title_label = Label(
            self.title_frame, text=title, bg=self.blue, font=self.font_title, fg=self.white)
        self.title_label.pack(ipady=(self.window_height*0.2)//2)
        self.title_frame.pack_propagate(False)

    def execute_and_redirect(self, function: Callable, *args) -> None:
        """Execute a function and redirect to another page
        :param function: Callable: function to execute
        :param page: str: page to redirect to
        """
        print("La longueur des arguments est de", len(args))
        print("ARGS0", args[0])


        if len(args) == 1:
            if function():
                self.display_content(args[0])
        else:
            print("ARGS1", args[1])
            if function(args[1]):
                self.display_content(args[0])       

    def display_content(self, page: str) -> None:
        """Display the content of the frame
        :param page: str: page to display
        """
        # Reset content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Reset title frame
        for widget in self.title_frame.winfo_children():
            widget.destroy()

        match page:
            case "landing_page":
                # Title
                self.change_title("Générateur de calendriers Notion")

                # Image
                imgpath = f"{os.getcwd()}/img/calendrier.png"
                img = tk.PhotoImage(file=imgpath)
                image_label = tk.Label(self.content_frame, image=img)
                image_label.pack(side=TOP, pady=75)
                image_label.image = img

                # Content
                left_button = Button(self.content_frame, text="Charger une configuration existante", bg=self.blue,
                                     font=self.font_content, command=self.menu.open_file, fg=self.white, width=self.button_width)
                right_button = Button(self.content_frame, text="Créer une configuration vide", bg=self.blue, font=self.font_content, fg=self.white,
                                      command=lambda: self.execute_and_redirect(self.config.init_config_from_empty_config, "json_editor"), width=self.button_width)
                left_button.place(x=145, y=(self.window_height*0.6))
                right_button.place(x=self.window_width-500,
                                   y=(self.window_height*0.6))

            case "json_editor":
                # Title
                self.change_title("Editeur de configuration")

                # Content
                # Add JSON editor
                editor = JsonEditor(self.content_frame, self.config)
                editor.pack(pady=self.margin_bottom_title)

                # Add buttons
                left_button = Button(self.content_frame, text="Revenir en arrière", bg=self.blue, font=self.font_content,
                                     command=lambda: self.display_content("landing_page"), fg=self.white, width=self.button_width)
                right_button = Button(self.content_frame, text="Suite", bg=self.blue, font=self.font_content,
                                      fg=self.white, command=lambda: self.display_content("notion_root_page"), width=self.button_width)
                left_button.place(x=145, y=(self.window_height*0.6))
                right_button.place(x=self.window_width-500,
                                   y=(self.window_height*0.6))

            case "notion_root_page":
                # Title
                self.change_title("Page Notion racine")

                # Content

                # Input field to get the Notion page root ID (max 36 chars)
                label = tk.Label(self.content_frame, text="Notion page ID:")
                label.grid(row=0, column=0, padx=10, pady=50, sticky="e")

                # Change label font size and font
                label.config(font=self.font_content)
                
                entry = tk.Entry(
                    self.content_frame,
                    bg="white",
                    fg=self.blue,
                    font=self.font_content,
                    bd=3
                )
                entry.grid(row=0, column=1, padx=10, pady=50)
                
                # Change width of the entry field
                entry.config(width=50)

                # If user presses enter, execute the function
                entry.bind("<Return>", lambda event: self.execute_and_redirect(NotionPage.check_if_root_page_is_valid, "generate_calendar", entry.get()))

                # Buttons
                left_button = Button(self.content_frame, text="Revenir en arrière", bg=self.blue, font=self.font_content,
                                     command=lambda: self.display_content("landing_page"), fg=self.white, width=self.button_width)
                right_button = Button(self.content_frame, text="Vérifier si la page Notion existe réellement", bg=self.blue, font=self.font_content,
                                      fg=self.white, command=lambda: self.execute_and_redirect(NotionPage.check_if_root_page_is_valid, "generate_calendar", entry.get()), width=self.button_width+10)
                left_button.grid(row=2, column=0, padx=10, pady=300)
                right_button.grid(row=2, column=1, padx=10, pady=300)

            case "generate_calendar":
                self.change_title("Génération du calendrier Notion")

                # Buttons
                left_button = Button(self.content_frame, text="Revenir en arrière", bg=self.blue, font=self.font_content,
                                     command=lambda: self.display_content("notion_root_page"), fg=self.white, width=self.button_width)
                right_button = Button(self.content_frame, text="Générer calendrier", bg=self.blue, font=self.font_content,
                                      fg=self.white, command=lambda: NotionPage.create_pages_from_config(self.config), width=self.button_width+10)
                left_button.grid(row=2, column=0, padx=10, pady=300)
                right_button.grid(row=2, column=1, padx=10, pady=300)


            case "a_propos":
                self.change_title("A propos")

            case _:
                self.display_content("landing_page")

    