from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Category'
        verbose_name_plural = 'Categories'

    # def get_absolute_url(self):
    #     return reverse("categories", kwargs={})

    def __str__(self):
        return self.name.upper()


class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'SubCategory'
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.name.capitalize()

def directory_path(image, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}/{2}'.format(image.subcategory.category.name,
    image.subcategory.name,
     filename)
     
class Items(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True,)
    # label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to=directory_path , null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Items'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.discount_price:
            print('discount price not given')
            self.discount_price = self.price
        super(Items, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("single_product", kwargs={
            'slug': self.slug
        })

    def add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={
            'pk': self.id
        })

    def reduce_cart_url(self):
        return reverse('reduce_cart', kwargs={
            'pk': self.id
        })

    def remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={
            'pk': self.id
        })

    def add_to_wishlist_url(self):
        return reverse('add_to_wishlist', kwargs={
            'pk': self.id
        })

    def remove_from_wishlist_url(self):
        return reverse('remove_from_wishlist', kwargs={
            'pk': self.id
        })

    def reduce_from_cart_url(self):
        return reverse("reduce-from-cart", kwargs={
            'slug': self.slug
        })

    def discount(self):
        return self.price - self.discount_price
