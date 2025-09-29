# note-keeper-168290-168308

Notes Backend (Flask) - RESTful CRUD API

Quick start:
- Run: `python run.py` (Swagger UI at /docs)
- Health: GET `/` => {"message":"Healthy"}

Notes API:
- List: GET `/api/notes?page=1&page_size=20`
- Create: POST `/api/notes` body: {"title":"...", "content":"..."}
- Get: GET `/api/notes/{id}`
- Update: PATCH `/api/notes/{id}` body: {"title":"..."} or {"content":"..."}
- Delete: DELETE `/api/notes/{id}`

Responses follow an Ocean Professional envelope:
{ "status": "success|error", "data": <payload|null>, "message": "optional", "meta": { ...optional } }