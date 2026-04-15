# School Management System

A complete, production-ready School Management System built with Django.

## Features

- **Multi-role System**: Admin, Teacher, Student, Parent
- **Authentication**: Login/logout with role-based access control
- **Dashboards**: Role-specific dashboards
- **Student Management**: CRUD, class assignment, profiles
- **Teacher Management**: Profiles, subject assignments
- **Class & Subject Management**: Academic structure
- **Attendance System**: Daily tracking
- **Exams & Grading**: Complete exam management
- **Timetable Management**: Class schedules
- **Fees/Payment Tracking**: Financial management
- **Notifications/Announcements**: Communication system
- **Messaging**: Teacher-student-parent communication
- **Reports**: PDF export capabilities
- **REST API**: Full API endpoints

## Tech Stack

- Django 4.2
- Django REST Framework
- PostgreSQL
- Bootstrap 5
- Crispy Forms
- Django Filters

## Project Structure

```
school_management/
├── school/                  # Main Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                    # Django apps
│   ├── users/              # User management & authentication
│   ├── students/           # Student management
│   ├── teachers/          # Teacher management
│   ├── academics/         # Attendance, exams, timetable
│   ├── finance/          # Fees and payments
│   └── communication/   # Messages and notifications
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # User uploads
├── requirements.txt
├── manage.py
└── README.md
```

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd school_management
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   
   Create a PostgreSQL database:
   ```sql
   CREATE DATABASE school_db;
   CREATE USER school_user WITH PASSWORD 'your-password';
   GRANT ALL PRIVILEGES ON DATABASE school_db TO school_user;
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Admin Panel: http://localhost:8000/admin/
   - Login: http://localhost:8000/login/

## Default User Roles

After creating a superuser, you can:
1. Login to admin panel
2. Create users with roles: `admin`, `teacher`, `student`, `parent`

## API Endpoints

The API is available at `/api/`

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout

### Users
- `GET /api/users/` - List users
- `POST /api/users/` - Create user
- `GET /api/users/{id}/` - Get user details

### Students
- `GET /api/students/students/` - List students
- `POST /api/students/students/` - Create student
- `GET /api/students/classes/` - List classes
- `GET /api/students/subjects/` - List subjects

### Academics
- `GET /api/academics/attendance/` - List attendance
- `POST /api/academics/attendance/` - Mark attendance
- `GET /api/academics/exams/` - List exams
- `GET /api/academics/results/` - List results
- `GET /api/academics/timetable/` - List timetable

### Finance
- `GET /api/finance/student-fees/` - List fees
- `POST /api/finance/payments/` - Record payment

## Role Permissions

### Admin
- Full access to all modules
- Manage users, students, teachers
- Configure classes, subjects
- Financial management
- View all reports

### Teacher
- View assigned classes
- Mark attendance
- Enter exam results
- View timetable
- Send messages

### Student
- View attendance
- View results
- View timetable
- View announcements
- Send messages

### Parent
- View child's attendance
- View child's results
- View fee status
- Receive notifications

## Templates

The system uses Bootstrap 5 for responsive UI. Templates are organized by app:
- `templates/users/` - Authentication & dashboards
- `templates/students/` - Student management
- `templates/teachers/` - Teacher management
- `templates/academics/` - Attendance, exams, timetable
- `templates/finance/` - Fees and payments
- `templates/communication/` - Messages and notifications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For support, email support@school.com or create an issue.

## Screenshots

(Add screenshots here)

## Changelog

### v1.0.0
- Initial release
- Multi-role authentication
- Student, Teacher management
- Attendance system
- Exam & Results management
- Fee management
- Messaging system
- REST API
