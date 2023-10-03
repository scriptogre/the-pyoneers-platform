# The Pyoneer Platform



Welcome to The Pyoneer Platform, the official platform for hosting The Pyoneer Project's courses. This project is built on top of Django and uses a variety of modern web technologies to provide a smooth and interactive learning experience.

## Live Platform

The live platform is accessible at [pyoneers.dev](https://pyoneers.dev).

## Technologies Used

- **Backend**: Django
- **CMS**: Wagtail
- **Frontend**: TailwindCSS, HTMX, Hyperscript
- **Templating**: Jinja2
- **Authentication**: django-allauth (Google and Discord SSO included)

## Features

- Dynamic Course Creation and Management
- Rich Text Editing with Wagtail CMS
- User Authentication including Social Login (Google and Discord)
- Interactive and Responsive UI with TailwindCSS and HTMX
- Extensible with Hyperscript

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/scriptogre/the-pyoneers-platform.git
    ```

2. Navigate to the project directory:
    ```bash
    cd the-pyoneers-platform
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser to manage the Wagtail admin:
    ```bash
    python manage.py createsuperuser
    ```

6. Set up the social apps for Google and Discord authentication:
   ```bash
   python manage.py setup_social_apps
   ```

7. Run the server:
    ```bash
    python manage.py runserver
    ```

Now, navigate to `http://localhost:8000` in your web browser.

### TailwindCSS Setup

We use TailwindCSS CLI for building the CSS. The command below compiles and watches for changes in files set as `content` from within `tailwind.config.js` file and minifies it to `output.min.css` which the `base.html` template looks for:

```bash
npx tailwindcss -i pyoneers_platform/static/css/src/input.css -o pyoneers_platform/static/css/output.css --watch --minify
```


## Usage

1. Access Wagtail Admin by going to `http://localhost:8000/admin` and login with the superuser credentials created earlier.
2. Create and manage courses, lessons and other content from the Wagtail Admin.
3. Users can sign up/login and start enrolling in courses.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
