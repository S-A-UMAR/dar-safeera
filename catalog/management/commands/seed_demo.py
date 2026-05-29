import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from catalog.models import Category, Product, ProductImage


PRODUCTS = [
    {
        'name': 'Al Noor Abaya',
        'category': 'Classic',
        'description': 'A timeless open abaya in premium matte crepe. Flowing silhouette with subtle hand-stitched details at the cuffs and hem. Perfect for everyday elegance.',
        'price': 85000,
        'sizes': 'S, M, L, XL, XXL',
        'colors': 'Midnight Black, Midnight Navy, Charcoal',
        'featured': True,
        'placeholder': 'placeholder_1.jpg',
        'primary_color': 'Midnight Black',
        'extra_images': []
    },
    {
        'name': 'Safiya Embroidered Abaya',
        'category': 'Embroidered',
        'description': 'Intricately embroidered floral motifs adorn the sleeves and neckline of this exquisite abaya. Crafted from lightweight chiffon over a satin lining.',
        'price': 120000,
        'sizes': 'S, M, L, XL',
        'colors': 'Midnight Black, Midnight Navy',
        'featured': True,
        'placeholder': 'placeholder_2.jpg',
        'primary_color': 'Midnight Black',
        'extra_images': []
    },
    {
        'name': 'Lailah Wrap Abaya',
        'category': 'Contemporary',
        'description': 'A modern wrap-style abaya with a draped front panel and wide sleeves. Made from premium georgette that moves beautifully with every step.',
        'price': 95000,
        'sizes': 'S, M, L, XL, XXL',
        'colors': 'Dusty Rose, Ivory Cream, Sage',
        'featured': True,
        'placeholder': 'placeholder_3.jpg',
        'primary_color': 'Dusty Rose',
        'extra_images': [
            {'file': 'placeholder_33.jpg', 'color': 'Ivory Cream'}
        ]
    },
    {
        'name': 'Nura Belted Abaya',
        'category': 'Contemporary',
        'description': 'An elegant belted abaya that cinches at the waist for a refined silhouette. Features a concealed zip closure and wide bishop sleeves in soft modal fabric.',
        'price': 110000,
        'sizes': 'XS, S, M, L, XL',
        'colors': 'Camel, Midnight Black, Ivory Cream',
        'featured': True,
        'placeholder': 'placeholder_4.jpg',
        'primary_color': 'Camel',
        'extra_images': [
            {'file': 'placeholder_44.jpg', 'color': 'Midnight Black'}
        ]
    },
    {
        'name': 'Hana Pearl Abaya',
        'category': 'Embroidered',
        'description': 'Adorned with hand-sewn pearl and crystal embellishments along the front panel. A statement piece for weddings, Eid, and special occasions.',
        'price': 175000,
        'sizes': 'S, M, L, XL',
        'colors': 'Warm White, Champagne, Midnight Black',
        'featured': True,
        'placeholder': 'placeholder_5.jpg',
        'primary_color': 'Warm White',
        'extra_images': [
            {'file': 'placeholder_55.jpg', 'color': 'Champagne'}
        ]
    },
    {
        'name': 'Zara Butterfly Abaya',
        'category': 'Classic',
        'description': 'The butterfly abaya silhouette — dramatic wide sleeves that drape into elegant wings when arms are raised. Crafted from premium Japanese fabric.',
        'price': 90000,
        'sizes': 'S, M, L, XL, XXL',
        'colors': 'Midnight Black, Bordeaux, Forest Green',
        'featured': True,
        'placeholder': 'placeholder_6.jpg',
        'primary_color': 'Midnight Black',
        'extra_images': [
            {'file': 'placeholder_66.jpg', 'color': 'Bordeaux'}
        ]
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with 6 demo Dar Safeera products and placeholder images linked to colors'

    def handle(self, *args, **options):
        self.stdout.write('🌸 Resetting and Seeding Dar Safeera demo products...')

        # Flush tables to avoid duplicates
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        placeholder_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'placeholders')

        created_categories = {}
        for data in PRODUCTS:
            # Get or create category
            cat_name = data['category']
            if cat_name not in created_categories:
                cat, _ = Category.objects.get_or_create(name=cat_name)
                created_categories[cat_name] = cat
            category = created_categories[cat_name]

            # Create product
            product = Product.objects.create(
                name=data['name'],
                category=category,
                description=data['description'],
                price=data['price'],
                available_sizes=data['sizes'],
                available_colors=data['colors'],
                is_featured=data['featured'],
                is_available=True,
            )

            # 1. Add primary image
            src = os.path.join(placeholder_dir, data['placeholder'])
            dst_name = f"{product.slug}_{data['placeholder']}"

            if os.path.exists(src):
                with open(src, 'rb') as f:
                    product_image = ProductImage(
                        product=product,
                        is_primary=True,
                        color=data['primary_color'],
                        alt_text=f'{product.name} – {data["primary_color"]} variant',
                        order=0
                    )
                    product_image.image.save(dst_name, File(f))
                    product_image.save()
                self.stdout.write(f'  ✅ Created: {product.name} (Primary: {data["primary_color"]})')
            else:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠️ Placeholder image not found at {src}')
                )

            # 2. Add extra/variant images
            for order_idx, extra in enumerate(data['extra_images'], start=1):
                src_extra = os.path.join(placeholder_dir, extra['file'])
                dst_extra_name = f"{product.slug}_{extra['file']}"

                if os.path.exists(src_extra):
                    with open(src_extra, 'rb') as f:
                        product_image = ProductImage(
                            product=product,
                            is_primary=False,
                            color=extra['color'],
                            alt_text=f'{product.name} – {extra["color"]} variant',
                            order=order_idx
                        )
                        product_image.image.save(dst_extra_name, File(f))
                        product_image.save()
                    self.stdout.write(f'     └─ Added extra variant image for: {extra["color"]}')

        self.stdout.write(self.style.SUCCESS('\n✨ Done! Visit http://127.0.0.1:8000 to see your store.'))
        self.stdout.write(self.style.SUCCESS('   Admin: http://127.0.0.1:8000/admin'))
