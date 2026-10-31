"""Dash entry point: `uv run python app.py` (or `ion repo dev`)."""

from dashboard.layout import create_app

app = create_app()
# WSGI server exposed for production (gunicorn app:server).
server = app.server

if __name__ == "__main__":
    app.run(debug=True)
