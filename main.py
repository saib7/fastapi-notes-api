from datetime import datetime, timezone

from fastapi import FastAPI, status

from models import Note, NoteCreate

app = FastAPI(title="Notes API", version="0.1.0")

# TODO: Replace with database-generated IDs. The current approach is not
#   safe across multiple server instances, and is only race-free here
#   because the handlers are `async def` (running on a single event loop).
notes_db: list[Note] = []
next_id: int = 1


@app.get("/notes", response_model=list[Note])
async def list_notes() -> list[Note]:
    """Return all notes currently stored."""
    return notes_db


@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note_in: NoteCreate) -> Note:
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
