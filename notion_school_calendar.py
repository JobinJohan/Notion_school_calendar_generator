from datetime import datetime, timezone
from dotenv import load_dotenv
import json
import os
import requests
from config.config import Config
from utils import *
from ui.menu import *
from ui.app import *


def main():

    app_gui = AppUI()


    

    # Load environment variables (Notion API Key)
    load_dotenv()
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")


    NOTION_ROOT_PAGE_ID = "a026cb1f-35fd-4631-a3e9-887e103c5d9a"

    headers = {
        "Authorization": "Bearer " + NOTION_API_KEY,
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }

    # # Configuration
    # configuration = Config()
    # configuration.load_config()
    # try:
    #     configuration.save_config()
    # except Exception:
    #     print("erreur")


# GUI
if __name__ == "__main__":
    main()
    

# Modification of the root page
# modified_page = {
#     "parent": {
#         "type": "page_id",
#         "page_id": NOTION_ROOT_PAGE_ID
#     },

#     "properties":{
#         "title":[
#             {
#                 "text": {
#                     "content": f"Année {datetime.today().year}-{int(datetime.today().year)+1} test"
#                 }
#             }
#         ]
#     }
# }

# res = requests.patch(f"https://api.notion.com/v1/pages/{NOTION_ROOT_PAGE_ID}", headers=headers, json=modified_page)
# print(res.json())

# # Add page that shows all different pages
# new_page = {
#     "parent": {
#         "type": "page_id",
#         "page_id": NOTION_ROOT_PAGE_ID
#     },
#     "properties": {
#         "title": [
#                 {
#                     "text": {
#                         "content": "Tuscan kale"
#                     }
#                 }
#             ]
#     },
#     "children": [
#         {
#             "object": "block",
#             "heading_2": {
#                 "rich_text": [
#                     {
#                         "text": {
#                             "content": "Lacinato kale"
#                         }
#                     }
#                 ]
#             }
#         },
#         {
#             "object": "block",
#             "paragraph": {
#                 "rich_text": [
#                     {
#                         "text": {
#                             "content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
#                             "link": {
#                                 "url": "https://en.wikipedia.org/wiki/Lacinato_kale"
#                             }
#                         },
#                         "href": "https://en.wikipedia.org/wiki/Lacinato_kale"
#                     }
#                 ],
#                 "color": "default"
#             }
#         }
#     ]
# }

# res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=new_page)
# print(res.json())