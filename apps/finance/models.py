from django.db import models
from django.core.validators import MinValueValidator


class FeeCategory(models.Model):
    """Fee category model - main grouping for fees."""

    class CategoryType(models.TextChoices):
        TUITION = "tuition", "Tuition Fee"
        ANNUAL = "annual", "Annual Charges"
        MONTHLY = "monthly", "Monthly Charges"
        ONE_TIME = "one_time", "One Time"
        TRANSPORT = "transport", "Transport Fee"
        EXAM = "exam", "Examination Fee"
        LIBRARY = "library", "Library Fee"
        LABORATORY = "laboratory", "Laboratory Fee"
        SPORTS = "sports", "Sports Fee"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    category_type = models.CharField(
        max_length=20,
        choices=CategoryType.choices,
        default=CategoryType.TUITION,
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fee Category"
        verbose_name_plural = "Fee Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class FeeParticular(models.Model):
    """Individual fee items/particulars."""

    FREQUENCY_CHOICES = [
        ("one_time", "One Time"),
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("semi_annual", "Semi-Annual"),
        ("annual", "Annual"),
    ]

    category = models.ForeignKey(
        FeeCategory, on_delete=models.CASCADE, related_name="particulars"
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, default="one_time"
    )
    is_optional = models.BooleanField(
        default=False, help_text="Students can opt out of this fee"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fee Particular"
        verbose_name_plural = "Fee Particulars"
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class FeeGroup(models.Model):
    """Groups of fee particulars that can be assigned to classes."""

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    particulars = models.ManyToManyField(
        FeeParticular,
        through="FeeGroupParticular",
        related_name="fee_groups",
    )
    academic_year = models.ForeignKey(
        "students.AcademicYear",
        on_delete=models.CASCADE,
        related_name="fee_groups",
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fee Group"
        verbose_name_plural = "Fee Groups"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"

    def get_total_amount(self):
        return sum(p.particular.amount for p in self.feegroupparticular_set.all())


class FeeGroupParticular(models.Model):
    """Junction table for FeeGroup and FeeParticular with custom amount."""

    fee_group = models.ForeignKey(FeeGroup, on_delete=models.CASCADE)
    particular = models.ForeignKey(FeeParticular, on_delete=models.CASCADE)
    custom_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Override the default amount (optional)",
    )

    class Meta:
        unique_together = ["fee_group", "particular"]

    def get_amount(self):
        return self.custom_amount or self.particular.amount


class ClassFee(models.Model):
    """Fee assigned to a specific class."""

    assigned_class = models.ForeignKey(
        "students.Class",
        on_delete=models.CASCADE,
        related_name="class_fees",
    )
    fee_group = models.ForeignKey(
        FeeGroup,
        on_delete=models.CASCADE,
        related_name="class_fees",
    )
    amount_override = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Override total fee amount",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Class Fee"
        verbose_name_plural = "Class Fees"
        unique_together = ["assigned_class", "fee_group"]
        ordering = ["assigned_class__name"]

    def __str__(self):
        return f"{self.assigned_class.name} - {self.fee_group.name}"

    def get_total_amount(self):
        if self.amount_override:
            return self.amount_override
        return self.fee_group.get_total_amount()


class DiscountCategory(models.Model):
    """Discount categories (sibling, staff, merit, etc.)."""

    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed Amount"

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(
        max_length=20, choices=DiscountType.choices, default=DiscountType.PERCENTAGE
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    max_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum discount amount (for percentage type)",
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Discount Category"
        verbose_name_plural = "Discount Categories"
        ordering = ["name"]

    def __str__(self):
        if self.discount_type == self.DiscountType.PERCENTAGE:
            return f"{self.name} ({self.value}%)"
        return f"{self.name} ({self.value})"


class StudentDiscount(models.Model):
    """Discount assigned to a student."""

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="discounts",
    )
    discount_category = models.ForeignKey(
        DiscountCategory,
        on_delete=models.CASCADE,
        related_name="student_discounts",
    )
    reason = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Student Discount"
        verbose_name_plural = "Student Discounts"
        unique_together = ["student", "discount_category"]

    def __str__(self):
        return f"{self.student} - {self.discount_category.name}"

    def get_discount_amount(self, fee_amount):
        if (
            self.discount_category.discount_type
            == DiscountCategory.DiscountType.PERCENTAGE
        ):
            discount = fee_amount * (self.discount_category.value / 100)
            if self.discount_category.max_amount:
                discount = min(discount, self.discount_category.max_amount)
            return discount
        return min(self.discount_category.value, fee_amount)


class FeeStructure(models.Model):
    """Fee structure model."""

    category = models.ForeignKey(
        FeeCategory, on_delete=models.CASCADE, related_name="fee_structures"
    )
    assigned_class = models.ForeignKey(
        "students.Class", on_delete=models.CASCADE, related_name="fee_structures"
    )
    academic_year = models.ForeignKey(
        "students.AcademicYear", on_delete=models.CASCADE, related_name="fee_structures"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fee Structure"
        verbose_name_plural = "Fee Structures"
        unique_together = ["category", "assigned_class", "academic_year"]

    def __str__(self):
        return f"{self.category.name} - {self.assigned_class.name} - {self.amount}"


class StudentFee(models.Model):
    """Student fee record model."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PARTIAL = "partial", "Partial"
        PAID = "paid", "Paid"
        OVERDUE = "overdue", "Overdue"

    student = models.ForeignKey(
        "students.Student", on_delete=models.CASCADE, related_name="student_fees"
    )
    fee_structure = models.ForeignKey(
        FeeStructure, on_delete=models.CASCADE, related_name="student_fees"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student Fee"
        verbose_name_plural = "Student Fees"
        unique_together = ["student", "fee_structure"]

    def __str__(self):
        return f"{self.student} - {self.fee_structure.category.name} - {self.amount}"

    @property
    def balance(self):
        return self.amount - self.amount_paid


class Payment(models.Model):
    """Payment model."""

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        BANK_TRANSFER = "bank_transfer", "Bank Transfer"
        CHEQUE = "cheque", "Cheque"
        CARD = "card", "Card"
        ONLINE = "online", "Online"

    student_fee = models.ForeignKey(
        StudentFee, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    transaction_id = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    received_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_payments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.student_fee.student} - {self.amount} - {self.payment_date}"


class Expense(models.Model):
    """Expense model."""

    CATEGORY_CHOICES = [
        ("salary", "Salary"),
        ("utilities", "Utilities"),
        ("maintenance", "Maintenance"),
        ("supplies", "Supplies"),
        ("events", "Events"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    description = models.TextField(blank=True)
    receipt_number = models.CharField(max_length=100, blank=True)
    recorded_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="recorded_expenses",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ["-expense_date"]

    def __str__(self):
        return f"{self.title} - {self.amount} - {self.expense_date}"
