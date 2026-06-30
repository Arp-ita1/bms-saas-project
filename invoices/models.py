from decimal import Decimal

from django.db import models
from django.utils import timezone


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Partial', 'Partial'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    ]

    business = models.ForeignKey(
        'businesses.Business',
        on_delete=models.CASCADE,
        related_name='invoices',
        null=True,
        blank=True
    )

    invoice_number = models.CharField(max_length=30, unique=True, blank=True)

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices'
    )

    description = models.TextField(blank=True, null=True)
    invoice_date = models.DateField(default=timezone.now)
    due_date = models.DateField(blank=True, null=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pending_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Unpaid')
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def amount(self):
        return self.total_amount

    def update_status(self):
        if self.status == 'Cancelled':
            return

        self.pending_amount = self.total_amount - self.paid_amount

        if self.paid_amount <= 0:
            self.status = 'Unpaid'
        elif self.paid_amount < self.total_amount:
            self.status = 'Partial'
        else:
            self.status = 'Paid'
            self.pending_amount = Decimal('0.00')

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_invoice = Invoice.objects.order_by('-id').first()
            next_id = 1 if not last_invoice else last_invoice.id + 1
            self.invoice_number = f'INV-{next_id:05d}'

        if self.total_amount <= 0:
            self.total_amount = self.subtotal + self.tax - self.discount
            if self.total_amount < 0:
                self.total_amount = Decimal('0.00')

        self.update_status()
        super().save(*args, **kwargs)

    def calculate_totals(self):
        subtotal = Decimal('0.00')

        for item in self.items.all():
            subtotal += item.total_price

        self.subtotal = subtotal
        self.total_amount = self.subtotal + self.tax - self.discount

        if self.total_amount < 0:
            self.total_amount = Decimal('0.00')

        self.update_status()
        self.save()

    def __str__(self):
        return self.invoice_number


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    item_name = models.CharField(max_length=160)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)
        self.invoice.calculate_totals()

    def delete(self, *args, **kwargs):
        invoice = self.invoice
        super().delete(*args, **kwargs)
        invoice.calculate_totals()

    def __str__(self):
        return self.item_name