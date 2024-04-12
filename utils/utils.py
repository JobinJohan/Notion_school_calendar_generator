import datetime

def day_to_value(day: str) -> int:
    """Convert a day to a value"""
    match day:
        case "lundi":
            return 0
        case "mardi":
            return 1
        case "mercredi":
            return 2
        case "jeudi":
            return 3
        case "vendredi":
            return 4
        case "samedi":
            return 5
        case "dimanche":
            return 6
        case _:
            return -1
        
def date_to_course_duration(holidays_dict: dict, date_course, start_course, end_course) -> str:
    """Convert a date to a course duration"""

    # Check if the date is a holiday
    if date_is_holiday(holidays_dict, date_course)[0]:
        return "-"
        
    # Check if the course takes place during more than 60 minutes (15 minutes margin)
    start_course_time = datetime.datetime.strptime(start_course, "%H:%M")
    end_course_time = datetime.datetime.strptime(end_course, "%H:%M")

    if (end_course_time - start_course_time).seconds >= 3000:
        return "2 périodes complètes"
    else:
        return "1 période complète"
    

def date_is_holiday(holidays_dict: dict, date) -> tuple:
    """Check if a date is a holiday"""

    date = datetime.datetime.strptime(date, "%Y-%m-%d")

    # Check if the date is a holiday
    for vacance in holidays_dict["vacances"]:
    
        date_debut = datetime.datetime.strptime(holidays_dict["vacances"][vacance]["date_debut"], "%Y-%m-%d")
        date_fin = datetime.datetime.strptime(holidays_dict["vacances"][vacance]["date_fin"], "%Y-%m-%d")

        if date >= date_debut and date <= date_fin:
            return (True, ["⛱ Vacances"])
        
    # Check if the date is a public holiday
    for day_off in holidays_dict["jours_feries"]:
        date_debut = datetime.datetime.strptime(holidays_dict["jours_feries"][day_off]["date_debut"], "%Y-%m-%d")
        date_fin = datetime.datetime.strptime(holidays_dict["jours_feries"][day_off]["date_fin"], "%Y-%m-%d")

        if date >= date_debut and date <= date_fin:
            return (True, ["⛱ Jour férié"])
        
    return (False, ["📒 Leçon"])
