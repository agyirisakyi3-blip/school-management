import os
from datetime import date, datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Populate database with demo accounts and sample data for all 14 roles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush", action="store_true",
            help="Delete all existing data before loading demo data",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            from django.core.management import call_command
            call_command("flush", verbosity=0, interactive=False)
            self.stdout.write(self.style.SUCCESS("Database flushed.\n"))
        else:
            demo_users = [u["username"] for u in self._get_users_data()]
            existing = User.objects.filter(username__in=demo_users).count()
            if existing > 0:
                self.stdout.write(self.style.WARNING(
                    f"Demo users already exist ({existing} found). Use --flush to reset.\n"
                ))
                return

        self.stdout.write(self.style.SUCCESS("Creating demo data...\n"))

        users_data = self._get_users_data()
        created_users = {}
        for u in users_data:
            password = u.pop("password")
            user = User.objects.create_user(**u)
            user.set_password(password)
            user.save()
            created_users[u["username"]] = user
            self.stdout.write(self.style.SUCCESS(f"  Created user: {u['username']} ({u['role']})"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Academic Year ---"))
        from apps.students.models import AcademicYear, Class, Subject
        current_year = AcademicYear.objects.create(
            name="2025-2026",
            start_date=date(2025, 9, 1),
            end_date=date(2026, 6, 30),
            is_current=True,
        )
        self.stdout.write(self.style.SUCCESS("  Created Academic Year: 2025-2026"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Classes ---"))
        classes_data = [
            {"name": "Grade 1", "code": "G1", "description": "First Grade"},
            {"name": "Grade 2", "code": "G2", "description": "Second Grade"},
            {"name": "Grade 3", "code": "G3", "description": "Third Grade"},
            {"name": "Grade 4", "code": "G4", "description": "Fourth Grade"},
            {"name": "Grade 5", "code": "G5", "description": "Fifth Grade"},
        ]
        created_classes = {}
        for c in classes_data:
            cls = Class.objects.create(
                name=c["name"], code=c["code"],
                academic_year=current_year,
                description=c["description"],
            )
            created_classes[c["code"]] = cls
            self.stdout.write(self.style.SUCCESS(f"  Created class: {c['name']}"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Subjects ---"))
        subjects_data = [
            {"name": "Mathematics", "code": "MATH", "description": "Core mathematics"},
            {"name": "English", "code": "ENG", "description": "English language and literature"},
            {"name": "Science", "code": "SCI", "description": "General science"},
            {"name": "History", "code": "HIST", "description": "World history"},
            {"name": "Art", "code": "ART", "description": "Visual arts"},
        ]
        created_subjects = {}
        for s in subjects_data:
            subj = Subject.objects.create(
                name=s["name"], code=s["code"], description=s["description"],
            )
            subj.classes.set(created_classes.values())
            created_subjects[s["code"]] = subj
            self.stdout.write(self.style.SUCCESS(f"  Created subject: {s['name']}"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Teacher Profiles ---"))
        from apps.teachers.models import Teacher, TeacherSubject
        teacher1 = Teacher.objects.create(
            user=created_users["teacher1"], employee_id="TCH001",
            join_date=date(2023, 8, 15), qualification="M.Ed Mathematics",
            experience_years=10, specialization="Mathematics & Science",
            department="Science", salary=55000,
        )
        teacher2 = Teacher.objects.create(
            user=created_users["teacher2"], employee_id="TCH002",
            join_date=date(2024, 1, 10), qualification="M.A English",
            experience_years=6, specialization="English Literature",
            department="Languages", salary=48000,
        )
        created_classes["G1"].class_teacher = created_users["teacher1"]
        created_classes["G1"].save()

        TeacherSubject.objects.create(
            teacher=teacher1, subject=created_subjects["MATH"],
            assigned_class=created_classes["G1"], academic_year=current_year,
        )
        TeacherSubject.objects.create(
            teacher=teacher1, subject=created_subjects["SCI"],
            assigned_class=created_classes["G1"], academic_year=current_year,
        )
        TeacherSubject.objects.create(
            teacher=teacher2, subject=created_subjects["ENG"],
            assigned_class=created_classes["G1"], academic_year=current_year,
        )
        self.stdout.write(self.style.SUCCESS("  Created teacher profiles & assignments"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Student Profiles ---"))
        from apps.students.models import Student
        student1 = Student.objects.create(
            user=created_users["student1"], student_id="STU00001",
            admission_date=date(2025, 9, 1),
            current_class=created_classes["G1"],
            roll_number="001", father_name="Robert Brown",
            mother_name="Susan Brown",
            guardian_name="Robert Brown", guardian_phone="555-0101",
            guardian_relation="Father",
        )
        student2 = Student.objects.create(
            user=created_users["student2"], student_id="STU00002",
            admission_date=date(2025, 9, 1),
            current_class=created_classes["G1"],
            roll_number="002", father_name="Mark Wilson",
            mother_name="Lisa Wilson",
            guardian_name="Lisa Wilson", guardian_phone="555-0102",
            guardian_relation="Mother",
        )
        self.stdout.write(self.style.SUCCESS("  Created student profiles"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Attendance ---"))
        from apps.academics.models import Attendance
        today = date.today()
        Attendance.objects.create(
            student=student1, date=today, status="present",
            marked_by=created_users["teacher1"],
        )
        Attendance.objects.create(
            student=student2, date=today, status="present",
            marked_by=created_users["teacher1"],
        )
        self.stdout.write(self.style.SUCCESS("  Created today's attendance"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Exam & Schedule ---"))
        from apps.academics.models import Exam, ExamSchedule
        exam = Exam.objects.create(
            name="Mid-Term Exam", exam_type="midterm",
            academic_year=current_year,
            start_date=date(2026, 2, 1), end_date=date(2026, 2, 5),
            description="Mid-term examinations for all grades",
        )
        ExamSchedule.objects.create(
            exam=exam, subject=created_subjects["MATH"],
            assigned_class=created_classes["G1"],
            exam_date=date(2026, 2, 1),
            start_time="09:00:00", end_time="11:00:00",
            total_marks=100, passing_marks=40, venue="Room 101",
        )
        ExamSchedule.objects.create(
            exam=exam, subject=created_subjects["ENG"],
            assigned_class=created_classes["G1"],
            exam_date=date(2026, 2, 2),
            start_time="09:00:00", end_time="11:00:00",
            total_marks=100, passing_marks=40, venue="Room 101",
        )
        self.stdout.write(self.style.SUCCESS("  Created Mid-Term Exam with schedule"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Results ---"))
        from apps.academics.models import Result
        math_schedule = ExamSchedule.objects.filter(subject=created_subjects["MATH"]).first()
        Result.objects.create(
            student=student1, exam_schedule=math_schedule,
            marks_obtained=85, created_by=created_users["teacher1"],
        )
        Result.objects.create(
            student=student2, exam_schedule=math_schedule,
            marks_obtained=72, created_by=created_users["teacher1"],
        )
        self.stdout.write(self.style.SUCCESS("  Created exam results"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Timetable ---"))
        from apps.academics.models import Timetable
        Timetable.objects.create(
            assigned_class=created_classes["G1"], subject=created_subjects["MATH"],
            teacher=teacher1, day=1, start_time="08:00:00", end_time="09:00:00",
            venue="Room 101", academic_year=current_year,
        )
        Timetable.objects.create(
            assigned_class=created_classes["G1"], subject=created_subjects["ENG"],
            teacher=teacher2, day=1, start_time="09:00:00", end_time="10:00:00",
            venue="Room 101", academic_year=current_year,
        )
        Timetable.objects.create(
            assigned_class=created_classes["G1"], subject=created_subjects["SCI"],
            teacher=teacher1, day=2, start_time="08:00:00", end_time="09:00:00",
            venue="Lab 1", academic_year=current_year,
        )
        self.stdout.write(self.style.SUCCESS("  Created class timetable"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Finance Data ---"))
        from apps.finance.models import (
            FeeCategory, FeeParticular, FeeGroup, FeeStructure,
            StudentFee, Expense,
        )
        fee_cat = FeeCategory.objects.create(
            name="Tuition Fee", code="TUITION",
            category_type="tuition", description="Regular tuition fees",
        )
        particular = FeeParticular.objects.create(
            category=fee_cat, name="Term Tuition", code="TERM_TUIT",
            amount=2500, frequency="quarterly",
        )
        fee_group = FeeGroup.objects.create(
            name="Grade 1 Fees", code="G1_FEE",
            academic_year=current_year,
            description="Fee structure for Grade 1",
        )
        from apps.finance.models import FeeGroupParticular
        FeeGroupParticular.objects.create(fee_group=fee_group, particular=particular)
        from apps.finance.models import ClassFee
        ClassFee.objects.create(
            assigned_class=created_classes["G1"], fee_group=fee_group,
        )
        fee_structure = FeeStructure.objects.create(
            category=fee_cat, assigned_class=created_classes["G1"],
            academic_year=current_year, amount=2500,
            due_date=date(2026, 4, 15),
        )
        student_fee = StudentFee.objects.create(
            student=student1, fee_structure=fee_structure,
            amount=2500, due_date=date(2026, 4, 15),
        )
        from apps.finance.models import Payment
        Payment.objects.create(
            student_fee=student_fee, amount=2500,
            payment_date=date(2026, 4, 1), payment_method="bank_transfer",
            transaction_id="TXN001", received_by=created_users["accountant"],
        )
        Expense.objects.create(
            title="Office Supplies", category="supplies",
            amount=350, expense_date=date(2026, 4, 15),
            description="Printer paper, pens, notebooks",
            recorded_by=created_users["accountant"],
        )
        self.stdout.write(self.style.SUCCESS("  Created fee structure, payment, and expense"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Library Data ---"))
        from apps.library.models import BookCategory, Book, LibraryMember, BookIssue
        book_cat = BookCategory.objects.create(
            name="Science", description="Science and nature books",
        )
        book = Book.objects.create(
            title="Introduction to Physics", isbn="978-0-123456-00-1",
            author="Dr. Physics", publisher="Science Press",
            category=book_cat, quantity=5, available_quantity=4,
            location="Shelf A-1",
        )
        lib_member = LibraryMember.objects.create(
            user=created_users["student1"], member_id="LIB001",
            member_type="student",
            expiry_date=date(2026, 6, 30),
        )
        BookIssue.objects.create(
            book=book, member=lib_member,
            due_date=date(2026, 5, 15),
            issued_by=created_users["librarian"],
        )
        self.stdout.write(self.style.SUCCESS("  Created library book and issue"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Transport Data ---"))
        from apps.transport.models import TransportRoute, Vehicle, VehicleRoute, StudentTransport
        route = TransportRoute.objects.create(
            name="Route A - Downtown", route_from="Downtown",
            route_to="School Campus", description="Main downtown route",
        )
        vehicle = Vehicle.objects.create(
            vehicle_number="BUS-001", vehicle_type="bus",
            model="Volvo 9700", capacity=50,
            driver_name="Tom Harris", driver_phone="555-0200",
            license_number="DL-12345",
        )
        vehicle_route = VehicleRoute.objects.create(
            route=route, vehicle=vehicle,
            driver=created_users["driver"],
            pickup_time="07:30:00", drop_time="15:30:00",
            fare=150,
        )
        StudentTransport.objects.create(
            student=student1, vehicle_route=vehicle_route,
            pickup_point="Main Street Stop",
        )
        self.stdout.write(self.style.SUCCESS("  Created transport route & assignment"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Dormitory Data ---"))
        from apps.dormitory.models import Dormitory, Room, StudentRoom
        dorm = Dormitory.objects.create(
            name="Boys Hostel A", type="boys",
            warden_name="James Clark", warden_phone="555-0300",
            total_rooms=10, capacity=40,
        )
        room = Room.objects.create(
            dormitory=dorm, room_number="101", room_type="double",
            floor=1, total_beds=2, cost_per_bed=500,
        )
        StudentRoom.objects.create(
            student=student1, room=room, bed_number="A",
            start_date=date(2025, 9, 1),
        )
        self.stdout.write(self.style.SUCCESS("  Created dormitory & room assignment"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Homework ---"))
        from apps.homework.models import Homework
        hw = Homework.objects.create(
            title="Math Chapter 5 Exercises",
            description="Complete exercises 1-20 from Chapter 5",
            subject=created_subjects["MATH"], class_obj=created_classes["G1"],
            teacher=created_users["teacher1"],
            due_date=timezone.now() + timedelta(days=7),
            priority="medium",
        )
        from apps.homework.models import HomeworkSubmission
        HomeworkSubmission.objects.create(
            homework=hw, student=student1,
            submission_text="Completed all exercises",
            status="accepted", marks=95,
        )
        self.stdout.write(self.style.SUCCESS("  Created homework & submission"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Leave Types & Requests ---"))
        from apps.leaves.models import LeaveType, LeaveRequest
        leave_type = LeaveType.objects.create(
            name="Sick Leave", code="SICK",
            description="Medical leave", days_allowed=10,
            is_paid=True,
        )
        LeaveRequest.objects.create(
            user=created_users["teacher1"], leave_type=leave_type,
            start_date=date(2026, 5, 1), end_date=date(2026, 5, 3),
            reason="Medical appointment and recovery",
            status="pending",
        )
        self.stdout.write(self.style.SUCCESS("  Created leave type & request"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Communications ---"))
        from apps.communication.models import Announcement, Notification, Contact
        Announcement.objects.create(
            title="Welcome to New Semester",
            content="We welcome all students and staff to the new academic semester.",
            priority="high", created_by=created_users["admin"],
        )
        Notification.objects.create(
            recipient=created_users["student1"],
            notification_type="announcement",
            title="New Announcement",
            message="Check out the latest announcements on the dashboard.",
        )
        Contact.objects.create(
            name="Prospective Parent", email="prospect@email.com",
            phone="555-9999", subject="Admission Inquiry",
            message="I would like to know about the admission process.",
        )
        self.stdout.write(self.style.SUCCESS("  Created announcement, notification, and contact"))

        self.stdout.write(self.style.SUCCESS("\n--- Creating Front Desk Data ---"))
        from apps.frontdesk.models import Visitor, Complaint
        Visitor.objects.create(
            name="Guest Visitor", phone="555-8888",
            purpose="Campus Tour", person_to_meet="Receptionist",
        )
        Complaint.objects.create(
            complaint_type="facility", complainant_name="Jane Doe",
            complainant_email="jane@email.com", complainant_phone="555-7777",
            subject="Broken AC in Lab", description="The AC unit in Lab 1 is not working.",
            priority="high", status="pending", assigned_to="Maintenance Team",
        )
        self.stdout.write(self.style.SUCCESS("  Created visitor log & complaint"))

        self.stdout.write(self.style.SUCCESS("\n" + "=" * 50))
        self.stdout.write(self.style.SUCCESS("DEMO DATA CREATED SUCCESSFULLY!"))
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(self.style.WARNING("\nLogin Credentials:\n"))
        self.stdout.write("  admin        / admin123       (Admin)")
        self.stdout.write("  teacher1     / teacher123     (Teacher)")
        self.stdout.write("  teacher2     / teacher123     (Teacher)")
        self.stdout.write("  student1     / student123     (Student)")
        self.stdout.write("  student2     / student123     (Student)")
        self.stdout.write("  parent1      / parent123      (Parent)")
        self.stdout.write("  parent2      / parent123      (Parent)")
        self.stdout.write("  accountant   / staff123       (Accountant)")
        self.stdout.write("  librarian    / staff123       (Librarian)")
        self.stdout.write("  receptionist / staff123       (Receptionist)")
        self.stdout.write("  driver       / staff123       (Driver)")
        self.stdout.write("  cook         / staff123       (Cook)")
        self.stdout.write("  guard        / staff123       (Guard)")
        self.stdout.write("  cleaner      / staff123       (Cleaner)")
        self.stdout.write("  maintenance  / staff123       (Maintenance)")
        self.stdout.write("  counselor    / staff123       (Counselor)")
        self.stdout.write("  nurse        / staff123       (Nurse)")
        self.stdout.write("")

    def _get_users_data(self):
        return [
            {"username": "admin", "email": "admin@school.com", "role": User.Role.ADMIN,
             "first_name": "Admin", "last_name": "User", "password": "admin123"},
            {"username": "teacher1", "email": "john.smith@school.com", "role": User.Role.TEACHER,
             "first_name": "John", "last_name": "Smith", "password": "teacher123"},
            {"username": "teacher2", "email": "sarah.jones@school.com", "role": User.Role.TEACHER,
             "first_name": "Sarah", "last_name": "Jones", "password": "teacher123"},
            {"username": "student1", "email": "alex.brown@school.com", "role": User.Role.STUDENT,
             "first_name": "Alex", "last_name": "Brown", "password": "student123"},
            {"username": "student2", "email": "emma.wilson@school.com", "role": User.Role.STUDENT,
             "first_name": "Emma", "last_name": "Wilson", "password": "student123"},
            {"username": "parent1", "email": "robert.brown@school.com", "role": User.Role.PARENT,
             "first_name": "Robert", "last_name": "Brown", "password": "parent123"},
            {"username": "parent2", "email": "lisa.wilson@school.com", "role": User.Role.PARENT,
             "first_name": "Lisa", "last_name": "Wilson", "password": "parent123"},
            {"username": "accountant", "email": "mike.finance@school.com", "role": User.Role.ACCOUNTANT,
             "first_name": "Mike", "last_name": "Johnson", "password": "staff123"},
            {"username": "librarian", "email": "nancy.library@school.com", "role": User.Role.LIBRARIAN,
             "first_name": "Nancy", "last_name": "Davis", "password": "staff123"},
            {"username": "receptionist", "email": "karen.front@school.com", "role": User.Role.RECEPTIONIST,
             "first_name": "Karen", "last_name": "White", "password": "staff123"},
            {"username": "driver", "email": "tom.drive@school.com", "role": User.Role.DRIVER,
             "first_name": "Tom", "last_name": "Harris", "password": "staff123"},
            {"username": "cook", "email": "maria.kitchen@school.com", "role": User.Role.COOK,
             "first_name": "Maria", "last_name": "Garcia", "password": "staff123"},
            {"username": "guard", "email": "james.security@school.com", "role": User.Role.GUARD,
             "first_name": "James", "last_name": "Clark", "password": "staff123"},
            {"username": "cleaner", "email": "anna.clean@school.com", "role": User.Role.CLEANER,
             "first_name": "Anna", "last_name": "Lewis", "password": "staff123"},
            {"username": "maintenance", "email": "paul.fix@school.com", "role": User.Role.MAINTENANCE,
             "first_name": "Paul", "last_name": "Walker", "password": "staff123"},
            {"username": "counselor", "email": "diane.counsel@school.com", "role": User.Role.COUNSELOR,
             "first_name": "Diane", "last_name": "Hall", "password": "staff123"},
            {"username": "nurse", "email": "rachel.health@school.com", "role": User.Role.NURSE,
             "first_name": "Rachel", "last_name": "Young", "password": "staff123"},
        ]
