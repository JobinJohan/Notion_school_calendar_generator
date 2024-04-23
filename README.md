# 
    # Notion School Calendar Generator

    This project is a Tkinter app that connects to the Notion API to generate calendars for each of my classes. It uses a configuration file where all vacations, holidays, and other important dates are stored to create a complete file structure to organize the content of my courses. This allows the students and me to have a clear view of the upcoming events and deadlines.

    ## Preview
    ![](https://github.com/notion_school_calendar_generator/notion_calendar_generator.gif)

    ## Features

    - Provides two classes to create/update pages and databases using Notion API 
    - Provides a Tkinter GUI to edit the configuration file and generate the calendar according to it.
    - Generates a calendar for each class with all the important dates and deadlines.
    
    ## Usage

    1. Install the required dependencies by running `pip install -r requirements.txt`.
    2. Create a '.env' file at the root of the project with the following variables:
        'NOTION_API_KEY' = 'YOUR_NOTION_API_KEY'
        'ADMIN_NAME' = 'YOUR_NAME"
        'ADMIN_SURNAME' = 'YOUR_SURNAME'
        'ADMIN_EMAIL' = 'YOUR_EMAIL'

    3. Launch the app by running `python notion-calendar.py`.
    4. Fill in the configuration file with the necessary information.
    5. Paste the ID of the Notion page where you want to create the calendar.
    5. Click on the 'Generate Calendar' button to create the calendar for each class.
    6. The app will create a folder for each class with the necessary pages and databases.
    7. Go to Notion and check the new pages and databases created.
