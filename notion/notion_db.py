import datetime
import os
import pprint
import requests
from dotenv import load_dotenv
from notion import notion_page


class NotionDB:
    """Class to create a Notion database with the given title, description and emoji."""

    def __init__(self,  db_id: str = "", page_parent_id: str = "", db_title: str = "", db_description: str = "Ce programme de cours présente une liste hebdomadaire exhaustive des sujets, lectures, devoirs et examens.", db_emoji: str = "🗓") -> None:
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
                "description": [{
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
            # Database id that will be set after the db is saved to Notion
            self.db_id = ""

    def add_columns_for_class(self, type_of_class: str) -> None:
        """Add columns to the database according to the class given.
        :param type_of_class: The type of class [1gy, 2gy, 1ecg, 2ecg, 2ec, 3c] to add columns to the database."""

        # Update the title of the database to match class name
        self.db_dict["title"][0]["text"][
            "content"] = f"{type_of_class.upper()} - Calendrier des cours {datetime.datetime.now().year}-{int(datetime.datetime.now().year)+1}"

        # Choose the columns schema according to the class given
        match type_of_class:
            case "1gy":
                columns = [
                    ("title", "Nom"),
                    ("select", "Classe", [{"name": "Vide", "color": "blue"}, {"name": "1GY1", "color": "yellow"}, {"name": "1GY2", "color": "default"}, {"name": "1GY3", "color": "green"}, {"name": "1GY4", "color": "gray"}, {"name": "1GY5", "color": "red"}, {
                     "name": "1GY6", "color": "pink"}, {"name": "1GY7", "color": "brown"}, {"name": "1GY8", "color": "blue"}, {"name": "1GY9", "color": "orange"}, {"name": "1GY10", "color": "purple"}, {"name": "1GY11", "color": "orange"}, {"name": "1GY12", "color": "brown"}]),
                    ("date", "Date du cours"),
                    ("select", "Durée du cours", [{"name": "1 période complète", "color": "purple"}, {"name": "2 périodes complètes", "color": "blue"}, {
                     "name": "-", "color": "green"}, {"name": "1ère période uniquement", "color": "orange"}, {"name": "2ème période uniquement", "color": "orange"}]),
                    ("multi_select", "Groupe", [{"name": "Groupe A+B", "color": "yellow"}, {"name": "Groupe A", "color": "brown"}, {"name": "Groupe B", "color": "orange"}, {"name": "1ère heure: A", "color": "pink"}, {
                     "name": "1ère heure: B", "color": "pink"}, {"name": "2ème heure: A", "color": "pink"}, {"name": "2ème heure: B", "color": "pink"}, {"name": "-", "color": "green"}]),
                    ("multi_select", "Modalité du cours", [{"name": "📒 Leçon", "color": "yellow"}, {"name": "🔥 Examen", "color": "red"}, {"name": "⛱ Vacances", "color": "green"}, {"name": "⛱ Congé", "color": "green"}, {
                     "name": "⛱ Congé épreuves en commun", "color": "green"}, {"name": "⛱ Jour férié", "color": "green"}, {"name": "🔥 Examen en 1ère heure", "color": "red"}, {"name": "🔥🔥 Examen de synthèse", "color": "red"}]),
                    ("multi_select", "Notion étudiée", [{"name": "⛱ - ", "color": "green"}, {"name": "🎒Introduction au cours", "color": "gray"}, {"name": "💻Programmation", "color": "orange"}, {"name": "🔐 Cybersécurité", "color": "default"}, {"name": "🧩Représentation de l'information", "color": "yellow"}, {
                     "name": "ℹ Informatique et société", "color": "purple"}, {"name": "💪🏼 Concours Castor Informatique", "color": "brown"}, {"name": "🔥 Distribution hottes Mails", "color": "red"}, {"name": "🖥 Architecture des ordinateurs", "color": "red"}, {"name": "🎨Web", "color": "pink"}]),
                    ("rich_text", "Remarque"),
                    ("number", "Série de semaine", "number")
                ]
            case "2gy":
                columns = [
                    ("title", "Nom"),
                    ("select", "Classe", [{"name": "Vide", "color": "blue"}, {"name": "2GY1", "color": "yellow"}, {"name": "2GY2", "color": "default"}, {"name": "2GY3", "color": "green"}, {"name": "2GY4", "color": "gray"}, {"name": "2GY5", "color": "red"}, {
                     "name": "2GY6", "color": "pink"}, {"name": "2GY7", "color": "brown"}, {"name": "2GY8", "color": "blue"}, {"name": "2GY9", "color": "orange"}, {"name": "2GY10", "color": "purple"}, {"name": "2GY11", "color": "orange"}, {"name": "2GY12", "color": "brown"}]),
                    ("date", "Date du cours"),
                    ("select", "Durée du cours", [{"name": "1 période complète", "color": "purple"}, {"name": "2 périodes complètes", "color": "blue"}, {
                     "name": "-", "color": "green"}, {"name": "1ère période uniquement", "color": "orange"}, {"name": "2ème période uniquement", "color": "orange"}]),
                    ("multi_select", "Groupe", [{"name": "Groupe A+B", "color": "yellow"}, {"name": "Groupe A", "color": "brown"}, {"name": "Groupe B", "color": "orange"}, {"name": "1ère heure: A", "color": "pink"}, {
                     "name": "1ère heure: B", "color": "pink"}, {"name": "2ème heure: A", "color": "pink"}, {"name": "2ème heure: B", "color": "pink"}, {"name": "-", "color": "green"}]),
                    ("multi_select", "Modalité du cours", [{"name": "📒 Leçon", "color": "yellow"}, {"name": "🔥 Examen", "color": "red"}, {"name": "⛱ Vacances", "color": "green"}, {"name": "⛱ Congé", "color": "green"}, {
                     "name": "⛱ Congé épreuves en commun", "color": "green"}, {"name": "⛱ Jour férié", "color": "green"}, {"name": "🔥 Examen en 1ère heure", "color": "red"}, {"name": "🔥🔥 Examen de synthèse", "color": "red"}]),
                    ("multi_select", "Notion étudiée", [{"name": "⛱ - ", "color": "green"}, {"name": "🎒Introduction au cours", "color": "gray"}, {"name": "💻Programmation", "color": "orange"}, {"name": "🤖 Robotique", "color": "red"}, {"name": "💪🏼 Concours Castor Informatique", "color": "brown"}, {"name": "🧩Algorithmique", "color": "yellow"}, {"name": "ℹ Informatique et société", "color": "brown"}, {
                     "name": "🔥 Distribution hottes Mails", "color": "red"}, {"name": "🎨 Web", "color": "pink"}, {"name": "🕵🏼‍♂️ Cryptographie", "color": "blue"}, {"name": "📁 Fichiers et formats de fichiers", "color": "brown"}, {"name": "📶 Applications web et réseaux", "color": "default"}, {"name": "📁 Bases de données", "color": "default"}, {"name": "💤 Conclusion du cours", "color": "green"}]),
                    ("rich_text", "Remarque"),
                    ("number", "Série de semaine", "number")
                ]
            case "1ecg":
                columns = [
                    ("title", "Nom"),
                    ("select", "Classe", [{"name": "Vide", "color": "blue"}, {"name": "1ECG1", "color": "yellow"}, {"name": "1ECG2", "color": "default"}, {"name": "1ECG3", "color": "green"}, {"name": "1ECG4", "color": "gray"}, {"name": "1ECG5", "color": "red"}, {
                     "name": "1ECG6", "color": "pink"}, {"name": "1ECG7", "color": "brown"}, {"name": "1ECG8", "color": "blue"}, {"name": "1ECG9", "color": "orange"}, {"name": "1ECG10", "color": "purple"}, {"name": "1ECG11", "color": "orange"}, {"name": "1ECG12", "color": "brown"}]),
                    ("date", "Date du cours"),
                    ("select", "Durée du cours", [{"name": "1 période complète", "color": "purple"}, {"name": "2 périodes complètes", "color": "blue"}, {
                     "name": "-", "color": "green"}, {"name": "1ère période uniquement", "color": "orange"}, {"name": "2ème période uniquement", "color": "orange"}]),
                    ("multi_select", "Groupe", [{"name": "Groupe A+B", "color": "yellow"}, {"name": "Groupe A", "color": "brown"}, {"name": "Groupe B", "color": "orange"}, {"name": "1ère heure: A", "color": "pink"}, {
                     "name": "1ère heure: B", "color": "pink"}, {"name": "2ème heure: A", "color": "pink"}, {"name": "2ème heure: B", "color": "pink"}, {"name": "-", "color": "green"}]),
                    ("multi_select", "Modalité du cours", [{"name": "📒 Leçon", "color": "yellow"}, {"name": "🔥 Examen", "color": "red"}, {"name": "⛱ Vacances", "color": "green"}, {"name": "⛱ Congé", "color": "green"}, {
                     "name": "⛱ Congé épreuves en commun", "color": "green"}, {"name": "⛱ Jour férié", "color": "green"}, {"name": "🔥 Examen en 1ère heure", "color": "red"}, {"name": "🔥🔥 Examen de synthèse", "color": "red"}]),
                    ("multi_select", "Notion étudiée", [{"name": "⛱ - ", "color": "green"}, {"name": "🎒Introduction au cours", "color": "gray"}, {"name": "📧 Courriel", "color": "gray"}, {"name": "📁 Fichiers", "color": "brown"}, {"name": "📄 Word", "color": "blue"}, {"name": "🖼 Powerpoint", "color": "purple"}, {
                     "name": "ℹ Informatique et société", "color": "red"}, {"name": "⌨ Matériel informatique", "color": "yellow"}, {"name": "⚫⚪ Représentation de l'information", "color": "default"}, {"name": "🎨 Multimédia", "color": "pink"}, {"name": "💻Programmation", "color": "orange"}]),
                    ("rich_text", "Remarque"),
                    ("number", "Série de semaine", "number")
                ]

            case "2ecg":
                columns = [
                    ("title", "Nom"),
                    ("select", "Classe", [{"name": "Vide", "color": "blue"}, {"name": "2ECG1", "color": "yellow"}, {"name": "2ECG2", "color": "default"}, {"name": "2ECG3", "color": "green"}, {"name": "2ECG4", "color": "gray"}, {"name": "2ECG5", "color": "red"}, {
                     "name": "2ECG6", "color": "pink"}, {"name": "2ECG7", "color": "brown"}, {"name": "2ECG8", "color": "blue"}, {"name": "2ECG9", "color": "orange"}, {"name": "2ECG10", "color": "purple"}, {"name": "2ECG11", "color": "orange"}, {"name": "2ECG12", "color": "brown"}]),
                    ("date", "Date du cours"),
                    ("select", "Durée du cours", [{"name": "1 période complète", "color": "purple"}, {"name": "2 périodes complètes", "color": "blue"}, {
                     "name": "-", "color": "green"}, {"name": "1ère période uniquement", "color": "orange"}, {"name": "2ème période uniquement", "color": "orange"}]),
                    ("multi_select", "Groupe", [{"name": "Groupe A+B", "color": "yellow"}, {"name": "Groupe A", "color": "brown"}, {"name": "Groupe B", "color": "orange"}, {"name": "1ère heure: A", "color": "pink"}, {
                     "name": "1ère heure: B", "color": "pink"}, {"name": "2ème heure: A", "color": "pink"}, {"name": "2ème heure: B", "color": "pink"}, {"name": "-", "color": "green"}]),
                    ("multi_select", "Modalité du cours", [{"name": "📒 Leçon", "color": "yellow"}, {"name": "🔥 Examen", "color": "red"}, {"name": "⛱ Vacances", "color": "green"}, {"name": "⛱ Congé", "color": "green"}, {
                     "name": "⛱ Congé épreuves en commun", "color": "green"}, {"name": "⛱ Jour férié", "color": "green"}, {"name": "🔥 Examen en 1ère heure", "color": "red"}, {"name": "🔥🔥 Examen de synthèse", "color": "red"}]),
                    ("multi_select", "Notion étudiée", [{"name": "⛱ - ", "color": "green"}, {"name": "🎒Introduction au cours", "color": "gray"}, {"name": "📧 Révisions sur le courriel", "color": "gray"}, {"name": "📁 Révisions sur les fichiers", "color": "brown"}, {"name": "📄 Révisions Word", "color": "brown"}, {"name": "📄 Word", "color": "blue"}, {
                     "name": "📈 Excel", "color": "pink"}, {"name": "ℹ Informatique et société", "color": "red"}, {"name": "⌨ ASSAP", "color": "yellow"}, {"name": "💻 Programmation", "color": "default"}, {"name": "💪🏼 Concours Castor Informatique", "color": "purple"}, {"name": "💻Programmation", "color": "orange"}]),
                    ("rich_text", "Remarque"),
                    ("number", "Série de semaine", "number")
                ]

            case "2ec":
                columns = [
                    ("title", "Nom"),
                    ("select", "Classe", [{"name": "Vide", "color": "blue"}, {"name": "2EC1", "color": "yellow"}, {"name": "2EC2", "color": "default"}, {"name": "2EC3", "color": "green"}, {"name": "2EC4", "color": "gray"}, {"name": "2EC5", "color": "red"}, {
                     "name": "2EC6", "color": "pink"}, {"name": "2EC7", "color": "brown"}, {"name": "2EC8", "color": "blue"}, {"name": "2EC9", "color": "orange"}, {"name": "2EC10", "color": "purple"}, {"name": "2EC11", "color": "orange"}, {"name": "2EC12", "color": "brown"}]),
                    ("date", "Date du cours"),
                    ("select", "Durée du cours", [
                     {"name": "1 période complète", "color": "purple"}, {"name": "-", "color": "green"}]),
                    ("multi_select", "Groupe", [
                     {"name": "Classe entière", "color": "orange"}, {"name": "-", "color": "green"}]),
                    ("multi_select", "Modalité du cours", [{"name": "📒 Leçon", "color": "yellow"}, {"name": "🔥 Examen", "color": "red"}, {"name": "⛱ Vacances", "color": "green"}, {
                     "name": "⛱ Congé", "color": "green"}, {"name": "⛱ Congé épreuves en commun", "color": "green"}, {"name": "⛱ Jour férié", "color": "green"}]),
                    ("multi_select", "Notion étudiée", [{"name": "⛱ - ", "color": "green"}, {"name": "🎒Introduction au cours", "color": "gray"}, {"name": "📕 Révisions offre", "color": "red"}, {"name": "📗 Révisions commande", "color": "brown"}, {"name": "🧾 Révisions confirmation de commande", "color": "brown"}, {
                     "name": "😤 Réclamation", "color": "orange"}, {"name": "❗ Rappel", "color": "pink"}, {"name": "🕜 Prorogation", "color": "yellow"}, {"name": "😊 Remerciements", "color": "red"}, {"name": "🔝 Offre publicitaire", "color": "blue"}, {"name": "🏤 Négociation", "color": "purple"}, {"name": "💁🏼‍♂️ Oral ou relance", "color": "orange"}]),
                    ("rich_text", "Remarque"),
                    ("number", "Série de semaine", "number")
                ]

            case "3ec":
                columns = [
                    ("title", "Nom"),
                    ("select", "Classe", [{"name": "Vide", "color": "blue"}, {"name": "3EC1", "color": "yellow"}, {"name": "3EC2", "color": "default"}, {"name": "3EC3", "color": "green"}, {"name": "3EC4", "color": "gray"}, {"name": "3EC5", "color": "red"}, {
                     "name": "3EC6", "color": "pink"}, {"name": "3EC7", "color": "brown"}, {"name": "3EC8", "color": "blue"}, {"name": "3EC9", "color": "orange"}, {"name": "3EC10", "color": "purple"}, {"name": "3EC11", "color": "orange"}, {"name": "3EC12", "color": "brown"}]),
                    ("date", "Date du cours"),
                    ("select", "Durée du cours", [
                     {"name": "1 période complète", "color": "purple"}, {"name": "-", "color": "green"}]),
                    ("multi_select", "Groupe", [
                     {"name": "Classe entière", "color": "orange"}, {"name": "-", "color": "green"}]),
                    ("multi_select", "Modalité du cours", [{"name": "📒 Leçon", "color": "yellow"}, {"name": "🔥 Examen", "color": "red"}, {"name": "⛱ Vacances", "color": "green"}, {
                     "name": "⛱ Congé", "color": "green"}, {"name": "⛱ Congé épreuves en commun", "color": "green"}, {"name": "⛱ Jour férié", "color": "green"}]),
                    ("multi_select", "Notion étudiée", [{"name": "⛱ - ", "color": "green"}, {"name": "🎒Introduction au cours", "color": "gray"}, {"name": "📕 Révisions demande d'offre et offre", "color": "red"}, {"name": "📗 Révisions commande", "color": "brown"}, {"name": "💌 Invitation et convocation", "color": "brown"}, {
                     "name": "📄 Documents internes", "color": "orange"}, {"name": "💲 Révision recouvrement de créances", "color": "pink"}, {"name": "💲 Assurances", "color": "yellow"}, {"name": "😠 Révisions réclamation", "color": "red"}, {"name": "🔄 Cas complet", "color": "blue"}]),
                    ("rich_text", "Remarque", [{"name": "Remarque de test"}]),
                    ("number", "Série de semaine", "number")
                ]

            case "test":
                columns= [
                    ("title", "Nom"),
                    ("url", "Site")
                ]
            case _:
                return None

        # Add columns into the database
        self.add_columns_into_db(columns)

    def add_columns_into_db(self, columns: list) -> None:
        """Add a list of columns into the database.
        :param columns: A list of columns to add into the database.
            Each column should be a tuple containing the column type, column name and specific info if needed.
                - colum_type can be: "checkbox", "created_by", "created_time", "date", "email", "files", "last_edited_time", "multi_select", "number", "people", "phone_number", "rich_text", "select", "title", "url"
                - column_name is the name of the column
                - specific_info is
                    - a list of options for multi_select type
                    - a list of options for select type
                    - None for other types of columns.
        """

        for column in columns:
            self.add_column_into_db(column)

    def add_column_into_db(self, column: tuple) -> None:
        """"Add a column into the database.
            Each tuple should contain the column type, column name and specific info if needed.
                - colum_type can be: "checkbox", "created_by", "created_time", "date", "email", "files", "last_edited_time", "multi_select", "number", "people", "phone_number", "rich_text", "select", "title", "url"
                - column_name is the name of the column
                - specific_info is
                    - a list of options for multi_select type
                    - a list of options for select type
                    - None for other types of columns.
        """

        # Check that tuple contains all elements
        if len(column) == 2:
            column = (*column, None)

        # Unpack the tuple to get the column type, column name and specific info
        column_type, column_name, specific_info = column
        column_dict = {}

        # Add specific dict for each column type
        match column_type:
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
                return None

        self.db_dict['properties'][list(column_dict.keys())[0]] = column_dict[list(column_dict.keys())[0]]

    def add_default_row_for_class(self, class_name: "str", nb_week: int, date_lesson: str,
    duration: str, group: list, modality: list, topics: list, group_week: int) -> None:
        """Add rows into the database according to the class given.
            :param class_name: The name of the class to add rows to the database.
            :param nb_week: The number of the week.
            :param date_lesson: The date of the lesson.
            :param duration: The duration of the lesson.
            :param group: The group of the lesson.
            :param modality: The modality of the lesson.
            :param topics: The topics of the lesson.
            :param group_week: The group of the week.
        """

        # Check if db is already saved
        if self.db_id:
            # Create a new page
            page = notion_page.NotionPage(self.db_id, "database_id", emoji="📙")

            # Add properties (=one row ) to the page
            page.add_page_properties([
                ("title", "Nom", f"Semaine {nb_week}"),
                ("select", "Classe", class_name),
                ("date", "Date du cours", (date_lesson, None, None)),
                ("select", "Durée du cours", duration),
                ("multi_select", "Groupe", group),
                ("multi_select", "Modalité du cours", modality),
                ("multi_select", "Notion étudiée", topics),
                ("rich_text", "Remarque", []),
                ("number", "Série de semaine", group_week)
            ])
            
            # Add default heading to the page
            page.add_heading(1, "Programme")

            self.save_page_into_db(page)

        else:
            print("Please, save db before adding rows")

    def add_rows_into_db(self, rows: list[list]) -> None:
        """Add a list of rows into the database.
            :param rows: A list of rows to add into the database.
        """

        for row in rows:
            self.add_row_into_db(row)

    def add_row_into_db(self, row: list) -> None:
        """Add a row into the database.
            :param row: A list of elements to add into the database.
        """

        # Check that the column names of the given row matches the columns of the database and check that each column type is correct
        if len([ element[1] for element in row if element[1] not in self.db_dict["properties"].keys()]) > 0:
            print("The property name doesn't match the column name of the database: row not inserted into the database.")

        elif False in [True if element[0] == self.db_dict["properties"][element[1]]["type"] else False for element in row ]:
            print("The property type doesn't match the column type of the database: row not inserted into the database.")

        else:
            page = notion_page.NotionPage(self.db_id, "database_id", emoji="")
            for element in row:
                page.add_page_property(element)
            self.save_page_into_db(page)

    def save_page_into_db(self, page: notion_page.NotionPage) -> None:
        """Save a page into the database.
            :param page: The page to save into the database.
        """

        page.save_as_new_page()

    def save_as_a_new_db(self) -> None:
        """POST the new page and save the id into the db_id attribute"""

        res = requests.post("https://api.notion.com/v1/databases",
                            headers=self.headers, json=self.db_dict, timeout=10)
        self.db_id = res.json()['id']
