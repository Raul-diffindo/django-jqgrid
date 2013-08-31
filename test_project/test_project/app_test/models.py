from django.db import models
from datetime import datetime

class Customer(models.Model):
    """
    Customer Model
    """
    created_at = models.DateTimeField(auto_now=True, default=datetime.now())
    customer_code = models.IntegerField(default=0)
    name = models.CharField(max_length=100, db_index=True)
    vat = models.CharField(max_length= 20, db_index=True)
    address = models.CharField(max_length=150)
    zip_code = models.IntegerField(max_length=6, null=True, db_index=True)
    state = models.CharField(max_length=50, null=True, db_index=True)
    city = models.CharField(max_length=50, null=True, db_index=True)
    telephone_number = models.CharField(max_length=15, null=True, default=' ')
    notes = models.TextField(null=True, default=' ')
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['customer_code']
        verbose_name_plural = u'Customers'

    def __unicode__(self):
        return u"%s, %s, %s" % (self.customer_code, self.name, self.vat)
