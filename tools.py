from google import genai
from datetime import date
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import os
from docx import Document 
from docx.opc.exceptions import PackageNotFoundError
 


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


def add_syllabus(file_path:str):
    """
When the user uploads their syllabus, first check whether they uploaded it.
That is where the `if not os.path...` line comes in.

Then, if they uploaded it, check whether it is a PDF or DOC/DOCX file.
If it is neither, ask them to upload it in one of those formats.

If the file is invalid or could not be read, return an appropriate error message.
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


