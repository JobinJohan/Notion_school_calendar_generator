from tkinter import ttk
import tkinter as tk
from jsoneditor.entrypopup import *
import pprint
from typing import Type
from typing import Callable
from typing import Dict


class JsonEditor:

    def __init__(self, window: tk.Frame, data: Dict):
        # Save config
        self.data = data

        # Create tree
        self.tree = ttk.Treeview(window, columns=("Column1"))
        self.tree.column("Column1", width=int(window.winfo_width()*0.5))
        self.tree.heading("Column1", text="Valeurs à compléter")
        self.tree.pack()

        # Add data into the tree and store a mapping between the keys and the item id
        # This is necessary to keep the data dictionary synchronized with the UI
        self.item_id_to_key_mapping = {}
        self.add_items_to_tree("", data, "")
        # pprint.pprint(self.key_to_item_id_mapping)
        self.expand_all()
        
        # Make the tree editable when the user double clicks
        self.tree.bind("<Double-1>", self.edit_value)
    

    def add_items_to_tree(self, parent_item: str, data: Dict, previous_key: str) -> None:
        # Go through the data that need to be stored into the tree
        for key, value in data.items():

            # If the value to be added is a dictionary, insert the key into the tree and repeat recursively
            if isinstance(value, dict):
                item = self.tree.insert(parent_item, 'end', text=key)

                if previous_key == "":
                    self.add_items_to_tree(item, value, f"{key}")
                else: 
                    self.add_items_to_tree(item, value, f"{previous_key}.{key}")
            else:
                item_id = self.tree.insert(parent_item, 'end', text=f"{key}:", values=(value,))
                if previous_key == "":    
                    self.item_id_to_key_mapping[item_id] = f"{key}"
                else:
                    self.item_id_to_key_mapping[item_id] = f"{previous_key}.{key}"
    


    def expand_all(self, item: str ="") -> None:
        # Get all children of a specific item ("" is the root item)
        children = self.tree.get_children(item)

        # Go through all children and expand each of them
        for child in children:
            self.tree.item(child, open=True)
            self.expand_all(child)


    def edit_value(self, event: tk.Event) -> None:
        # Get the number of row and column on which the user clicked on
        rowid = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        # If the element clicked by the user has at least one value associated (i.e. all tree leaves)
        if len(self.tree.item(rowid, "values")) >= 1:
            
            # Get column position info
            x, y, width, mheight = self.tree.bbox(rowid, column)

            # Create the entry popup   
            self.entryPopup = EntryPopup(self.tree, rowid, self.tree.item(rowid, "values")[0], self.data, self.item_id_to_key_mapping)
            
            # Place Entry popup properly      
            self.entryPopup.place(x=0, y=y, relwidth=1)