from django.db import models

# Create your models here.

class Senator(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Committee(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Bill(models.Model):
    bill_id = models.CharField(max_length=10, primary_key=True)
    bill_number = models.CharField(max_length=10)
    bill_name = models.CharField(max_length=300)
    senator_primary_sponsor = models.ForeignKey(Senator, null=True, related_name="SenSponsor")
    committee_primary_sponsor = models.ForeignKey(Committee, null=True, related_name="CommSponsor")
    co_sponsors = models.ManyToManyField(Senator, related_name="CoSponsors")
    introduction_date = models.DateField() 
    status = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.bill_number

class History(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    date = models.DateField()
    action = models.CharField(max_length=200)
    journal_page = models.CharField(max_length=50)

class ConsideredAmendment(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, blank=True)
    link = models.CharField(max_length=200)

class ProposedAmendment(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    proposer = models.CharField(max_length=100)
    status = models.CharField(max_length=50, blank=True)
    link = models.CharField(max_length=200)

class Transcript(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)

class TextCopy(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)

class AdditionalInfo(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
