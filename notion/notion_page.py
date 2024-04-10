import copy
import datetime
import os
import pprint
from typing import List, Tuple
import requests
from dotenv import load_dotenv


class NotionPage:
    """Class to create, edit and save a page to Notion"""

    def __init__(self, parent_id: str = "", parent_type: str = "page_id", page_title: str = "", emoji: str = "", page_id=""):
        # Load environment variables (Notion API Key)
        load_dotenv()
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")

        # Header of the HTTP request
        self.headers = {
            "Authorization": f"Bearer {self.NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22"
        }

        # If we create the page locally
        if page_id == "":
            self.page_dict = {
                "parent": {
                    "type": parent_type,
                    parent_type: parent_id
                },
                "properties": {
                    "title": [
                        {
                            "text": {
                                "content": page_title
                            }
                        }
                    ]
                },
                "children": [],
            }

            if emoji:
                self.page_dict["icon"] = {
                    "type": "emoji",
                    "emoji": emoji
                }

            self.page_id = ""

            # Store the number of blocks not saved since last saved
            # Is used to determine which content blocks aren't saved to Notion
            self.nb_blocks_not_saved_since_last_save = 0

        # If the page is loaded from Notion
        else:
            self.get_page_properties_from_notion(page_id)
            self.get_page_content_from_notion(page_id)

    def get_page_properties_from_notion(self, page_id) -> None:
        """Get page properties from Notion
            :param page_id: the id of the page to get the properties from
        """
        res = requests.get(
            f"https://api.notion.com/v1/pages/{page_id}", headers=self.headers, timeout=5)
        self.page_id = res.json()["id"]
        self.page_dict = res.json()

    def get_page_content_from_notion(self, page_id) -> None:
        """Get page content from Notion
            :param page_id: the id of the page to get the content from
        """
        res = requests.get(
            f"https://api.notion.com/v1/blocks/{page_id}/children", headers=self.headers, timeout=5)
        self.page_dict["children"] = res.json()["results"]
        self.nb_blocks_not_saved_since_last_save = 0

    def save_as_new_page(self) -> None:
        """POST the new page and save the id into the page_id attribute"""

        res = requests.post("https://api.notion.com/v1/pages",
                            headers=self.headers, json=self.page_dict, timeout=5)
        print(res.json())
        self.page_id = res.json()['id']
        self.nb_blocks_not_saved_since_last_save = 0

    def add_page_properties(self, properties: List[Tuple]) -> None:
        """Add all properties to the page
            :param properties: a list of properties tuplle to add into the page
        """

        for property in properties:
            self.add_page_property(property)

    def add_page_property(self, property: Tuple) -> None:
        """Add a property tuple to the page
            :param property: tuple that must respect the following format: (property_type, property_name, property_value)
                - property_type can be one of the following: "checkbox", "created_by", "created_time", "date", "email", "files", "last_edited_time", "multi_select", "number", "people", "phone_number", "rich_text", "select", "title", "url"
                - property_name is the name of the property: pay attention, the property name must be the same as the column name in the database it belongs to
                - property_value is the value of the property, depending on the property_type, it can be one of the following types:
                    - For checkbox: a boolean that is True or False
                    - For date: a tuple having the following format: (start, end, time_zone)
                    - For email: a string
                    - For files: a list of lists having the following format: [[name_of_file, url_of_file], [name_of_file, url_of_file], ...]
                    - For multi_select: a list of strings having the following format: [value1, value2, ...]
                    - For number: a float/integer number
                    - For people: a list of Notion users id strings having the following format: [user_id1, user_id2, ...]
                    - For phone_number: a string representing a phone number
                    - For rich_text: a list of strings having the following format: [text1, text2, ...]
                    - For select: a string representing the value of the select
                    - For title: a string representing the title of the page
                    - For url: a string representing an url
        """

        # Unpack the property tuple
        property_type, property_name, property_value = property

        match property_type:
            case "checkbox":
                self.page_dict["properties"][property_name] = property_value

            case "created_by":
                print("Notion API doesn't allow to set the created_by property")
                return None

            case "created_time":
                print("Notion API doesn't allow to set the created_time property")
                return None

            case "date":
                self.page_dict["properties"][property_name] = {
                    "start": property_value[0],
                    "end": property_value[1],
                    "time_zone": property_value[2]
                }

            case "email":
                self.page_dict["properties"][property_name] = property_value

            case "files":
                self.page_dict["properties"][property_name] = []
                for value in property_value:
                    self.page_dict["properties"][property_name].append(
                        {
                            "name": value[0],
                            "external": {
                                "url": value[1]
                            }
                        }
                    )

            case "last_edited_time":
                print("Notion API doesn't allow to set the last_edited_time property")
                return None

            case "multi_select":
                self.page_dict["properties"][property_name] = []
                for value in property_value:
                    self.page_dict["properties"][property_name].append(
                        {
                            "name": value
                        }
                    )

            case "number":
                self.page_dict["properties"][property_name] = property_value

            case "people":
                self.page_dict["properties"][property_name] = []
                for value in property_value:
                    self.page_dict["properties"][property_name].append(
                        {
                            "id": value
                        }
                    )

            case "phone_number":
                self.page_dict["properties"][property_name] = property_value

            case "rich_text":
                self.page_dict["properties"][property_name] = []
                for value in property_value:
                    self.page_dict["properties"][property_name].append(
                        {
                            "text": {
                                "content": value,
                                "link": None
                            }
                        }
                    )

            case "select":
                self.page_dict["properties"][property_name] = {
                    "name": property_value,
                }

            case "title":
                self.page_dict["properties"]["title"][0]["text"]["content"] = property_value

            case "url":
                self.page_dict["properties"][property_name] = property_value

            case _:
                return None

    def append_unsaved_content_to_same_page(self) -> str:
        """Append the unsaved content to the same page"""

        # If the page has already been saved, then append the unsaved content to the same page and save it again
        if self.page_id:
            res = requests.patch(f"https://api.notion.com/v1/blocks/{self.page_id}/children", headers=self.headers, json={
                                 "children": self.page_dict["children"][self.nb_blocks_not_saved_since_last_save:]}, timeout=10)
            self.page_dict["children"] = res.json()["results"]
            self.nb_blocks_not_saved_since_last_save = 0

    def add_heading(self, heading_level: int, text_content: str, text_color: str = "default") -> None:
        """Add heading into the page content
        :param heading_level: can be one of the following: 1, 2, 3
        :param text_content: is the text content of the heading
        :param text_color: can be one of the following: "default", "gray", "brown", "orange", "yellow", "green", "blue", "purple", "pink", "red"
        """

        if heading_level == 1 or heading_level == 2 or heading_level == 3:
            self.page_dict["children"].append(
                {
                    "object": "block",
                    f"heading_{heading_level}":
                        {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": text_content,
                                    },
                                }
                            ],
                            "color": text_color
                        }
                }
            )
            self.nb_blocks_not_saved_since_last_save += 1

    def add_paragraph(self, text_content: str, text_color: str = "default", url: str = None, new_paragraph: bool = True) -> None:
        """Add paragraph into the page content
        :param text_content: is the text content of the paragraph
        :param text_color: can be one of the following: "default", "gray", "brown", "orange", "yellow", "green", "blue", "purple", "pink", "red"
        :param url: is the url to add to the text content
        :param new_paragraph: if True, add a new paragraph, else append some text to the last paragraph added into the page content        
        """
        if new_paragraph:
            paragraph = {
                "object": "block",
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": text_content
                            },
                        }
                    ],
                    "color": text_color
                }
            }
            if url:
                paragraph["paragraph"]["rich_text"][0]["text"]["link"] = {
                    "url": url}

            self.page_dict["children"].append(paragraph)
            self.nb_blocks_not_saved_since_last_save += 1

        # Append some text to the last paragraph added into the page content
        else:
            # Check if the last element added into the page is a paragraph
            if "paragraph" in self.page_dict["children"][-1]:
                self.page_dict["children"][-1]["paragraph"]["rich_text"].append(
                    {
                        "text": {
                            "content": f" {text_content}"
                        },
                    }
                )
                if url:
                    self.page_dict["children"][-1]["paragraph"]["rich_text"][-1]["text"]["link"] = {
                        "url": url}

            # Else, add a new paragraph
            else:
                self.add_paragraph(
                    text_content, text_color=text_color, url=url, new_paragraph=True)

    def add_divider(self) -> None:
        """Add divider into the page content"""

        self.page_dict["children"].append(
            {
                "object": "block",
                "divider": {}
            }
        )
        self.nb_blocks_not_saved_since_last_save += 1

    def add_numbered_list(self, text_bullet_point: str) -> None:
        """Add numbered list into the page content
        :param text_bullet_point: is the text content of the bullet point
        """

        # Add numbered list into the page content
        self.page_dict["children"].append(
            {
                "object": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text":
                        [
                            {
                                "text": {
                                    "content": text_bullet_point,
                                    "link": {
                                        "url": ""
                                    }
                                },
                            }
                        ],
                    "color": ""
                }
            }
        )
        self.nb_blocks_not_saved_since_last_save += 1

    def add_table(self, list_of_lists: dict, has_column_header: bool = False, has_row_header: bool = False) -> None:
        """Add table into the page content
        :param list_of_lists: is a list of lists containing the table content
        :param has_column_header: if True, the table has a column header
        :param has_row_header: if True, the table has a row header
        """

        # Empty table (= without rows)
        table_dict = {
            "type": "table",
            "table": {
                "table_width": len(list_of_lists[0]),
                "has_column_header": has_column_header,
                "has_row_header": has_column_header,
                "children": []
            }
        }

        # Empty row (=without cells)
        row_dict = {
            "type": "table_row",
            "table_row": {
                "cells": []
            }
        }

        # Add cells to rows and rows to table
        for row in list_of_lists:
            row_to_add = copy.deepcopy(row_dict)
            for cell_content in row:
                row_to_add["table_row"]["cells"].append([
                    {
                        "type": "text",
                        "text": {
                            "content": cell_content,
                        }
                    }
                ])
            table_dict["table"]["children"].append(row_to_add)

        # Add the table to the page content
        self.page_dict["children"].append(table_dict)
        self.nb_blocks_not_saved_since_last_save += 1

    def create_page_for_a_class(self, class_info: dict) -> None:
        """Create a page for a class
        :param class_info: a dict containing the class information
        """
        # Divider
        self.add_divider()

        # About the teacher
        self.add_heading(2, "A propos de l'enseignant")
        self.add_paragraph("👨🏼‍🏫 Johan Jobin")
        self.add_paragraph("📧")
        self.add_paragraph("adresse", url="mailto:adresse",
                           new_paragraph=False)

        # About the course
        self.add_heading(2, "A propos du cours")
        self.add_paragraph("📄 Moodle du cours")
        self.add_paragraph(
            f"🧭 Le cours a lieu chaque semaine le lundi de 8h10-9h45 (salle 202) ainsi que le jeudi de 8h10-8h55 (salle 202).")
        self.add_paragraph("💻")
        self.add_paragraph(
            f"Accès à JupyterHub", url="https://jupyterhub.informatique-csud.ch", new_paragraph=False)
        self.add_paragraph(f"🤓")
        self.add_paragraph(f"Liste des comptes JupyterHub de tous les étudiants",
                           url="https://www.notion.so/Liste-des-comptes-JupyterHub-de-tous-les-tudiants-23-24-0131d95a68c941a583a90c930f36541f?pvs=21", new_paragraph=False)
        self.add_paragraph(f"👨🏼‍💻 23 élèves.")

        # Database
        self.add_heading(2, "Calendrier détaillé des cours")

        # Groupes
        self.add_heading(2, "Groupes")


    @staticmethod
    def create_pages_from_config(config: dict) -> None:
        """Create pages from a configuration file
        :param config: a dict containing the configuration
        """

        # Page id where the hierarchy of pages has to be appended
        page_root_id = "a026cb1f-35fd-4631-a3e9-887e103c5d9a"

        # Year interval: 2023-2024
        # Short year interval: 23-24
        current_year_interval = f"{datetime.datetime.now().year}-{int(datetime.datetime.now().year)+1}"
        short_current_year_interval = f"{str(datetime.datetime.now().year)[2:]}-{str(int(datetime.datetime.now().year)+1)[2:]}"

        # Create page with general info
        page_general_info = NotionPage(
            page_root_id, f"Année {current_year_interval}")
        page_general_info.add_heading(2, "Informations générales")
        page_general_info.save_as_new_page()

        # Create page with all JupyterHub accounts
        page_jupyterhub = NotionPage(
            page_general_info.page_id, f"Liste des comptes JupyterHub de tous les étudiants [{short_current_year_interval}]", "🤓")
        page_jupyterhub.add_paragraph(
            "Vous trouverez ci-dessous votre nom d'utilisateur pour accéder à")
        page_jupyterhub.add_paragraph(
            "la plateforme JupyterHub", url="https://jupyterhub.informatique-csud.ch", new_paragraph=False)
        page_jupyterhub.add_paragraph(
            "qui sera utilisée toute l'année pour apprendre la programmation Python")
        page_jupyterhub.save_as_new_page()

        # Create page for exams retaking
        page_exam_retaking = NotionPage(
            page_general_info.page_id, f"Rattrapages examens [{short_current_year_interval}]", "📄")
        page_exam_retaking.add_table([["Classe", "Elève", "Date rattrapage", "Etat"], [
                                     " ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]])
        page_exam_retaking.save_as_new_page()

        # Create page for the schedule
        schedule_page = NotionPage(
            page_general_info.page_id, f"Horaires [{short_current_year_interval}]", "📆")
        schedule_page.save_as_new_page()

        # Create page for the maturity work
        tm_page = NotionPage(page_general_info.page_id,
                             f"Travaux de maturité [{short_current_year_interval}]", "📄")
        tm_page.add_heading(2, "Sujet")
        tm_page.add_paragraph("Description du sujet à ajouter ici")
        tm_page.add_heading(2, "Calendrier des séances/échéances")
        tm_page.save_as_new_page()

        page_general_info.add_heading(2, "Heading ajouté par après")
        page_general_info.append_unsaved_content_to_same_page()
