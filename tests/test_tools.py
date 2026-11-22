from getpass import getpass  # asks for a password without echoing it
from db import new_client  # makes a fresh, not-yet-logged-in client
from tools import make_tools  # the builder you just wrote

client = new_client()  # a client owned by this script only
email = input("Test user email: ")  # typed at run time, never stored in the file
password = getpass("Test user password: ")  # hidden while you type
client.auth.sign_in_with_password({"email": email, "password": password})  # logs in; this client now carries the user's login

add_assignment, list_assignments, read_syllabus, search_papers = make_tools(client)  # unpacks the returned list; the order must match the return line in make_tools

print(list_assignments())  # a clean table: expect an empty list with the "No assignments" message
print(add_assignment("Calc", "Exam 1", "2026-11-12"))  # expect success
print(add_assignment("Calc", "Exam 1", "2026-11-12"))  # the same again: expect "already exists"
print(add_assignment("Calc", "Quiz", "11/12/2026"))  # wrong format: expect the YYYY-MM-DD message
print(list_assignments())  # expect one Calc exam
print(list_assignments("calc"))  # lowercase filter: expect the same one

client.auth.sign_out()  # log out when finished