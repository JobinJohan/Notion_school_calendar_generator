from typing import Dict
import json
import datetime
import os
from tkinter import messagebox
from jsonschema import validate
from config.config_schema import schema


class Config():

    # Current config
    config: Dict
    config_path: str

    # File that contains the empty configuration
    empty_config_file_name: str

    def __init__(self, config_path: str = f"config_{datetime.datetime.now().strftime('%Y_%m_%d')}.json", empty_config_file_name: str = "empty_config.json") -> None:

        # Get the filename of the empty configuration file
        self.empty_config_file_name = empty_config_file_name

        # Save the config path
        self.config_path = config_path


    def load_valid_config(self) -> bool:

        # If the configuration file already exists, load it, else, create a new
        if os.path.isfile(self.config_path):
            to_load = self.config_path
        else:
            to_load = self.empty_config_file_name

        # Try to load a configuration
        try:
            with open(to_load, 'r') as config_file:
                self.config = json.load(config_file)
            
        except json.JSONDecodeError:
            self.reset_config()
            messagebox.showerror("Erreur", "Le fichier sélectionné n'est pas un fichier de configuration .json valide")
            return False
        
        # Check if the configuration matches the correct schema defined in config_schema.py
        if not self.is_valid_config():
            self.reset_config()
            return False
        else:
            return True
        

    def save_config(self) -> None:
        try:
            with open(self.config_path, "w") as fichier:
                json.dump(self.config, fichier)
        except Exception:
            print("Une erreur s'est produite lors de la sauvegarde de la configuration")


    def reset_config(self) -> None:
        self.empty_config_file_name = ""
        self.config_path = ""
        self.config = {}
    
    def is_valid_config(self) -> bool:
        if self.config is not None:
            try:
                validate(self.config, schema=schema)
                return True
            except Exception as e:
                messagebox.showerror("Erreur", f"{e}")
                return False
        else:
            return False


    def edit_info_for_a_specific_class(self, classe_name: str) -> None:
        pass

    def reset_info_for_a_specific_class(self, class_name: str) -> None:
        pass

    def edit_general_info(self, info: str) -> None:
        pass

    def add_holiday(self, holiday_name: str) -> None:
        pass

    def edit_holiday(self, holiday_name: str) -> None:
        pass
