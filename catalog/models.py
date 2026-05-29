from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price in NGN')
    available_sizes = models.CharField(max_length=200, default='S, M, L, XL, XXL',
                                       help_text='Comma-separated sizes, e.g. S, M, L, XL')
    available_colors = models.CharField(max_length=200, default='Black',
                                        help_text='Comma-separated colors, e.g. Black, Navy, Beige')
    is_featured = models.BooleanField(default=False, help_text='Show on homepage')
    is_available = models.BooleanField(default=True, help_text='Hide if sold out')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_sizes_list(self):
        return [s.strip() for s in self.available_sizes.split(',')]

    def get_colors_list(self):
        return [c.strip() for c in self.available_colors.split(',')]

    def get_primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()

    def formatted_price(self):
        return f'₦{self.price:,.0f}'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', help_text='Upload product photo')
    is_primary = models.BooleanField(default=False, help_text='Main image shown in listings')
    color = models.CharField(
        max_length=100,
        blank=True,
        help_text='Color name this image represents (e.g. "Midnight Black"). Leave blank if not color-specific.',
    )
    alt_text = models.CharField(max_length=200, blank=True, help_text='Describe the image for accessibility')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_primary', 'order']

    def save(self, *args, **kwargs):
        # Ensure only one primary per product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        # Auto alt_text
        if not self.alt_text:
            suffix = f' – {self.color}' if self.color else ' – product image'
            self.alt_text = f'{self.product.name}{suffix}'
        super().save(*args, **kwargs)

    def __str__(self):
        color_label = f' [{self.color}]' if self.color else ''
        return f'{self.product.name}{color_label} – image {self.order}'
