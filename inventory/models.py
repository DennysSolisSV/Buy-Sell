from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_userforeignkey.models.fields import UserForeignKey

class ClassModel(models.Model):
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "created_%(class)ss")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "updated_%(class)ss", blank=True, null=True)


    class Meta:
        abstract=True


class ClassModel2(models.Model):
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = UserForeignKey(auto_user_add=True, related_name="+")
    updated_by = UserForeignKey(auto_user_add=True, related_name="+")


    class Meta:
        abstract=True


class Category(ClassModel):
    description = models.CharField(max_length=100,  help_text='Description', unique=True)

    def __str__(self):
        return '{}'.format(self.description)

    class Meta: 
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse("inventory:category_edit", kwargs={"pk": self.pk})

    def del_absolute_url(self):
        return reverse("inventory:category_del", kwargs={"pk": self.pk})


class SubCategory(ClassModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategory")
    description = models.CharField(max_length=100,  help_text='Description')

    def __str__(self):
        return '{}:{}'.format(self.category.description, self.description)

    def save(self): # sobreescribiendo metodo save del modelo.
        self.description = self.description.upper()
        super(SubCategory, self).save()

    class Meta: 
        verbose_name_plural = 'Subcategories'
        unique_together = ('category', 'description') #unique compuesto
    
    def get_absolute_url(self):
        return reverse("inventory:subcategory_edit", kwargs={"pk": self.pk})


class Brand( ClassModel):
    description = models.CharField(max_length=100, help_text="brand description", unique=True)

    def __str__(self):
        return '{}'.format(self.description)
    
    def save(self):
        self.description = self.description.upper()
        super(Brand, self).save()

    class Meta:
        verbose_name_plural = "Brands"

    def get_absolute_url(self):
        return reverse("inventory:brand_edit", kwargs={"pk": self.pk})


class UnitOfMeasurement(ClassModel):
    description = models.CharField(max_length=100, help_text="Unit description", unique=True)

    def __str__(self):
        return '{}'.format(self.description)
    
    def save(self):
        self.description = self.description.upper()
        super(UnitOfMeasurement, self).save()

    class Meta:
        verbose_name_plural = "Unit of Measurements"

    def get_absolute_url(self):
        return reverse("inventory:unit_of_measurements_edit", kwargs={"pk": self.pk})


class Product(ClassModel):
    cod = models.CharField(
        max_length=20, 
        unique=True
    )

    barcode = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    last_purchase = models.DateField(null=True, blank=True)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    unit_measurements = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.description)

    def save(self):
        self.description = self.description.upper()
        super(Product, self).save()

    class Meta:
        verbose_name_plural = 'Products'
        unique_together = ('cod', 'barcode')