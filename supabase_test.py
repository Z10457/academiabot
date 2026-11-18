from getpass import getpass
from db import client, add_assignment_row, list_assignment_rows, assignment_exists

email = input("Test user email: ")  # you type it when the script runs, so it never sits in a file
password = getpass("Test user password: ")  # same, but hidden while you type

result = client.auth.sign_in_with_password({"email": email, "password": password})  # logs in; from now on the client attaches this user's login token to every request, which is how the database knows who you are
print("Logged in as:", result.user.email)  # proof that the login worked

client.table("assignments").insert({"course": "Test", "assignment_name": "Test quiz", "due_date": "2026-11-20"}).execute()  

rows = client.table("assignments").select("*").execute()  
print(rows.data)  # a list of dicts, one per row; RLS means you only get YOUR rows

print(assignment_exists(client, "Calc", "Exam 1", "2026-11-12"))  # expect False
add_assignment_row(client, "Calc", "Exam 1", "2026-11-12")
print(assignment_exists(client, "Calc", "Exam 1", "2026-11-12"))  # expect True
print(list_assignment_rows(client))  # expect your Calc exam
print(list_assignment_rows(client, "calc"))  # expect the same one, since case is ignored
print(list_assignment_rows(client, "Bio"))  # expect an empty list

client.auth.sign_out()  # logs out and closes things down properly

print(client.table("assignments").select("*").execute().data)  # now logged out: expect an empty list or a permission error, which proves the table is locked to strangers

