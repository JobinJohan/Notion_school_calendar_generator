from tkinter import *
from ui.menu import *
from typing import Type

class AppUI():
    
    def __init__(self) -> None:
        # Create root window
        self.root = Tk()
        self.root.title("Application de génération de calendrier Notion pour le Collège du Sud")
        self.window_width = 1080
        self.window_height = 720
        self.root.geometry(f"{self.window_width}x{self.window_height}")

        # Add window logo
        p1 = PhotoImage(file = './img/favicon_csud.png')
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

        # The window is split into two frames (TITLE - CONTENT) (20% - 80% of window height)
        self.title_frame = Frame(self.root, bg=self.blue, width=self.window_width, height=self.window_height*0.2)
        self.title_frame.pack(side=TOP)

        # Title label of the TITLE frame
        self.change_title("Générateur de calendriers Notion")

        # Content frame
        self.content_frame = Frame(self.root, bg=self.white, width=self.window_width, height=self.window_height*0.8)
        self.content_frame.pack(side=TOP)
        self.display_content("landing_page")

        # Config
        self.config = Config()

        self.root.mainloop()

    def reset_frame(self, frame: Type[Frame] ) -> None:
        for widget in frame.winfo_children():
            widget.destroy()
    
    def change_title(self, title: str) -> None:
        self.title_label = Label(self.title_frame, text=title, bg=self.blue, font=self.font_title, fg=self.white)
        self.title_label.pack(ipady=(self.window_height*0.2)//2)
        self.title_frame.pack_propagate(False)
    
    def display_content(self, page: str) -> None:
        # Reset content frame
        for widget in self.content_frame.winfo_children():
                    widget.destory()

        match page:
            case "landing_page":
                # Display two buttons:
                # Left button to load an existing configuration file
                # Right button to creating)
                left_button = Button(self.content_frame, text="Charger une configuration existante", bg=self.blue, font=self.font_content, command=self.menu.open_file, fg=self.white)
                right_button = Button(self.content_frame, text="Créer une configuration vide", bg=self.blue, font=self.font_content, fg=self.white)
                left_button.place(x=150, y=(self.window_height*0.8)//2)
                right_button.place(x=self.window_width-400, y=(self.window_height*0.8)//2)

            case "json_editor":
                pass
            case "calendar_creation":
                pass





    
    