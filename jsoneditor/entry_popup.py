from tkinter import ttk
import tkinter as tk
from typing import Dict

class EntryPopup(ttk.Entry):

    def __init__(self, parent: ttk.Treeview, iid: int, old_value: str, config, item_id_to_key_mapping: Dict) -> None:

        # App config
        self.config = config

        # Create the entry and add it to the tree
        super().__init__(parent)
        self.tv = parent
        self.iid = iid

        # Store the data used to create the tree (is used to keep the UI of the tree and the underlying data synchronized)
        self.tree_data = config.config
        self.item_id_to_key_mapping = item_id_to_key_mapping

        # The default text in the input field is the old value
        self.insert(0, old_value)

        # Set the focus in the input field
        self.focus_force()

        # Bind key event to functions
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *ignore: self.destroy())

    def on_return(self, event: tk.Event) -> None:
        # Update the tree at the correct position
        new_value = self.get()
        self.tv.set(self.iid, "Column1", new_value)

        # Update the tree data accordingly using the item id and the item_id_to_key_mapping dictionary
        full_paths = self.item_id_to_key_mapping[self.iid].split(".")
        current_data = self.tree_data

        for current_path in full_paths[:-1]:
            current_data = current_data[current_path]

        # Update the dictionary with the new value at the correct position
        current_data[full_paths[-1]] = new_value

        # Update the app config by saving the modification in the associated file
        self.config.save_config_from_dict(self.tree_data)

        # Destroy the entry
        self.destroy()

    def select_all(self, *ignore) -> None:
        self.selection_range(0, 'end')

        # returns 'break' to interrupt default key-bindings
        return 'break'