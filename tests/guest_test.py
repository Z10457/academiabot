from db import new_client
from tools import make_tools

client = new_client()
client.auth.sign_in_anonymously()

add_assignment , list_assignments, read_syllabus, search_papers = make_tools(client)

print(list_assignments)
print(add_assignment("Test", "Quiz 1", "2026-12-01"))
print (read_syllabus)

client.auth.sign_out()

