"""
Models and repository abstraction for Notes.

This module defines:
- Note data model for internal use
- NotesRepository interface (PUBLIC_INTERFACE) to abstract persistence (assumed to be provided by `notes_database`)
- InMemoryNotesRepository fallback for local preview/testing

The repository uses simple dict-based storage for preview. Replace InMemoryNotesRepository with an adapter to `notes_database` for production.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List
import uuid


@dataclass
class Note:
    """
    Internal Note representation.

    Fields:
      - id: Unique identifier (UUID string)
      - title: Title of the note
      - content: Body content of the note
      - created_at: ISO timestamp when note was created
      - updated_at: ISO timestamp when note was last updated
    """
    id: str
    title: str
    content: str
    created_at: str
    updated_at: str

    @staticmethod
    def now_iso() -> str:
        return datetime.utcnow().isoformat() + "Z"

    @classmethod
    def new(cls, title: str, content: str) -> "Note":
        now = cls.now_iso()
        return cls(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            created_at=now,
            updated_at=now,
        )


class NotesRepository:
    # PUBLIC_INTERFACE
    def list(self, page: int = 1, page_size: int = 20) -> Dict[str, object]:
        """
        PUBLIC_INTERFACE
        List notes with basic pagination.

        Parameters:
          - page: Page number starting at 1
          - page_size: Number of items per page

        Returns:
          dict with 'items': List[Note], and 'meta': pagination metadata.
        """
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def get(self, note_id: str) -> Optional[Note]:
        """
        PUBLIC_INTERFACE
        Retrieve a single note by id.

        Parameters:
          - note_id: UUID string

        Returns:
          Note or None if not found.
        """
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def create(self, title: str, content: str) -> Note:
        """
        PUBLIC_INTERFACE
        Create a new note.

        Parameters:
          - title: Title string
          - content: Content string

        Returns:
          The created Note.
        """
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def update(self, note_id: str, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Note]:
        """
        PUBLIC_INTERFACE
        Update fields of a note.

        Parameters:
          - note_id: UUID string
          - title: Optional new title
          - content: Optional new content

        Returns:
          Updated Note or None if not found.
        """
        raise NotImplementedError

    # PUBLIC_INTERFACE
    def delete(self, note_id: str) -> bool:
        """
        PUBLIC_INTERFACE
        Delete a note by id.

        Parameters:
          - note_id: UUID string

        Returns:
          True if deleted, False if not found.
        """
        raise NotImplementedError


class InMemoryNotesRepository(NotesRepository):
    """
    Simple in-memory repository to enable preview/testing without an external DB.
    Replace with an adapter to `notes_database` in production.
    """

    def __init__(self) -> None:
        self._data: Dict[str, Note] = {}

    def list(self, page: int = 1, page_size: int = 20) -> Dict[str, object]:
        items: List[Note] = list(self._data.values())
        total = len(items)
        start = (page - 1) * page_size
        end = start + page_size
        page_items = items[start:end]
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 1
        meta = {
            "total": total,
            "total_pages": total_pages,
            "first_page": 1 if total > 0 else 0,
            "last_page": total_pages if total > 0 else 0,
            "page": page,
            "previous_page": page - 1 if page > 1 else None,
            "next_page": page + 1 if page < total_pages else None,
        }
        return {"items": page_items, "meta": meta}

    def get(self, note_id: str) -> Optional[Note]:
        return self._data.get(note_id)

    def create(self, title: str, content: str) -> Note:
        note = Note.new(title=title, content=content)
        self._data[note.id] = note
        return note

    def update(self, note_id: str, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Note]:
        note = self._data.get(note_id)
        if not note:
            return None
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        note.updated_at = Note.now_iso()
        self._data[note_id] = note
        return note

    def delete(self, note_id: str) -> bool:
        if note_id in self._data:
            del self._data[note_id]
            return True
        return False
