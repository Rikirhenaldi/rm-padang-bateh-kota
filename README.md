# RM Padang Bateh Kota

Django 5 monolithic restaurant website backed by JSON files. It does not use Django ORM, models, migrations, SQLite, or Django Admin.

## Local setup

Use Python 3.13 or newer. Copy `local_settings.py.sample` to `local_settings.py` and set local values. `local_settings.py` is ignored by git and replaces `.env` configuration.

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

The public site is at `/`; the custom dashboard is at `/dashboard/login/`.

## Storage

`STORAGE_BACKEND = "local"` reads and writes `data/` and `static/images/` directly. `STORAGE_BACKEND = "github"` reads and commits JSON/images through the GitHub Contents API. GitHub credentials are backend-only settings.

## Configuration

Supported `local_settings.py` values are documented in `local_settings.py.sample`: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `STORAGE_BACKEND`, `GITHUB_TOKEN`, `GITHUB_OWNER`, `GITHUB_REPOSITORY`, `GITHUB_BRANCH`, and `CSRF_TRUSTED_ORIGINS`.

## Deployment

Render uses `./build.sh` and `gunicorn config.wsgi:application`. The build only installs dependencies and runs `collectstatic`; it never runs migrations. Configure secrets in Render's environment settings. GitHub storage is required for durable production content because Render's filesystem is ephemeral.

## Menu provenance

The initial menu is transcribed from the public GoFood listing for RM Padang Bateh Kota:

`https://gofood.co.id/bandung/restaurant/rm-padang-bateh-kota-rajawali-samping-plaza-telkom-rajawali-322f1e2b-15ff-4305-b97c-73eb630896de`

The listing exposed the menu through its public structured data, including four menu sections, names, descriptions, and IDR prices. These records are marked `price_verified: true` and retain the source categories. GoFood exposed one restaurant image, not individual menu images. That image is referenced in `restaurant.json` and `gallery.json`; menu cards continue using the existing SVG plate illustrations until the restaurant owner uploads item-specific photos through the dashboard.
