from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def get_default_category_id():
    default_category, created = Category.objects.get_or_create(slug="uncategorized", defaults={"title": "Uncategorized"})
    return default_category.id


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(db_index=True, default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=get_default_category_id)
    inventory = models.SmallIntegerField()

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user','menuitem')

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
#     status = models.BooleanField(db_index=True, default=0)
#     total = models.DecimalField(max_digits=6, decimal_places=2)
#     date = models.DateField(db_index=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="delivery_orders",
        null=True,
        limit_choices_to={'groups__name': "Delivery crew"}  # Filter only delivery crew
    )
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)

    def save(self, *args, **kwargs):
        # Ensure the selected delivery crew user is in the 'Delivery Crew' group
        if self.delivery_crew and not self.delivery_crew.groups.filter(name="Delivery crew").exists():
            raise ValidationError("Selected user is not part of the Delivery Crew group.")
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order','menuitem')