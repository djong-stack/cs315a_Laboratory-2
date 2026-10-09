# Running the project

This project is a Python 3.12 FastAPI library inventory API.

Use the **Start application** workflow (Replit's Run button). It runs:

```sh
cd exam_project && python -m uvicorn main:app --host 0.0.0.0 --port 5000
```

The working directory matters: local module imports and the SQLite database path
are relative to `exam_project`. Keep the existing directory structure.

- `/`: API status and docs link.
- `/docs`: interactive Swagger documentation for trying requests.
- `/categories/`: create and list categories.
- `/books/`: create, list, and filter books by category.
- `/books/{book_id}`: retrieve, update, and delete books.

Dependencies are managed in the root `pyproject.toml` and `uv.lock`.
No secrets or external services are required. Data is stored in
`exam_project/library.db`; do not delete it when restarting the app.
