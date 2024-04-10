import datetime
import json
import os
from pathlib import Path
from tkinter import messagebox
from typing import Dict
from jsonschema import validate
from config.config_schema import schema

class Config():
    """Class that handles the configuration of the calendar to generate"""
    
    # Current config
    config: Dict
    empty_config_file_name: str
    config_file_path: str

    def __init__(self) -> None:
        # Get the filename of the empty configuration file
        self.empty_config_file_name = "empty_config.json"

    def load_config_if_valid(self, path: str) -> bool:
        """Load a configuration file if it is valid
        :param path: str: path to the configuration file
        """

        # If the configuration file already exists, load it, else, create a new
        if os.path.isfile(path):
            # Try to load a configuration
            try:
                with open(path, 'r') as config_file:
                    self.config = json.load(config_file)
                    
                     # Check if the configuration matches the correct schema defined in config_schema.py
                    if not self.is_valid_config():
                        self.reset_config()
                        return False
                    
                    self.config_file_path = path

            except json.JSONDecodeError:
                messagebox.showerror("Erreur", "Le fichier sélectionné n'est pas un fichier .json valide")
                return False   
    
            return True

        else:
            self.reset_config()
            return False
    
        
    def init_config_from_empty_config(self) -> bool:
        """Initialize the configuration from an empty configuration file"""
        
        # Path to empty config file
        empty_config_file_path = os.path.join(os.getcwd(), "config", self.empty_config_file_name)

        # Check that the empty config file exists
        if os.path.isfile(empty_config_file_path):
            try:
                with open(empty_config_file_path, 'r') as config_file:
                    self.config = json.load(config_file)
            except json.JSONDecodeError:
                messagebox.showerror("Erreur", "Le fichier de configuration vide est introuvable")
                return False
            
            # Dictionnaries to add to empty config
            dates_dict = {
                "date_debut": "",
                "date_fin": "",
            }

            cours_info_dict = {
                "jour": "",
                "heure_debut": "",
                "heure_fin": "",
                "salle": ""
            }

            classe_info_dict = {
                "nb_eleves" : 0,
                "cours_1" : cours_info_dict.copy(),
                "cours_2" : cours_info_dict.copy(),
            }

            moodle_jupyterhub_dict = {
                "url_moodle": "",
                "url_jupyterhub": ""
            }

            # Add holidays to empty config
            for holiday in self.config['infos_generales']['vacances']:
                self.config['infos_generales']['vacances'][holiday] = dates_dict.copy()
            
            # Add public holidays to config
            for public_holiday in self.config['infos_generales']['jours_feries']:
                self.config['infos_generales']['jours_feries'][public_holiday] = dates_dict.copy()

            # Add moodle and jupyterhub url info as well as courses info for each class to config
            for level in self.config['niveaux']:
                for year in self.config['niveaux'][level]:
                    self.config['niveaux'][level][year]['infos_generales'] = moodle_jupyterhub_dict.copy()
                    for classe in self.config['niveaux'][level][year]['classes']:
                        self.config['niveaux'][level][year]['classes'][classe] = classe_info_dict.copy()    

            # Save config
            self.save_config_in_file()

            return True
        
        else:
            return False
        
    def save_config_in_file(self) -> None:
        """Save the current configuration in a file"""
    
        # Check if the file already exist and prevent overwriting it
        i = 0
        f_p = Path(f"config_{datetime.datetime.now().strftime('%Y_%m_%d')}_{i}.json")
        while f_p.exists():
            i += 1
            f_p = Path(f"config_{datetime.datetime.now().strftime('%Y_%m_%d')}_{i}.json")

        # Save file name as an attribute
        self.config_file_path = f"config_{datetime.datetime.now().strftime('%Y_%m_%d')}_{i}.json"

        # Write config into the file
        try:
            with open(self.config_file_path, "w", encoding="utf-8") as fichier:
                json.dump(self.config, fichier, indent=4)
        except Exception:
            print("Une erreur s'est produite lors de la sauvegarde de la configuration")

    def save_config_from_dict(self, dict) -> None:
        """Save the given dictionary into the configuration file
        :param dict: dict: dictionary to save into the configuration file
        """
        # Write the given dict into the config file
        try:
            with open(self.config_file_path, "w", encoding="utf-8") as fichier:
                json.dump(dict, fichier, indent=4)
        except Exception:
            print("Une erreur s'est produite lors de la sauvegarde de la configuration")

    def reset_config(self) -> None:
        """Reset the configuration to an empty state"""

        # Reset all attributes
        self.empty_config_file_name = ""
        self.config = {}
        self.config_file_path = ""
    
    def is_valid_config(self) -> bool:
        """Check if the current configuration is valid"""

        # Check that the config exists and is not null
        if self.config is not None:
            try:
                validate(self.config, schema=schema)
                return True
            except Exception as error:
                messagebox.showerror("Erreur", f"{error}")
                return False
        else:
            return False
