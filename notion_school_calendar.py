from datetime import datetime, timezone
import json
import os
import requests
from config.config import Config
from utils import *
from ui.menu import *
from ui.app import *
from notion import notion_page
from datetime import *
from dotenv import load_dotenv
import pprint

def main():

    # Create app GUI
    # app_gui = AppUI()
    
    NOTION_ROOT_PAGE_ID = "a026cb1f-35fd-4631-a3e9-887e103c5d9a"
    liste_page = []

    # page = notion_page.NotionPage(NOTION_ROOT_PAGE_ID, f"test_{0}")
    # page.create_page_for_a_class({})
    # page = notion_page.NotionPage(notion_page_id="48d78175-3e93-4331-88fb-c5f6c6bff437")
    # pprint.pprint(page.page_dict)
    # print(page.nb_blocks_saved_since_last_save)
    notion_page.NotionPage.create_pages_from_config({})
    # page.save_as_new_page()
    # notion_page.NotionPage.get_page_content("9001f534-d103-49bb-8381-c0dc59398beb")
    # page2 = notion_page.NotionPage(NOTION_ROOT_PAGE_ID, f"PAGE à ARCHIVER")
    # page2.save()
    # page2.edit_parent_page_id(page.page_id)
    # page2.save()



# GUI
if __name__ == "__main__":
    main()