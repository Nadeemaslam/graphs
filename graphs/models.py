from django.db import models

class SaleData(models.Model):
	day = models.TextField(max_length=10,null=True)
	month = models.TextField(max_length=20)
	sale = models.IntegerField()

	def __unicode__(self):
		return self.month



