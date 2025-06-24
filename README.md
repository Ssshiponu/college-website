# 📚 College Website

A modern, responsive Django and Tailwindcss powered website for Dhamrai Government College, featuring dynamic content management, event listings, faculty profiles, galleries, and more.

---

## Live Demo

A live demo of the Dhamrai Government College website is available for preview and testing:

[🌐 View Live Demo](https://dhamraigovtcollege.pythonanywhere.com)



## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Setup & Installation](#setup--installation)
5. [Core Django Apps](#core-django-apps)
6. [Templates & Static Files](#templates--static-files)
7. [Database Models](#database-models)
8. [Development & Running](#development--running)
9. [Customization](#customization)
10. [Contributing](#contributing)
11. [License](#license)

---

## Project Overview

This project is a full-featured website for Dhamrai Government College, built with Django. It provides information about the college, its departments, faculty, events, notices, gallery, and more. The site is designed to be user-friendly, mobile-responsive, and easy to maintain.

---

## Features

- **Dynamic Content:** Manage notices, events, faculty, departments, and gallery via Django admin.
- **Responsive Design:** Mobile-friendly layouts using Tailwind CSS.
- **Rich Templates:** Modular templates with reusable components (header, footer, banners, FAQ, etc.).
- **Media Management:** Gallery and campus images handled via Django's media system.
- **Localization:** Bengali language support throughout the UI.
- **SEO Friendly:** Semantic HTML and meta tags for better search engine visibility.

---

## Project Structure

```
college_college/
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── dgc/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/
│   └── images/
└── templates/
    ├── components/
    ├── 404.html
    ├── admission.html
    ├── alumni.html
    ├── base.html
    ├── calender.html
    ├── campus.html
    ├── contact.html
    ├── department_detail.html
    ├── departments.html
    ├── event_detail.html
    ├── events.html
    ├── faculty_detail.html
    ├── faculty.html
    ├── gallery.html
    ├── history.html
    └── ...
```

---

## Setup & Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/ssshiponu/college-website
   cd college-website
   ```

2. **Create a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   - Copy `.env.example` to `.env` and set your secrets.

5. **Apply Migrations**
   ```sh
   python manage.py migrate
   ```

6. **Run the Development Server**
   ```sh
   python manage.py runserver
   ```

---

## Core Django Apps

- **core**: Main app containing models, views, URLs, and admin configuration for college data.
- **dgc**: Project-level settings, URLs, and WSGI/ASGI configuration.

---

## Templates & Static Files

- **Templates:** Located in `templates/`, organized by page and component.
- **Static Files:** CSS and images in `static/`. Tailwind CSS output is in `static/css/output.css`.

### Notable Templates

- `base.html`: Main layout, includes header, footer, and message handling.
- `components/`: Reusable UI parts (header, footer, banners, FAQ, etc.).
- Page templates: `index.html`, `admission.html`, `faculty.html`, `events.html`, `gallery.html`, etc.

---

## Database Models

Defined in `core/models.py`:

- **Notice:** Title, description, category, publish date, document, importance, slug.
- **Gallery:** Title, image, category, description, upload date.
- **Faculty:** Name, details, and more.
- **Department, Event, Alumni, etc.**: Additional models as needed.

---

## Development & Running

- **Development Server:**  
  ```sh
  python manage.py runserver
  ```
- **Static Files:** Managed via Django's staticfiles app.
- **Admin Panel:**  
  Visit `/admin` to manage content.

---

## Customization

- **Styling:** Modify `static/css/output.css` or update Tailwind config.
- **Templates:** Edit or extend templates in `templates/` for custom pages or layouts.
- **Models:** Add or modify models in `core/models.py` as needed.

---

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit your changes.
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request.

---

## License

This project is licensed under the MIT License.

---