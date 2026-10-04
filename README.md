# Developer Portfolio

A Django portfolio site with an editable profile, project case studies, and a
contact form. The included demo content lets you preview the site before adding
your own details.

## Requirements

- Python 3.10 or newer
- Git, if you want to clone the repository from GitHub

## Run locally

### 1. Get the project

Clone the repository and change into its folder:

```bash
git clone https://github.com/skm08/Portfolio-website-with-Django.git
cd Portfolio-website-with-Django
```

Alternatively, download and extract the repository ZIP, then open a terminal
in the extracted project folder.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

**macOS or Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies and prepare the database

With the virtual environment activated:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
```

The `seed_demo` command adds a sample profile and four sample projects. It is
safe to run again: existing demo entries are kept, and the command refuses to
mix demo content into a database that already has a non-demo profile or
projects.

### 4. Start the development server

```bash
python manage.py runserver
```

Open these addresses in your browser:

- Portfolio: <http://127.0.0.1:8000/>
- Project list: <http://127.0.0.1:8000/projects/>
- Contact form: <http://127.0.0.1:8000/contact/>
- Django admin: <http://127.0.0.1:8000/admin/>

Stop the server with `Ctrl+C` in the terminal.

## Edit the portfolio content

Create an admin account:

```bash
python manage.py createsuperuser
```

Sign in at <http://127.0.0.1:8000/admin/>. Update the sample **Site profile**
with your name, headline, biography, email, and social links. Edit, publish, or
remove the sample **Projects** and add your own case studies. The homepage
shows featured published projects; the Projects page shows all published
projects. Contact form submissions are saved under **Contact messages** in
the admin.

The demo identity and project descriptions are fictional examples. Replace
them before presenting the website as your own.

## Useful development commands

Run the automated tests and Django configuration checks:

```bash
python manage.py test
python manage.py check
```

After changing a model, generate and apply its database migration:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Troubleshooting

- **`python` is not recognized on Windows:** use `py` in place of `python`, or
  install Python and enable the option to add it to `PATH`.
- **The virtual environment is not active:** activate `.venv` again in the
  terminal where you run Django commands.
- **Port 8000 is already in use:** start the server on another port, for
  example `python manage.py runserver 8001`.
- **Changes do not appear:** refresh the browser. The Django development server
  reloads Python changes automatically; if needed, stop it with `Ctrl+C` and
  start it again.

## Production deployment

The settings in this project are configured for local development by default.
Before deploying, set `DJANGO_SECRET_KEY` to a long random secret,
`DJANGO_DEBUG=false`, and `DJANGO_ALLOWED_HOSTS` to your production hostname(s).
Debug-disabled settings enable HTTPS redirects, secure session and CSRF
cookies, and HSTS. Configure HTTPS and static-file serving on the hosting
platform, then run:

```bash
python manage.py migrate
python manage.py collectstatic
```

SQLite is used locally. Select and configure a production database, backups,
and any trusted-proxy security settings for your host before deployment. Never
use the development server as a production web server.
