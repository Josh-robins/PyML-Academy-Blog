# Django Blog

A simple blog application built with Django 6. Users can view a list of posts on the homepage and click through to read the full post on a dedicated detail page.

---

## Features

- Post list homepage — shows title, author, date, and a truncated preview
- Post detail page — shows the full post content
- Auto-timestamped posts (`created_at`)
- Django admin support for managing posts
- 18 automated tests covering URLs, views, templates, and models

---

## Project Structure

```
blog/                       # Django project root
├── blog/                   # Main app
│   ├── migrations/         # Database migrations
│   ├── admin.py            # Admin registration
│   ├── models.py           # Post model
│   ├── urls.py             # App URL patterns
│   ├── views.py            # ListView + DetailView
│   └── tests.py            # All test cases
├── django_project/         # Project settings & root URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/              # HTML templates
│   ├── base.html           # Master layout
│   ├── home.html           # Post list page
│   └── post_detail.html    # Post detail page
├── static/                 # Static files (CSS, JS, images)
├── manage.py
├── requirements.txt
└── .gitignore
```

---

## Prerequisites

- Python 3.10+
- Git

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd blog
```

### 2. Create and activate a virtual environment

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (for the admin panel)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## URLs

| URL | View | Description |
|-----|------|-------------|
| `/` | `BlogView` | Homepage — list of all posts |
| `/post/<pk>/` | `PostDetailView` | Full post detail page |
| `/admin/` | Django Admin | Create, edit, delete posts and users |

---

## Data Model

### `Post`

| Field | Type | Description |
|-------|------|-------------|
| `title` | `CharField(200)` | Title of the post |
| `author` | `ForeignKey(User)` | Linked to Django's built-in `auth.User` |
| `body` | `TextField` | Full post content |
| `created_at` | `DateTimeField` | Auto-set when the post is created |

---

## Running Tests

```bash
python manage.py test blog
```

For verbose output (see each test name):

```bash
python manage.py test blog --verbosity=2
```

### Test Coverage

| Test Class | What it tests |
|---|---|
| `PostModelTest` | Model `__str__`, `created_at`, `get_absolute_url` |
| `HomePageURLTest` | `/` URL, `'home'` name, view, template, content |
| `PostDetailURLTest` | `/post/<pk>/` URL, `'post-detail'` name, view, template, content, 404 |

---

## Contributing

Contributions are welcome! Follow these steps:

### 1. Fork the repository

Click **Fork** on GitHub to create your own copy.

### 2. Create a feature branch

```bash
git checkout -b feature/your-feature-name
```

Use a descriptive branch name, e.g. `feature/add-comments`, `fix/detail-page-404`.

### 3. Make your changes

- Follow the existing code style
- Keep views class-based where possible
- Add templates to `templates/`
- Add static files to `static/`

### 4. Write tests

All new features must include tests in `blog/tests.py`. Run the full suite before submitting:

```bash
python manage.py test blog --verbosity=2
```

All 18 existing tests must still pass.

### 5. Commit your changes

```bash
git add .
git commit -m "feat: short description of your change"
```

Commit message conventions:
- `feat:` — new feature
- `fix:` — bug fix
- `refactor:` — code change with no behaviour change
- `test:` — adding or updating tests
- `docs:` — documentation only

### 6. Push and open a Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with a clear description of what you changed and why.

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 6.0.3 | Web framework |
| asgiref | 3.11.1 | ASGI support (required by Django) |
| sqlparse | 0.5.5 | SQL formatting (required by Django) |
| tzdata | 2025.3 | Timezone data |

---

## License

This project is open source. Feel free to use it as a learning resource or starting point for your own Django projects.
