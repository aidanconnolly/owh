from django.db import models

# Create your models here.
class Legislature(models.Model):
    legislature_id = models.CharField(max_length=10, primary_key=True)
    legislature = models.CharField(max_length=5)
    session = models.CharField(max_length=1)

class Introducer(models.Model):
    introducer_id = models.CharField(max_length=10, primary_key=True)
    introducer_name = models.CharField(max_length=50)
    def __str__(self):
        return self.introducer_name

class Bill(models.Model):
    bill_id = models.CharField(max_length=10, primary_key=True)
    bill_number = models.CharField(max_length=10)
    bill_name = models.CharField(max_length=100)
    introducer_id = models.ManyToManyField(Introducer)
    introduction_date = models.DateField() 
    status = models.CharField(max_length=50)
    def __str__(self):
        return self.bill_number

class History(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    date = models.DateField()
    action = models.CharField(max_length=100)
    journal_page = models.CharField(max_length=50)

class Amendment(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    proposer = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

class Transcript(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=100)

class TextCopy(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=100)

class AdditionalInfo(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=100)
