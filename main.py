from datetime import datetime, timezone

from fastapi import FastAPI

from models import Note, NoteCreate

app = FastAPI(title="Notes API", version="0.1.0")

# In-memory storage. Will be replaced with a database in a future PR.
# TODO: Replace with database-generated IDs. Current approach is not safe
#   under concurrent requests or multiple server instances.
notes_db: list[Note] = []
next_id: int = 1


@app.get("/notes", response_model=list[Note])
def list_notes() -> list[Note]:
    """Return all notes currently stored."""
    return notes_db


@app.post("/notes", response_model=Note, status_code=201)
def create_note(note_in: NoteCreate) -> Note:
    """Create a new note from the provided title and content."""
    global next_id
    now = datetime.now(timezone.utc)
    new_note = Note(
        id=next_id,
        title=note_in.title,
        content=note_in.content,
        created_at=now,
        updated_at=now,
    )
    notes_db.append(new_note)
    next_id += 1
    return new_note
