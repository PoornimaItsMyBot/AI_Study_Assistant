class NoteManager:
    def __init__(self):
        self.notes = []
        self.next_id = 1

    def create_note(self, title, content, subject=None):
        note = {
            "id": self.next_id,
            "title": title,
            "content": content,
            "subject": subject
        }
        self.notes.append(note)
        self.next_id += 1
        return note

    def get_notes(self):
        return self.notes

    def delete_note(self, note_id):
        for note in self.notes:
            if note["id"] == note_id:
                self.notes.remove(note)
                return True
        return False

    def update_note(self, note_id, title=None, content=None, subject=None):
        for note in self.notes:
            if note["id"] == note_id:
                if title is not None:
                    note["title"] = title
                if content is not None:
                    note["content"] = content
                if subject is not None:
                    note["subject"] = subject
                return True
        return False