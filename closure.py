notes = []

def make_tools(owner):
    def add_notes(text:str):
        """Save a note."""
        notes.append({"owner":owner, "text": text})
        return ({"success": True})

    def list_notes():
        """Return notes."""
        my_notes = [n for n in notes if n["owner"] == owner]
        return ({"success": True, "owner": owner, "notes": my_notes})

    return [add_notes, list_notes]

A_tools = make_tools("A")
Zee_tools = make_tools("Zee")
    

