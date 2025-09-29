"""
Marshmallow schemas for Notes API.

Schema responses are aligned with a modern, clean "Ocean Professional" style by using
consistent envelope fields: status, data, and meta where applicable.
"""
from marshmallow import Schema, fields, validate


class PaginationQuerySchema(Schema):
    page = fields.Int(load_default=1, metadata={"description": "Page number starting at 1"})
    page_size = fields.Int(load_default=20, validate=validate.Range(min=1, max=100), metadata={"description": "Items per page (1-100)"})


class NoteCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200), metadata={"description": "Title of the note"})
    content = fields.Str(required=True, validate=validate.Length(min=1), metadata={"description": "Content of the note"})


class NoteUpdateSchema(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=1, max=200), metadata={"description": "Updated title"})
    content = fields.Str(required=False, validate=validate.Length(min=1), metadata={"description": "Updated content"})


class NoteSchema(Schema):
    id = fields.Str(required=True, metadata={"description": "Note identifier (UUID)"})
    title = fields.Str(required=True, metadata={"description": "Title"})
    content = fields.Str(required=True, metadata={"description": "Content"})
    created_at = fields.Str(required=True, metadata={"description": "Creation timestamp (ISO8601)"})
    updated_at = fields.Str(required=True, metadata={"description": "Last update timestamp (ISO8601)"})


class EnvelopeSchema(Schema):
    status = fields.Str(required=True, metadata={"description": "Request status: success|error"})
    data = fields.Raw(required=False, allow_none=True, metadata={"description": "Payload"})
    message = fields.Str(required=False, allow_none=True, metadata={"description": "Human friendly message"})
    meta = fields.Dict(required=False, allow_none=True, metadata={"description": "Metadata like pagination"})
