"""Dash entry point: `uv run python app.py` (or `kiln dev`)."""

from dashboard.layout import create_app

app = create_app()
# WSGI server exposed for production (gunicorn app:server).
server = app.server

if __name__ == "__main__":
    app.run(debug=True)
