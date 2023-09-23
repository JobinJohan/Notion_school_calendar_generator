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
    empty_config_file_name: str

    def __init__(self) -> None:

        # Get the filename of the empty configuration file
        self.empty_config_file_name = "empty_config.json"


    def load_config_if_valid(self, path: str) -> bool:

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

            except json.JSONDecodeError:
                messagebox.showerror("Erreur", "Le fichier sélectionné n'est pas un fichier .json valide")
                return False   
    
            return True

        else:
            self.reset_config()
            return False
    
        
    def init_config_from_empty_config(self) -> bool:

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
        try:
            with open(f"config_{datetime.datetime.now().strftime('%Y_%m_%d')}.json", "w") as fichier:
                json.dump(self.config, fichier, indent=4)
        except Exception:
            print("Une erreur s'est produite lors de la sauvegarde de la configuration")


    def reset_config(self) -> None:
        self.empty_config_file_name = ""
        self.config = {}
    
    def is_valid_config(self) -> bool:
        if self.config is not None:
            try:
                validate(self.config, schema=schema)
                return True
            except Exception as error:
                messagebox.showerror("Erreur", f"{error}")
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
