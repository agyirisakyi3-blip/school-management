from rest_framework.routers import DefaultRouter
from .serializers import (
    AttendanceViewSet,
    ExamViewSet,
    ExamScheduleViewSet,
    ResultViewSet,
    TimetableViewSet,
)

router = DefaultRouter()
router.register(r"attendance", AttendanceViewSet, basename="attendance")
router.register(r"exams", ExamViewSet, basename="exam")
router.register(r"exam-schedules", ExamScheduleViewSet, basename="exam-schedule")
router.register(r"results", ResultViewSet, basename="result")
router.register(r"timetable", TimetableViewSet, basename="timetable")

urlpatterns = []
