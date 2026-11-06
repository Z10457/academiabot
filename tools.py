import json
from datetime import date
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import os
from docx import Document 
from docx.opc.exceptions import PackageNotFoundError
 

FILE = "assignments.json"


def add_assignment(course:str, assignment_name:str, due_date:str ):

    """Save one assignment with its course, name, and due date.

    Use this when the user mentions a deadline, or after reading a syllabus,
    once for every assignment and exam found. If the date is relative, such
    as "next Friday", work out the real date from today's date first.

    Args:
        course: The course name or code, e.g. "Calc 2".
        assignment_name: The assignment or exam name, e.g. "Exam 1".
        due_date: The due date in YYYY-MM-DD format, e.g. "2026-11-12".
     """
        
    try: 
        parsed = date.fromisoformat(due_date)
    except ValueError: 
        return {"success": False, "message": "Invalid date format, please use YYYY-MM-DD"}
    item = {"due_date": due_date, "course": course, "assignment_name": assignment_name}
    assignment_list.append(item)

    save_assignment()
    return ({"success": True, "assignment": item})

 

def read_pdf(file_path:str): 
    reader = PdfReader(file_path)
    all_text = ""
    for page in reader.pages:
        all_text += page.extract_text() + "\n"
    return all_text

    

def read_docx(file_path:str):
    doc = Document(file_path)
    doc_text = ""

    for paragraph in doc.paragraphs:
        doc_text += paragraph.text + "\n"

    for table in doc.tables: 
        for row in table.rows :
            cells = [cell.text for cell in row.cells]
            doc_text += " | ".join(cells) + "\n"
    return doc_text 


def read_syllabus(file_path:str):

    """Read a syllabus file and return its text. This does not save anything.

    Use this when the user gives a file path to their syllabus. Afterwards,
    find every assignment and exam in the text and save each one with
    add_assignment. Supports PDF and Word (.docx) files only.

    Args:
        file_path: The full path to the syllabus file on the user's computer.
    """
    if not os.path.exists(file_path):
        return{"success": False, "message": "File not found."}
    ext = os.path.splitext(file_path)[1].lower()
    try: 
        if ext == ".pdf":
            text = read_pdf(file_path)
        elif ext == ".docx":
            text = read_docx(file_path)
        else:
            return{"success":False, "message": "Please upload a PDF or a Word Doc"}


    except PdfReadError:
        return{"success": False, "message": "Invalid file"}
    except PackageNotFoundError:
        return{"success": False, "message": "The word file could not be read."}
        
    if not text.strip(): #empty or whitespace only
        return{"success": False, "message": "File is empty"}

        
    return {"success" : True, "text": text }

    #add more tools such as reading doc and not just pdf
    #give them the option to combine the syllabuses, so the dates are stacked up.


def list_assignments(course:str = ""):
    """Return the saved assignments, sorted by due date with the soonest first.

    Use this when the user asks what is due, what is coming up, or wants to
    see their assignments.

    Args:
        course: Optional. If given, only return assignments for this course.
    """
    results = assignment_list
    if course:
        results = [assignment for assignment in assignment_list if assignment["course"] == course]

    if not results:
        return{"success": True, "assignment_list":[], "message": "No assignment has been saved yet."}

    return{"success": True, "assignment_list": sorted(results, key=lambda assignment: assignment["due_date"])}


import json

def load_assignment():

    if not os.path.exists(FILE):
        return []
    with open(FILE) as f:
        return json.load(f)
    
    
def save_assignment():
    with open(FILE, "w") as f:
        json.dump(assignment_list, f, indent = 2)

assignment_list = load_assignment()


def calculate_average(grades):
	
    total = sum(grades)
    count = len(grades)
    average = total/count
    return (average)

GRADE_SCALE = [
    (93, 'A',  4.00),
    (90, 'A-', 3.67),
    (87, 'B+', 3.33),
    (83, 'B',  3.00),
    (80, 'B-', 2.67),
    (77, 'C+', 2.33),
    (73, 'C',  2.00),
    (70, 'C-', 1.67),
    (60, 'D',  1.00),
]

def get_letter_grade(average):
    for cutoff, letter,gpa  in GRADE_SCALE:
        if average >= cutoff:
            return letter,gpa
        
    return 'F', 0.00




