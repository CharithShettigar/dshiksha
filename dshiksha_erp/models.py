from django.db import models
import uuid

# Create your models here.

class State(models.Model):
    StateID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    StateName = models.CharField(max_length=50)


class District(models.Model):
    DistrictID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    DistrictName = models.CharField(max_length=50)
    State = models.ForeignKey(State, on_delete=models.CASCADE)


class Taluk(models.Model):
    TalukID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    TalukName = models.CharField(max_length=50)
    District = models.ForeignKey(District, on_delete=models.CASCADE)


class Village(models.Model):
    VillageID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    VillageName = models.CharField(max_length=50)
    Taluk = models.ForeignKey(Taluk, on_delete=models.CASCADE)
