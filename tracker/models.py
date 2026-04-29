from django.db import models

from django.db import models

class Expense(models.Model):
    amount = models.FloatField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.category
    

    from django.db import models
from django.contrib.auth.models import User   # ✅ add this

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ ADD THIS
    amount = models.FloatField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()