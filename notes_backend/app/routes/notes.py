from flask_smorest import Blueprint
from flask.views import MethodView

from http import HTTPStatus

from ..models import InMemoryNotesRepository, NotesRepository
from ..schemas import (
    PaginationQuerySchema,
    NoteCreateSchema,
    NoteUpdateSchema,
    NoteSchema,
    EnvelopeSchema,
)

# Notes blueprint with Ocean Professional style and OpenAPI tags
blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/api/notes",
    description="CRUD endpoints to manage notes with a modern, clean API design.",
)

# Repository instance
# In a production setting, replace with an adapter using `notes_database`
repo: NotesRepository = InMemoryNotesRepository()


@blp.route("/")
class NotesCollection(MethodView):
    """
    Notes collection endpoints.

    GET: List notes with pagination
    POST: Create a new note
    """

    @blp.arguments(PaginationQuerySchema, location="query")
    @blp.response(HTTPStatus.OK, EnvelopeSchema, description="List all notes with pagination", example={
        "status": "success",
        "data": {
            "items": [
                {
                    "id": "uuid",
                    "title": "Sample",
                    "content": "Content",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                }
            ],
            "meta": {
                "total": 1,
                "total_pages": 1,
                "first_page": 1,
                "last_page": 1,
                "page": 1,
                "previous_page": None,
                "next_page": None,
            },
        },
        "message": "Notes fetched",
    })
    def get(self, args):
        """
        List notes with pagination.

        Query Parameters:
          - page: integer, default 1
          - page_size: integer, default 20

        Returns:
          200 OK with an envelope {status, data: {items, meta}, message}
        """
        page = args.get("page", 1)
        page_size = args.get("page_size", 20)
        result = repo.list(page=page, page_size=page_size)
        items = [NoteSchema().dump(n) for n in result["items"]]
        return {
            "status": "success",
            "data": {"items": items, "meta": result["meta"]},
            "message": "Notes fetched",
        }, HTTPStatus.OK

    @blp.arguments(NoteCreateSchema)
    @blp.response(HTTPStatus.CREATED, EnvelopeSchema, description="Create a new note", example={
        "status": "success",
        "data": {
            "id": "uuid",
            "title": "New",
            "content": "Body",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        },
        "message": "Note created",
    })
    def post(self, payload):
        """
        Create a new note.

        Request Body:
          - title: string (1..200)
          - content: string (>=1)

        Returns:
          201 Created with envelope {status, data: note, message}
        """
        note = repo.create(title=payload["title"], content=payload["content"])
        return {
            "status": "success",
            "data": NoteSchema().dump(note),
            "message": "Note created",
        }, HTTPStatus.CREATED


@blp.route("/<string:note_id>")
class NoteItem(MethodView):
    """
    Single note endpoints.

    GET: Retrieve a note by id
    PATCH: Update note fields
    DELETE: Remove a note
    """

    @blp.response(HTTPStatus.OK, EnvelopeSchema, description="Get a note by id")
    def get(self, note_id: str):
        """
        Retrieve a note by id.

        Path Parameters:
          - note_id: UUID string

        Returns:
          200 OK with envelope {status, data: note}
          404 Not Found if not exists
        """
        note = repo.get(note_id)
        if not note:
            return {
                "status": "error",
                "data": None,
                "message": "Note not found",
            }, HTTPStatus.NOT_FOUND
        return {"status": "success", "data": NoteSchema().dump(note)}, HTTPStatus.OK

    @blp.arguments(NoteUpdateSchema)
    @blp.response(HTTPStatus.OK, EnvelopeSchema, description="Update a note by id")
    def patch(self, payload, note_id: str):
        """
        Update fields of a note.

        Path Parameters:
          - note_id: UUID string

        Request Body (any of):
          - title: string
          - content: string

        Returns:
          200 OK with envelope {status, data: note, message}
          404 Not Found if not exists
        """
        if not payload:
            return {
                "status": "error",
                "data": None,
                "message": "No fields provided for update",
            }, HTTPStatus.BAD_REQUEST

        updated = repo.update(note_id, title=payload.get("title"), content=payload.get("content"))
        if not updated:
            return {
                "status": "error",
                "data": None,
                "message": "Note not found",
            }, HTTPStatus.NOT_FOUND

        return {
            "status": "success",
            "data": NoteSchema().dump(updated),
            "message": "Note updated",
        }, HTTPStatus.OK

    @blp.response(HTTPStatus.NO_CONTENT, description="Delete a note by id")
    def delete(self, note_id: str):
        """
        Delete a note by id.

        Path Parameters:
          - note_id: UUID string

        Returns:
          204 No Content on success
          404 Not Found if not exists
        """
        deleted = repo.delete(note_id)
        if not deleted:
            return {
                "status": "error",
                "data": None,
                "message": "Note not found",
            }, HTTPStatus.NOT_FOUND
        # For 204, return empty body
        return "", HTTPStatus.NO_CONTENT
