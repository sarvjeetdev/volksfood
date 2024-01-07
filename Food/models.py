from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    feature = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)

    def __str__(self):
        return str(self.user)



class Food(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price  = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_images/')
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    feature = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    contactid = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50,null=True)
    pin_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.contactid)
    


class Order(models.Model):
    orderid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.orderid)
    

class OrderItem(models.Model):
    food_name = models.CharField(max_length=50)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"OrderID: {self.food_name} - {self.quantity} - {self.total} - {self.status}"
    



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Food', through='CartItem')

    def total_items(self):
        return self.items.count()

    def total_cost(self):
        return sum(item.food.cost for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey('Food', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def item_cost(self):
        return self.food.cost * self.quantity


'''
class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user
'''




