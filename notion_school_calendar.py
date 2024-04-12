import json
import os
import pprint
from datetime import *
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
from config.config import Config
from notion import notion_db, notion_page
from ui.app import *


def main():
    """Main function of the app"""

    # Create app GUI
    app_gui = AppUI()
    
    NOTION_ROOT_PAGE_ID = "a026cb1f-35fd-4631-a3e9-887e103c5d9a"

# GUI
if __name__ == "__main__":
    main()
