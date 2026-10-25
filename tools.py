from google import genai
from datetime import date

assignment_list = []

def add_assignment(course:str, assignment_name:str, due_date:str ):
    try: 
        parsed = date.fromisoformat(due_date)
    except ValueError: 
        return ValueError("Invalid date format, please use YYYY-MM-DD")
    item = {"due_date": due_date, "course": course, "assignment_name": assignment_name}
    assignment_list.append(item)

    return ({"success": True, "assignment": item})

print(add_assignment("Calc", "Exam 1", "2026-11-12"))
print(add_assignment("Calc", "Exam 1", "11/12/2026"))
print(add_assignment("Calc", "Exam 1", "2026-01-12"))
print(assignment_list)

 #modify the code so when you print the list, the assignments are in order of due dates. makes it easier for student. 

