from django.db import models

# Create your models here.
class  Visitor(models.Model):
    ename=models.CharField(max_length=20,default=None)
    eemail=models.EmailField(max_length=30)
  
    epass=models.TextField(max_length=10)
    eimage=models.ImageField()
    
    class Meta:
        db_table='employee'

class ProductDetail(models.Model):
    
    pid=models.IntegerField()
    pimage=models.ImageField(upload_to='C:\\venv\Ecommerce\static\media')
    pdetail=models.TextField(max_length=100)
    pprice=models.DecimalField(max_digits=8, decimal_places=2)
    ptitle=models.TextField(max_length=20,default="non")
    class Meta:
        db_table='product'

class Cartdetail(models.Model):
    pid=models.IntegerField()
    pimage=models.ImageField(upload_to='C:\\venv\Ecommerce\static\media')
    pdetail=models.TextField(max_length=100)
    pprice=models.DecimalField(max_digits=8, decimal_places=2)
    ptitle=models.TextField(max_length=20,default="non")
    pnumber=models.IntegerField(default=1)
    userid=models.IntegerField(default=None)

class Order(models.Model):
    pid=models.IntegerField()
    ptitle=models.CharField(max_length=10)
    pprice=models.DecimalField(max_digits=8, decimal_places=2)
    pnumber=models.IntegerField()
    ename=models.CharField(max_length=20)
    eemail=models.EmailField(max_length=30)
    userid=models.IntegerField(default=None)
    order_status = models.BooleanField(default=False)

