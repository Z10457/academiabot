from google import genai
from datetime import date

today = date.today()
print(today)

assignment_list = []

def add_assignment(course:str, assignment_name:str, due_date:str ):
    try: 
        parsed = date.fromisoformat(due_date)
    except ValueError: 
        return {"success": False, "message": "Invalid date format, please use YYYY-MM-DD"}
    item = {"due_date": due_date, "course": course, "assignment_name": assignment_name}
    assignment_list.append(item)

    return ({"success": True, "assignment": item})


 #modify the code so when you print the list, the assignments are in order of due dates. makes it easier for student. 

