from google import genai
from datetime import date
from pypdf import PdfReader
from pypdf.errors import PdfReadError


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

def add_syllabus(file_path:str): 
    try:
        reader = PdfReader(file_path)
        all_text = ""
        for page in reader.pages:
            all_text += page.extract_text() + "\n"
    except FileNotFoundError:
        return {"success": False, "message": "File not found"}

    except PdfReadError:
        return{"success": False, "message": "Invalid file"}

    if not all_text.strip(): #empty or whitespace only
        return{"success": False, "message": "File is empty"}

    
    return {"success" : True, "all_text": all_text }

#add more tools such as reading doc and not just pdf
#give them the option to combine the syllabuses, so the dates are stacked up.


