# VolHub

VolHub is a Django-based web application that serves as a platform for managing volunteer activities and user interactions. The project is built using Django 5.1.5 and follows a multi-app architecture with separate modules for Admin, Guest, and User functionalities.

## Features

- Multi-user role system (Admin, Guest, User)
- Email functionality integration
- Media file handling
- SQLite database backend
- Static and media file management

## Project Structure

```
volHub/
├── Admin/          # Admin-specific functionality
├── Guest/          # Guest user features
├── User/           # Registered user features
├── MainProject/    # Main project configuration
├── templates/      # HTML templates
├── media/          # User-uploaded media files
├── assets/         # Static assets
└── manage.py       # Django management script
```

## Prerequisites

- Python 3.x
- Django 5.1.5
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ecoholic84/volHub.git
cd volHub
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Configuration

The project uses the following key configurations:

- Database: SQLite3
- Email: Gmail SMTP
- Static files: `/static/`
- Media files: `/media/`

## Security Notes

- The project includes Django's built-in security features
- CSRF protection is enabled
- Password validation is implemented
- Debug mode is set to True by default (change for production)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or support, please contact: volhubofecoholic@gmail.com 
