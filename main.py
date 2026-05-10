from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status

from models import Note, NoteCreate

app = FastAPI(title="Notes API", version="0.1.0")

# TODO: Replace with database-generated IDs. The current approach is not
#   safe across multiple server instances, and is only race-free here
#   because the handlers are `async def` (running on a single event loop).
notes_db: list[Note] = []
next_id: int = 1


# helper function to find a note by ID
def find_note_by_id(note_id: int) -> Note | None:
    """Return the note with the given id, or None if not found."""
    for note in notes_db:
        if note.id == note_id:
            return note
    return None


@app.get("/notes", response_model=list[Note])
async def list_notes() -> list[Note]:
    """Return all notes currently stored."""
    return notes_db


@app.get("/notes/{note_id}", response_model=Note)
async def get_note(note_id: int) -> Note:
    """Return the note with the given id, or 404 if not found."""
    note = find_note_by_id(note_id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )
    return note


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


@app.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, note_in: NoteCreate) -> Note:
    """Replace an existing note's title and content. Returns 404 if not found."""
    existing = find_note_by_id(note_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )
    existing.title = note_in.title
    existing.content = note_in.content
    existing.updated_at = datetime.now(timezone.utc)
    return existing


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int) -> None:
    """Delete the note with the given id. Returns 404 if not found."""
    existing = find_note_by_id(note_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found",
        )
    notes_db.remove(existing)
    return None
