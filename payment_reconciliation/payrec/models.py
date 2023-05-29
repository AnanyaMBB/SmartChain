from django.db import models


class Entity(models.Model):
    bID = models.AutoField(primary_key=True, blank=False, null=False)
    bname = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return str(self.bname) + ":" + str(self.address)


class ProductsList(models.Model):
    productID = models.AutoField(primary_key=True, blank=False, null=False)
    productName = models.CharField(max_length=200)
    entityID = models.IntegerField()

    def __str__(self):
        return str(self.productID) + ":" + str(self.entityID)


class involvedEntity(models.Model):
    productID = models.IntegerField()
    entityID = models.IntegerField()

    def __str__(self):
        return str(self.productID) + ":" + str(self.entityID)
