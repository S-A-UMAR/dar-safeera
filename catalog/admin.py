from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
from .models import Category, Product, ProductImage
from .widgets import ColorPickerWidget


# ── Forms ─────────────────────────────────────────────────────────────────────

class ProductAdminForm(forms.ModelForm):
    available_colors = forms.CharField(
        widget=ColorPickerWidget(),
        required=False,
        help_text='Select all available colors for this product.',
    )

    class Meta:
        model = Product
        fields = '__all__'


# ── Inlines ───────────────────────────────────────────────────────────────────

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ('image', 'image_preview', 'color', 'is_primary', 'alt_text', 'order')
    readonly_fields = ('image_preview',)
    ordering = ('-is_primary', 'order')

    def image_preview(self, obj):
        if obj.image and obj.url:
            return format_html(
                '<img src="{}" style="height:80px;width:60px;object-fit:cover;'
                'border-radius:6px;border:1px solid #333;" />',
                obj.url,
            )
        return mark_safe('<span style="color:#888;font-size:11px;">No image yet</span>')
    image_preview.short_description = 'Preview'


# ── Admin: Category ───────────────────────────────────────────────────────────

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def product_count(self, obj):
        count = obj.products.count()
        return format_html(
            '<span style="background:#c9a96e22;color:#c9a96e;padding:2px 8px;'
            'border-radius:20px;font-weight:600;">{}</span>',
            count,
        )
    product_count.short_description = 'Products'


# ── Admin: Product ────────────────────────────────────────────────────────────

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('thumbnail', 'name', 'category', 'price_display',
                    'color_swatches', 'is_featured', 'is_available', 'image_count')
    list_display_links = ('thumbnail', 'name')
    list_filter = ('category', 'is_featured', 'is_available')
    list_editable = ('is_featured', 'is_available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    save_on_top = True

    fieldsets = (
        ('✦ Product Info', {
            'fields': ('name', 'slug', 'category', 'description', 'price'),
        }),
        ('✦ Options', {
            'fields': ('available_sizes', 'available_colors', 'is_featured', 'is_available'),
        }),
    )

    class Media:
        css = {'all': ('css/color_picker.css',)}
        js = ('js/color_picker.js',)

    # ── List display helpers ──────────────────────────────────────────────────

    def thumbnail(self, obj):
        img = obj.get_primary_image()
        if img and img.image and img.url:
            return format_html(
                '<img src="{}" style="height:56px;width:44px;object-fit:cover;'
                'border-radius:6px;border:1px solid #2e2e30;" />',
                img.url,
            )
        return mark_safe(
            '<div style="height:56px;width:44px;background:#1e1e1e;border-radius:6px;'
            'display:flex;align-items:center;justify-content:center;'
            'font-size:9px;color:#555;border:1px solid #2e2e30;">No img</div>'
        )
    thumbnail.short_description = ''

    def price_display(self, obj):
        return format_html(
            '<span style="color:#c9a96e;font-weight:600;">{}</span>',
            obj.formatted_price(),
        )
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'

    def color_swatches(self, obj):
        colors = obj.get_colors_list()
        if not colors:
            return '—'
        swatches = []
        for color in colors[:6]:
            # Simple hex lookup from name, fallback to a neutral
            hex_map = {
                'midnight black': '#0a0a0a', 'charcoal': '#2c2c2c',
                'warm white': '#faf8f5', 'ivory cream': '#f5f0e8',
                'blush rose': '#e8c5b5', 'dusty mauve': '#c4a0a0',
                'warm gold': '#c9a96e', 'champagne': '#f7e7ce',
                'forest green': '#2d5a3d', 'sage': '#7a9e7e',
                'midnight navy': '#1a2744', 'slate blue': '#4a6fa5',
                'bordeaux': '#6b2737', 'dusty rose': '#d4a0a0',
                'camel': '#c19a6b', 'sand': '#d2b48c',
                'mocha': '#6f4e37', 'pearl grey': '#d8d0c8',
                'lavender mist': '#c5b8d4', 'deep plum': '#4a1942',
                'black': '#0a0a0a', 'navy': '#1a2744', 'white': '#faf8f5',
            }
            bg = hex_map.get(color.lower(), color if color.startswith('#') else '#888')
            border = '1px solid #333' if bg in ('#faf8f5', '#f5f0e8', '#f7e7ce', '#d8d0c8') else '1px solid transparent'
            swatches.append(
                f'<span title="{color}" style="display:inline-block;width:18px;height:18px;'
                f'border-radius:50%;background:{bg};border:{border};'
                f'margin-right:3px;vertical-align:middle;"></span>'
            )
        extra = f'<span style="color:#888;font-size:11px;">+{len(colors)-6}</span>' if len(colors) > 6 else ''
        return mark_safe(''.join(swatches) + extra)
    color_swatches.short_description = 'Colors'

    def image_count(self, obj):
        count = obj.images.count()
        if count == 0:
            color = '#e74c3c'
        elif count < 3:
            color = '#f39c12'
        else:
            color = '#27ae60'
        return format_html(
            '<span style="color:{};font-weight:600;">{} photo{}</span>',
            color, count, 's' if count != 1 else '',
        )
    image_count.short_description = 'Photos'


# ── Admin: ProductImage ───────────────────────────────────────────────────────

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'product', 'is_primary', 'order', 'alt_text')
    list_filter = ('product', 'is_primary')
    list_editable = ('is_primary', 'order')
    search_fields = ('product__name', 'alt_text')

    def image_preview(self, obj):
        if obj.image and obj.url:
            return format_html(
                '<img src="{}" style="height:64px;width:50px;object-fit:cover;'
                'border-radius:6px;border:1px solid #333;" />',
                obj.url,
            )
        return '—'
    image_preview.short_description = 'Preview'
