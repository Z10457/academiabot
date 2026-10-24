from datetime import date

assignments = {}

def add_assignment(course: str, assignment_name:str , due_date: str):
    """Add an assignment with its course , title and due date."""
    try:
        date.isocalendar(due_date)
    except ValueError: 
        raise ValueError("Due date must be in YYYY-MM-DD format.")

    assignment_id = len(assignments) + 1
    assignments[assignment_id] = {
        "id": assignment_id,
        "course": course, 
        "due_date": due_date,
        "assignment_name": assignment_name,
        "completed": False,
    }

    return {
        "Success": True,
        "assignment_id": assignments[assignment_id],
    }