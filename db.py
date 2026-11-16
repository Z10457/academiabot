def assignment_exists(client, course, assignment_name, due_date):  # client = the logged-in Supabase client; the rest describe one assignment
    result = (  # parentheses let one long chain of calls span several lines
        client.table("assignments")  
        .select("id")  # we only need to know whether a row exists, so fetch just the id column
        .eq("course", course)  # .eq means "equals": keeps rows whose course column matches
        .eq("assignment_name", assignment_name)  
        .eq("due_date", due_date)  # all three must match, so this is an exact-duplicate check
        .limit(1)  # stop looking after the first match; one is enough to know it exists
        .execute()  # sends the request; until this line, you were only describing the query
    )
    return len(result.data) > 0  


def add_assignment_row(client, course, assignment_name, due_date):
    client.table("assignments").insert({ 
        "course": course,  # column name on the left in quotes, your variable on the right with no quotes
        "assignment_name": assignment_name,
        "due_date": due_date,  # Supabase expects YYYY-MM-DD text here and turns it into a real date
    }).execute()  # user_id is missing on purpose: the database fills it from the login


def list_assignment_rows(client, course=""):  # course="" means the filter is optional, like in your old list_assignments
    result = (
        client.table("assignments")
        .select("id, course, assignment_name, due_date, completed")  # the columns to fetch, separated by commas
        .order("due_date")  
    )
    rows = result.data  # a list of dicts, one per assignment, and only the logged-in user's rows come back
    if course:  # only filter when a course was given
        rows = [r for r in rows if r["course"].lower() == course.lower()]  
    return rows  # hand the list back; the tools will wrap it in a success dict