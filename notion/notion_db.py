
import requests
import os
from dotenv import load_dotenv
import pprint
import datetime

class NotionDB:

    def __init__(self, page_parent_id: str = "", db_title: str = f"Calendrier des cours {datetime.datetime.now().year}-{int(datetime.datetime.now().year)+1}", db_description: str = "Ce programme de cours présente une liste hebdomadaire exhaustive des sujets, lectures, devoirs et examens.", db_emoji: str = "🗓", db_id: str ="") -> None:
          # Load environment variables (Notion API Key)
        load_dotenv()
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")

        # Header of the HTTP request
        self.headers = {
            "Authorization": f"Bearer {self.NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22"
        }

        # If we locally create the db
        if db_id == "":
            self.db_dict = {
                "parent": {
                    "type": "page_id",
                    "page_id": page_parent_id
                },
                "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": db_title
                            }
                        }
                    ],
                "properties": {
                },
                "description":[{
                    "type": "text",
                    "text": {
                        "content": db_description
                    }
                }]
            }

            # Add db emoji
            if db_emoji:
                self.db_dict["icon"] = {
                    "type": "emoji",
                    "emoji": db_emoji
                }

            self.db_id = ""

    def add_columns_for_class(self, type_of_class: str):
        match type_of_class:
            case "1gy":
                columns = [
                    ("title", "Nom"), 
                    ("select", "Classe", [{"name": "Vide", "color": "blue"}, {"name": "1GY1", "color": "yellow"}, {"name": "1GY2", "color": "default"}, {"name": "1GY3", "color": "green"}, {"name": "1GY4", "color": "gray"}, {"name": "1GY5", "color": "red"}, {"name": "1GY6", "color": "pink"}, {"name": "1GY7", "color": "brown"}, {"name": "1GY8", "color": "blue"}, {"name": "1GY9", "color": "orange"}, {"name": "1GY10", "color": "purple"}, {"name": "1GY11", "color": "orange"}, {"name": "1GY12", "color": "brown"}]),
                    ("date", "Date du cours"),
                    ("select", "Durée du cours", [{"name":"1 période complète", "color": "purple"},{"name": "2 périodes complètes", "color": "blue"}, {"name": "-", "color": "green"}, {"name": "1ère période uniquement", "color": "orange"}, {"name": "2ème période uniquement", "color": "orange"}]),
                    ("multi_select", "Groupe", [{"name": "Groupe A+B", "color": "yellow"}, {"name": "Groupe A", "color": "brown"}, {"name": "Groupe B", "color": "orange"}, {"name": "1ère heure: A", "color":"pink"}, {"name": "1ère heure: B", "color":"pink"}, {"name": "2ème heure: A", "color":"pink"}, {"name": "2ème heure: B", "color":"pink"}, {"name": "-", "color":"green"}]),
                    ("multi_select", "Modalité du cours", [{"name": "📒 Leçon", "color": "yellow"}, {"name": "🔥 Examen", "color": "red"}, {"name": "⛱ Vacances", "color": "green"}, {"name": "⛱ Congé", "color": "green"},{"name": "⛱ Congé épreuves en commun", "color": "green"}, {"name": "⛱ Jour férié", "color": "green"}, {"name": "🔥 Examen en 1ère heure", "color": "red"}, {"name": "🔥🔥 Examen de synthèse", "color": "red"}]),
                    ("multi_select", "Notion étudiée", [{"name": "⛱ - ", "color": "green"}, {"name": "🎒Introduction au cours", "color": "gray"}, {"name": "💻Programmation", "color": "orange"}, {"name": "🔐 Cybersécurité", "color": "default"}, {"name": "🧩Représentation de l'information", "color": "yellow"}, {"name": "ℹ Informatique et société", "color": "purple"}, {"name": "💪🏼 Concours Castor Informatique", "color": "brown"}, {"name": "🔥 Distribution hottes Mails", "color": "red"}, {"name": "🖥 Architecture des ordinateurs", "color": "red"}, {"name": "🎨Web", "color": "pink"}]),
                    ("rich_text", "Remarque"),
                    ("number", "Série de semaine", "number")
                ]
            case "2gy":
                columns = [
                    ("title", "Nom"), 
                    ("select", "Classe", [{"name": "Vide", "color": "blue"}, {"name": "2GY1", "color": "yellow"}, {"name": "2GY2", "color": "default"}, {"name": "2GY3", "color": "green"}, {"name": "2GY4", "color": "gray"}, {"name": "2GY5", "color": "red"}, {"name": "2GY6", "color": "pink"}, {"name": "2GY7", "color": "brown"}, {"name": "2GY8", "color": "blue"}, {"name": "2GY9", "color": "orange"}, {"name": "2GY10", "color": "purple"}, {"name": "2GY11", "color": "orange"}, {"name": "2GY12", "color": "brown"}]),
                    ("date", "Date du cours"),
                    ("select", "Durée du cours", [{"name":"1 période complète", "color": "purple"},{"name": "2 périodes complètes", "color": "blue"}, {"name": "-", "color": "green"}, {"name": "1ère période uniquement", "color": "orange"}, {"name": "2ème période uniquement", "color": "orange"}]),
                    ("multi_select", "Groupe", [{"name": "Groupe A+B", "color": "yellow"}, {"name": "Groupe A", "color": "brown"}, {"name": "Groupe B", "color": "orange"}, {"name": "1ère heure: A", "color":"pink"}, {"name": "1ère heure: B", "color":"pink"}, {"name": "2ème heure: A", "color":"pink"}, {"name": "2ème heure: B", "color":"pink"}, {"name": "-", "color":"green"}]),
                    ("multi_select", "Modalité du cours", [{"name": "📒 Leçon", "color": "yellow"}, {"name": "🔥 Examen", "color": "red"}, {"name": "⛱ Vacances", "color": "green"}, {"name": "⛱ Congé", "color": "green"},{"name": "⛱ Congé épreuves en commun", "color": "green"}, {"name": "⛱ Jour férié", "color": "green"}, {"name": "🔥 Examen en 1ère heure", "color": "red"}, {"name": "🔥🔥 Examen de synthèse", "color": "red"}]),
                    ("multi_select", "Notion étudiée", [{"name": "⛱ - ", "color": "green"}, {"name": "🎒Introduction au cours", "color": "gray"}, {"name": "💻Programmation", "color": "orange"}, {"name": "🤖 Robotique", "color": "red"}, {"name": "💪🏼 Concours Castor Informatique", "color": "brown"}, {"name": "🧩Algorithmique", "color": "yellow"}, {"name": "ℹ Informatique et société", "color": "brown"}, {"name": "🔥 Distribution hottes Mails", "color": "red"}, {"name": "🎨 Web", "color": "pink"}, {"name": "🕵🏼‍♂️ Cryptographie", "color": "blue"}, {"name": "📁 Fichiers et formats de fichiers", "color": "brown"}, {"name": "📶 Applications web et réseaux", "color": "default"}, {"name": "📁 Bases de données", "color": "default"}, {"name": "Conclusion du cours", "color": "green"}]),
                    ("rich_text", "Remarque"),
                    ("number", "Série de semaine", "number")
                ]
            case "1ecg":
                pass

            case _:
                return "Unknown type of class"

        self.add_columns_into_db(columns)
    

    def add_columns_into_db(self, columns: list) -> None:
        # Add all columns into the database
        for column in columns:
            self.add_column_into_db(column)


    def add_column_into_db(self, column: tuple) -> None:

        # Check that tuple contains all elements
        if len(column) == 2:
            column = (*column, None)

        type, column_name, specific_info = column
        column_dict = {}

        # Add specific dict for each column type
        match type:
            case "checkbox":
                column_dict[column_name] = {
                    "name": column_name,
                      "type": "checkbox",
                      "checkbox": {}
                    }
            case "created_by":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "created_by",
                    "created_by": {}
                }
            case "created_time":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "created_time",
                    "created_time": {}
                }
            case "date":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "date",
                    "date": {}
                }
            case "email":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "email",
                    "email": {}
                }
            case "files":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "files",
                    "files": {}
                }
            case "last_edited_time":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "last_edited_time",
                    "last_edited_time": {}
                }
            case "multi_select":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "multi_select",
                    "multi_select": {
                        "options": [label for label in specific_info]
                    }
                }
            case "number":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "number",
                    "number": {
                        "format": specific_info
                    }
                }
            case "people":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "people",
                    "people": {}
                }
            case "phone_number":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "phone_number",
                    "phone_number": {}
                }
            case "rich_text":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "rich_text",
                    "rich_text": {}
                }
            case "select":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "select",
                    "select": {
                        "options": [label for label in specific_info]
                    }
                }
            case "title":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "title",
                    "title": {}
                }
            case "url":
                column_dict[column_name] = {
                    "name": column_name,
                    "type": "url",
                    "url": {}
                }
            case _:
                return "Impossible to add column into the database."
            
        self.db_dict['properties'][list(column_dict.keys())[0]] = column_dict[list(column_dict.keys())[0]]


    def add_row_to_db(self, row) -> None:
        pass

    def save_as_a_new_db(self) -> None:
        # POST the new page and save the id into the page_id attribute
        pprint.pprint(self.db_dict)
        res = requests.post("https://api.notion.com/v1/databases", headers=self.headers, json=self.db_dict)
        pprint.pprint(res.json())
        # self.db_id = res.json()['id']

            






