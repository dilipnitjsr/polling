# Polling

A small Django polling application with question creation, voting, results, and a JSON vote-count API.

## Security note

Historical revisions contained a Django secret key and PostgreSQL credentials in source code. Treat those historical credentials as compromised and rotate/revoke them before any production deployment.

The current application reads deployment configuration from environment variables and defaults to SQLite for local development.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Required production configuration:

- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL` for PostgreSQL
- `DJANGO_DEBUG=false`

## Tests

```bash
python manage.py test
```

## Important behavioral fix

Older revisions started an infinite random-voting background thread while importing URL configuration. That code has been removed. Importing or starting the web application no longer mutates poll results.

Voting uses an atomic database increment to avoid lost updates under concurrent requests.

## API

```text
GET /polls/api/?question_id=<id>
```

returns the question text and current choice vote counts.
