from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    """Fields shared between note creation requests and full note representation."""
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10_000)


class NoteCreate(NoteBase):
    """Shape of the data a client sends to create a new note.

    Server-generated fields (id, created_at, updated_at) are deliberately
    excluded — clients don't get to set those.
    """
    pass


class Note(NoteBase):
    """Full representation of a note, including server-generated fields.

    `from_attributes=True` allows construction from ORM objects in addition to dicts.
    """
    # Pydantic config is replaced (not merged) on inheritance, so we restate
    # extra="forbid" alongside from_attributes=True.
    model_config = ConfigDict(extra="forbid", from_attributes=True)
   

    id: int
    created_at: datetime
    updated_at: datetime