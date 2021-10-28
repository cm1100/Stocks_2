from django.db import models

# Create your models here.


class Stock(models.Model):

    name = models.CharField(max_length=200)
    bse = models.CharField(max_length=100,null=True)
    nse = models.CharField(max_length=100,null=True)
    isin_num = models.CharField(max_length=200,null=True)
    mc_id = models.CharField(max_length=100,null=True,default=None)


    def __str__(self):
        return self.name


class LookupStock(models.Model):

    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    url = models.URLField()


    def __str__(self):
        return self.stock.name


class OHCL(models.Model):

    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    date = models.DateField()
    open_p = models.FloatField()
    high_p = models.FloatField()
    low_p = models.FloatField()
    close_p = models.FloatField()
    volume = models.FloatField()



class News(models.Model):

    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    headline = models.CharField(max_length=300,null=True)
    date_time = models.DateTimeField(null=True)
    description = models.CharField(max_length=400,null=True)


    def __str__(self):
        return self.stock.name


class Indices(models.Model):

    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class OHCLI(models.Model):

    indice = models.ForeignKey(Indices,on_delete=models.CASCADE)
    date = models.DateField()
    open_p = models.FloatField()
    high_p = models.FloatField()
    low_p = models.FloatField()
    close_p = models.FloatField()



    def __str__(self):
        return self.indice.name




