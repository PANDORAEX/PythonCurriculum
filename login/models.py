from django.db import models


class User(models.Model):
    USERID = models.CharField(max_length=8, primary_key=True)
    PASSWORD = models.CharField(max_length=50)


class Status(models.Model):
    STATUS_CODE = models.CharField(max_length=1, primary_key=True)
    STATUS_NAME = models.CharField(max_length=20)

    def __str__(self):
        return self.STATUS_NAME


class ProjectType(models.Model):
    PROTYPE_CODE = models.CharField(primary_key=True, max_length=2)
    PROTYPE_NAME = models.CharField(max_length=20)

    def __str__(self):
        return self.PROTYPE_NAME


class Language(models.Model):
    LANGUAGE_CODE = models.CharField(max_length=2, primary_key=True)
    LANGUAGE_NAME = models.CharField(max_length=20)

    def __str__(self):
        return self.LANGUAGE_NAME


class Project(models.Model):
    PROJECT_ID = models.DecimalField(max_digits=4, decimal_places=0, primary_key=True)
    START_DATE = models.DateField()
    PROJECT_NO = models.CharField(max_length=15)
    PROJECT_NAME = models.CharField(max_length=30)
    PROTYPE_CODE = models.ForeignKey(ProjectType, on_delete=models.PROTECT, db_column='PROTYPE_CODE')
    LANGUAGE_CODE = models.ForeignKey(Language, on_delete=models.PROTECT, db_column='LANGUAGE_CODE')
    SUMMARY = models.CharField(max_length=255)
    STATUS_CODE = models.ForeignKey(Status, on_delete=models.PROTECT, db_column='STATUS_CODE')
    CUSTOMER = models.CharField(max_length=20, null=True)
    CHARGE = models.CharField(max_length=20, null=True)
    REVIEWER = models.CharField(max_length=20, null=True)
    RELEASE_DATE = models.DateField(null=True)
    REMARKS = models.CharField(max_length=255, null=True)
