# Setup Instructions for School Management System

## Step 1: Prerequisites

Ensure you have the following installed:
- Python 3.10 or higher
- PostgreSQL 14 or higher
- Git (optional)

## Step 2: Clone and Setup

```bash
# Navigate to your desired directory
cd "C:\Users\AGYIRI SAKYI\Videos\Django projects"

# The project is already created at school_management/
cd school_management
```

## Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Database Setup

### Create PostgreSQL Database:

1. Open pgAdmin or PostgreSQL command line

2. Run these commands:
```sql
-- Create database
CREATE DATABASE school_db;

-- Create user
CREATE USER school_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE school_db TO school_user;

-- Connect to database
\c school_db

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO school_user;
```

## Step 6: Environment Configuration

```bash
# Copy the example env file
copy .env.example .env

# Edit .env with your database credentials
notepad .env
```

Update these values in `.env`:
```
SECRET_KEY=generate-a-new-secret-key
DEBUG=True
DB_NAME=school_db
DB_USER=school_user
DB_PASSWORD=your_secure_password
```

To generate a new SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 7: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 8: Create Superuser

```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

## Step 9: Create Sample Data (Optional)

For testing, you can create sample academic years and classes:

1. Login to admin panel: http://localhost:8000/admin/
2. Navigate to Students > Academic Years
3. Add an academic year (e.g., "2024-2025")
4. Navigate to Students > Classes
5. Add classes (e.g., "Class 1", "Class 2")
6. Navigate to Students > Subjects
7. Add subjects (e.g., "Mathematics", "Science")

## Step 10: Run Development Server

```bash
python manage.py runserver
```

Visit:
- Application: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- API: http://localhost:8000/api/

## Step 11: Create Users with Roles

1. Login to admin panel
2. Go to Users > Users
3. Add new users and set their roles:
   - `admin` - For administrators
   - `teacher` - For teachers
   - `student` - For students
   - `parent` - For parents

## API Testing

### Get Auth Token:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### List Students:
```bash
curl -X GET http://localhost:8000/api/students/students/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure database exists

### Migration Errors
- Delete `db.sqlite3` if it exists (for SQLite fallback)
- Re-run migrations

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

## Production Deployment

For production:

1. Set `DEBUG=False` in `.env`
2. Use a proper web server (Nginx/Apache)
3. Configure SSL certificate
4. Set up proper email backend
5. Use environment variables for secrets

## Project Structure Overview

```
school_management/
├── school/                    # Main Django settings
│   ├── settings.py           # All configurations
│   ├── urls.py               # Root URL patterns
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── apps/                      # Django applications
│   ├── users/               # Custom user model & auth
│   ├── students/            # Student & academic structure
│   ├── teachers/            # Teacher management
│   ├── academics/           # Attendance, exams, timetable
│   ├── finance/             # Fees and payments
│   └── communication/       # Messages and notifications
├── templates/                 # HTML templates
├── static/                    # CSS, JavaScript
├── media/                      # User uploads
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation
```

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/login/` | Login page |
| `/logout/` | Logout |
| `/admin/` | Django admin |
| `/students/` | Student management |
| `/teachers/` | Teacher management |
| `/academics/` | Academics module |
| `/finance/` | Finance module |
| `/communication/` | Communication module |
| `/api/` | REST API |

## Quick Test Flow

1. Create admin user
2. Login as admin
3. Create academic year
4. Create classes
5. Create subjects
6. Create teachers (with teacher role)
7. Create students (with student role)
8. Mark attendance
9. Create exams
10. Enter results
11. View as student

## Support

For issues or questions:
- Check README.md for detailed documentation
- Review Django documentation
- Check PostgreSQL documentation

## Next Steps

After setup:
1. Customize templates
2. Add email notifications
3. Implement PDF reports
4. Add more features as needed
5. Configure production server
