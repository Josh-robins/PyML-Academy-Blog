# Django Blog

A full-featured blog application built with Django 6. Authenticated users can create, edit, and delete posts. Visitors can sign up or log in to participate. Static files are served in both development and production via WhiteNoise.

---

## Features

- **Post list homepage** — shows title, author, date, and a truncated body preview
- **Post detail page** — shows the full post content with edit/delete actions
- **Create, edit, and delete posts** — class-based views with form validation
- **User authentication** — login, logout, and sign-up with Django's built-in auth system
- **Time-aware greeting** — homepage greets logged-in users with "Good morning / afternoon / evening"
- **Responsive navbar** — shows Login + Sign up when logged out; New Post + Log out when logged in
- **Custom 404 page** — friendly error page for missing routes
- **Auto-timestamps** — `created_at` and `updated_at` fields on every post
- **WhiteNoise static file serving** — CSS served correctly with `DEBUG = False`
- **Django admin** — full post and user management
- **52 automated tests** — covering models, URLs, views, templates, CRUD, auth, and 404 handling

---

## Project Structure

```
blog/                           # Django project root
├── blog/                       # Main blog app
│   ├── migrations/             # Database migrations
│   ├── admin.py                # Admin registration
│   ├── models.py               # Post model
│   ├── urls.py                 # App URL patterns
│   ├── views.py                # ListView, DetailView, CreateView, UpdateView, DeleteView
    └── tests.py                # All 52 test cases
├── django_project/             # Project settings & root URLs
│   ├── settings.py             # WhiteNoise, static files, auth config
│   ├── urls.py                 # Root URL conf with auth + accounts routes
│   ├── views.py                # Custom 404 handler
│   └── wsgi.py
├── templates/                  # HTML templates
│   ├── base.html               # Master layout with navbar
│   ├── home.html               # Post list + time-aware greeting
│   ├── post_detail.html        # Full post with edit/delete buttons
│   ├── post_new.html           # Create post form
│   ├── post_edit.html          # Edit post form
│   ├── post_delete.html        # Delete confirmation
│   ├── 404.html                # Custom 404 page
│   └── registration/
│       ├── login.html          # Login form
│       └── signup.html         # Sign-up form
├── static/css/
│   └── base.css                # Site-wide styles
├── staticfiles/                # Collected static files (WhiteNoise)
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

### 5. Collect static files

```bash
python manage.py collectstatic
```

### 6. Create a superuser (for the admin panel)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## URLs

| URL | View | Description |
|-----|------|-------------|
| `/` | `BlogView` | Homepage — list of all posts |
| `/post/new/` | `PostCreateView` | Create a new post |
| `/post/<pk>/` | `PostDetailView` | Full post detail page |
| `/post/<pk>/edit/` | `PostUpdateView` | Edit an existing post |
| `/post/<pk>/delete/` | `PostDeleteView` | Delete a post (with confirmation) |
| `/accounts/login/` | Django `LoginView` | Login page |
| `/accounts/logout/` | Django `LogoutView` | Logs out (POST only) |
| `/accounts/signup/` | `SignUpView` | User registration page |
| `/admin/` | Django Admin | Full admin interface |

---

## Data Model

### `Post`

| Field | Type | Description |
|-------|------|-------------|
| `title` | `CharField(200)` | Title of the post |
| `author` | `ForeignKey(User)` | Linked to Django's built-in `auth.User` |
| `body` | `TextField` | Full post content |
| `created_at` | `DateTimeField` | Auto-set when the post is created |
| `updated_at` | `DateTimeField` | Auto-updated on every save |

---

## Static Files & WhiteNoise

This project uses [WhiteNoise](https://whitenoise.readthedocs.io/) to serve static files, meaning CSS loads correctly even with `DEBUG = False` — no separate web server required for local testing.

After any CSS change, re-run:

```bash
python manage.py collectstatic
```

---

## Running Tests

```bash
python manage.py test blog
```

For verbose output (see each test name):

```bash
python manage.py test blog --verbosity=2
```

### Test Coverage (52 tests)

| Test Class | What it tests |
|---|---|
| `PostModelTest` | Model `__str__`, `created_at`, `get_absolute_url` |
| `HomePageURLTest` | `/` URL, view, template, post content displayed |
| `PostDetailURLTest` | `/post/<pk>/` URL, view, template, full content, 404 |
| `PostUpdateViewTest` | Edit URL, view, template, form pre-fill, POST updates DB, 404 |
| `PostDeleteViewTest` | Delete URL, view, template, POST removes post, redirects home, 404 |
| `Custom404PageTest` | Unknown URL, missing post detail/edit/delete all return 404 |
| `LoginViewTest` | Login URL, template, signup link, valid/invalid credentials, greeting |
| `LogoutViewTest` | POST logs out and redirects home, GET returns 405, user is unauthenticated after |
| `SignUpViewTest` | Signup URL, template, login link, valid signup creates user, invalid stays on page |

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

All 36 existing tests must still pass.

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
