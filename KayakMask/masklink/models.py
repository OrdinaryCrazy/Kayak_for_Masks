from django.db import models

# Create your models here.

class MaskInfo(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    brand = models.CharField(max_length=256, verbose_name="manufacture")
    size = models.CharField(max_length=256, verbose_name="size")
    price = models.FloatField(verbose_name="price")
    # available = models.IntegerField(verbose_name='avai')
    available = models.CharField(max_length=256, verbose_name='avai')
    link = models.CharField(max_length=256, verbose_name="purchasing link")
    fe = models.FloatField(verbose_name="filtration efficiency")
    # time = models.IntegerField(verbose_name="time")
    def __str__(self) -> str:
        return "{}-{}-{}".format(self.name, self.brand, self.size)
    class Meta:
        verbose_name = "Mask for Kids"