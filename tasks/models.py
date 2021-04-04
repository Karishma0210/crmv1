from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    # if user gets deleted then its respective tasks will also be deleted
    given_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="given_to", null=True)
    given_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="given_by", null=True)
    task_date = models.DateField(null=True)
    deadline = models.DateField(null=True)
    date_created = models.DateTimeField(
        auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    pushed_on_portal = models.DateTimeField(blank=True, null=True)

    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    READY_TO_REVIEW = 'ready_to_review'
    # APPROVED = 'approved'
    # REJECTED = 'rejected'
    READY_TO_UPLOAD = 'ready_to_upload'
    CANCELLED = 'cancelled'
    UPLOADED = 'uploaded'

    STATUS_CHOICES = (
        (NEW, 'NEW'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (READY_TO_REVIEW, 'READY_TO_REVIEW'),
        # (APPROVED, 'APPROVED'),
        # (REJECTED, 'REJECTED'),
        (READY_TO_UPLOAD, 'READY_TO_UPLOAD'),
        (CANCELLED, 'CANCELLED'),
        (UPLOADED, 'UPLOADED')
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=NEW)


# it has to be assosiated with Task
class Product(models.Model):
    product_id = models.IntegerField(null=False, default=0000)
    name = models.CharField(max_length=200)
    permalink = models.CharField(null=True, max_length=800)
    regular_price = models.FloatField(blank=True, null=True)
    sale_price = models.FloatField(blank=True, null=True)
    # curr_price = models.FloatField(blank=True, null=True)
    parent_id = models.IntegerField(null=False, default=0000)

    NOT_REVIEWED = 'not_reviewed'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    UPLOADED = 'uploaded'

    STATUS_CHOICES = (
        (NOT_REVIEWED, 'NOT_REVIEWED'),
        (APPROVED, 'APPROVED'),
        (REJECTED, 'REJECTED'),
        (UPLOADED, 'UPLOADED')
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=NOT_REVIEWED)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE)
    last_mod_onsite = models.DateTimeField(blank=True, null=True)

    # after product's value has been updated
    new_reg_price = models.FloatField(blank=True, null=True)
    suggested_price = models.FloatField(blank=True, null=True)
    sharaf_dg_price = models.FloatField(blank=True, null=True)
    sharaf_dg_product_link = models.CharField(null=True, max_length=1000)
    carrefour_price = models.FloatField(blank=True, null=True)
    carrefour_product_link = models.CharField(null=True, max_length=1000)
    lulu_price = models.FloatField(blank=True, null=True)
    lulu_product_link = models.CharField(null=True, max_length=1000)
    jumbo_price = models.FloatField(blank=True, null=True)
    jumbo_product_link = models.CharField(null=True, max_length=1000)
    axiom_price = models.FloatField(blank=True, null=True)
    axiom_product_link = models.CharField(null=True, max_length=1000)
