# School Management System - Quick Reference Card

## Project Summary

A comprehensive, production-ready School Management System built with Django 4.2 featuring:
- Multi-role authentication (Admin, Teacher, Student, Parent)
- Complete academic management
- Financial tracking
- Communication system
- RESTful API

## Quick Start Commands

```bash
# 1. Navigate to project
cd school_management

# 2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env with your database credentials

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

## Access Points

| URL | Purpose |
|-----|---------|
| http://localhost:8000/ | Main Application |
| http://localhost:8000/admin/ | Django Admin |
| http://localhost:8000/login/ | Login Page |
| http://localhost:8000/api/ | REST API |

## App Overview

### 1. Users App (`apps/users/`)
- Custom user model with 4 roles
- Role-based access control
- User profile management
- Django signals for profile creation

### 2. Students App (`apps/students/`)
- Student CRUD operations
- Class management
- Subject management
- Academic year configuration

**Models:**
- `Student` - Student profiles
- `Class` - Grade/class definitions
- `Subject` - Subject catalog
- `AcademicYear` - Academic sessions

### 3. Teachers App (`apps/teachers/`)
- Teacher profiles
- Subject assignments
- Department management

**Models:**
- `Teacher` - Teacher profiles
- `TeacherSubject` - Subject assignments

### 4. Academics App (`apps/academics/`)
- Daily attendance tracking
- Exam management
- Result entry
- Timetable scheduling

**Models:**
- `Attendance` - Daily attendance
- `Exam` - Exam definitions
- `ExamSchedule` - Exam timetable
- `Result` - Student results
- `Timetable` - Class schedules

### 5. Finance App (`apps/finance/`)
- Fee category management
- Fee structure setup
- Payment tracking
- Expense recording

**Models:**
- `FeeCategory` - Fee types
- `FeeStructure` - Class-wise fees
- `StudentFee` - Individual fees
- `Payment` - Payment records
- `Expense` - School expenses

### 6. Communication App (`apps/communication/`)
- Announcements
- Messaging system
- Notifications
- Contact management

**Models:**
- `Announcement` - School-wide announcements
- `Message` - User messaging
- `Notification` - User notifications
- `Contact` - Public enquiries

## Key Features

### Authentication
- Session-based authentication
- Role-based redirects
- Custom user model
- Profile auto-creation

### Role-Based Access
- **Admin**: Full system access
- **Teacher**: Class-specific operations
- **Student**: View-only access to own data
- **Parent**: Child-related information

### REST API
- Token authentication
- CRUD operations
- Filtering and search
- Pagination
- All models serialized

### Database Schema

**Users:**
```
User (id, username, email, role, phone, address, profile_picture, date_of_birth)
  └── UserProfile (bio, emergency_contact, blood_group, religion, nationality)
```

**Academics:**
```
AcademicYear (id, name, start_date, end_date, is_current)
  └── Class (id, name, code, academic_year, class_teacher)
        └── Subject (id, name, code, description)
              └── TeacherSubject (id, teacher, subject, assigned_class, academic_year)
        └── Student (id, user, student_id, admission_date, current_class, guardian_info)
              └── Attendance (id, student, date, status, remarks)
              └── Result (id, student, exam_schedule, marks_obtained)
        └── FeeStructure (id, category, assigned_class, academic_year, amount)
              └── StudentFee (id, student, fee_structure, amount, amount_paid, status)
                    └── Payment (id, student_fee, amount, payment_date, method)
```

## Common Tasks

### Add a Student
1. Admin Panel → Users → Add User (role: student)
2. Admin Panel → Students → Add Student (link to user)
3. Assign to class

### Mark Attendance
1. Teacher Dashboard → Take Attendance
2. Select class and date
3. Mark present/absent/late for each student

### Record Payment
1. Finance → Record Payment
2. Select student fee
3. Enter amount and payment details

### Create Announcement
1. Communication → New Announcement
2. Enter title and content
3. Select priority and target audience

### Generate Fee Structure
1. Finance → Fee Categories (create types)
2. Finance → Fee Structures (class-wise amounts)
3. Finance → Generate Fees (auto-create student fees)

## API Examples

### Login
```bash
POST /api/auth/login/
{
  "username": "admin",
  "password": "password"
}
```

### List Students
```bash
GET /api/students/students/
Authorization: Token <your-token>
```

### Mark Attendance
```bash
POST /api/academics/attendance/
{
  "student": 1,
  "date": "2024-01-15",
  "status": "present"
}
```

## File Structure Quick Reference

```
school_management/
├── school/
│   ├── settings.py         # Main settings (DB, apps, middleware)
│   ├── urls.py            # Root URL config
│   ├── wsgi.py            # WSGI entry point
│   └── asgi.py            # ASGI entry point
├── apps/
│   ├── users/
│   │   ├── models.py      # User, UserProfile
│   │   ├── views.py       # Dashboard views
│   │   ├── urls.py        # URL patterns
│   │   ├── admin.py       # Admin config
│   │   ├── forms.py       # Forms
│   │   ├── serializers.py # DRF serializers
│   │   ├── signals.py     # Auto-create profile
│   │   └── api_urls.py    # API routes
│   ├── students/          # (same structure)
│   ├── teachers/          # (same structure)
│   ├── academics/         # (same structure)
│   ├── finance/           # (same structure)
│   └── communication/    # (same structure)
├── templates/
│   ├── base.html          # Base template
│   ├── home.html          # Home page
│   ├── users/             # Auth templates
│   ├── students/          # Student templates
│   ├── teachers/          # Teacher templates
│   ├── academics/         # Academic templates
│   ├── finance/           # Finance templates
│   └── communication/     # Communication templates
├── static/
│   ├── css/style.css      # Custom styles
│   └── js/script.js       # Custom JS
├── manage.py             # Django CLI
├── requirements.txt      # Dependencies
├── README.md             # Documentation
├── SETUP.md              # Setup guide
└── QUICKREF.md           # This file
```

## Admin Panel Checklist

After first login to admin panel:

1. **Academic Structure**
   - [ ] Create Academic Year (Students → Academic Years)
   - [ ] Create Classes (Students → Classes)
   - [ ] Create Subjects (Students → Subjects)

2. **User Management**
   - [ ] Create Admin users (Users → Users)
   - [ ] Create Teachers (Users → Users + Teachers → Add Teacher)
   - [ ] Create Students (Users → Users + Students → Add Student)

3. **Configuration**
   - [ ] Assign class teachers (Students → Classes → Edit)
   - [ ] Assign subjects to teachers (Teachers → Teacher Subject Assignments)

## Troubleshooting

### Error: "relation does not exist"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "Permission denied" on static files
```bash
python manage.py collectstatic
```

### Login not redirecting
Check `LOGIN_URL` and `LOGIN_REDIRECT_URL` in settings.py

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False in production
- [ ] Use strong database password
- [ ] Enable HTTPS in production
- [ ] Configure email credentials
- [ ] Set up proper ALLOWED_HOSTS
- [ ] Use environment variables for secrets

## Performance Tips

1. Use database indexes on foreign keys
2. Enable query caching
3. Use select_related/prefetch_related
4. Paginate all list views
5. Optimize static files (CDN in production)
6. Use database connection pooling

## Next Enhancements

Consider adding:
- PDF report generation (reportlab)
- Email notifications
- SMS notifications
- File uploads (assignments)
- Online examination
- Parent portal
- Mobile app (React Native/Flutter)
- Student ID card generation
- Library management
- Transport management
- Hostel management
- Online payment gateway
- Data analytics dashboard

## Support Resources

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Bootstrap 5: https://getbootstrap.com/docs/5.3/
- PostgreSQL: https://www.postgresql.org/docs/

---

Created: 2024
Version: 1.0.0
