import os
import shutil
from PIL import Image, ImageDraw, ImageFont

# Path configuration
static_placeholder_dir = '/Users/S.A/Desktop/darsafeera/static/images/placeholders'
os.makedirs(static_placeholder_dir, exist_ok=True)

# 1. Use the AI generated image as placeholder 1
ai_img_src = '/Users/s.a/.gemini/antigravity/brain/1e6c48ca-c05d-4246-adac-843c94bffee0/abaya_placeholder_1_1780051725969.png'
p1_dst = os.path.join(static_placeholder_dir, 'placeholder_1.jpg')

if os.path.exists(ai_img_src):
    try:
        # Convert png to jpg and save to static folder
        img = Image.open(ai_img_src)
        rgb_img = img.convert('RGB')
        rgb_img.save(p1_dst, 'JPEG', quality=90)
        print("✓ Converted and copied AI generated image to placeholder_1.jpg")
    except Exception as e:
        print(f"Error processing AI image: {e}")
else:
    print("AI image not found, will generate a beautiful default.")

# 2. Programmatically generate 6 premium, color-matched placeholders
# This ensures we have high-quality, beautiful editorial visuals for all products
placeholders_config = [
    {
        'filename': 'placeholder_1.jpg',
        'color': '#2C2C2C', # Charcoal
        'text_color': '#FAF7F2',
        'label': 'AL NOOR ABAYA',
        'sub': 'Premium Crepe Collection',
        'bg_gradient': ('#3D3D3D', '#1C1C1C')
    },
    {
        'filename': 'placeholder_2.jpg',
        'color': '#1E2530', # Midnight Navy
        'text_color': '#FAF7F2',
        'label': 'SAFIYA EMBROIDERED',
        'sub': 'Artisanal Chiffon',
        'bg_gradient': ('#2A3240', '#0F131A')
    },
    {
        'filename': 'placeholder_3.jpg',
        'color': '#D9B4A7', # Dusty Rose
        'text_color': '#2C2C2C',
        'label': 'LAILAH WRAP',
        'sub': 'Georgette Contemporary',
        'bg_gradient': ('#E6C5B8', '#C9A093')
    },
    {
        'filename': 'placeholder_4.jpg',
        'color': '#C5A687', # Camel
        'text_color': '#2C2C2C',
        'label': 'NURA BELTED',
        'sub': 'Modal Elegance',
        'bg_gradient': ('#D6BBA0', '#B49372')
    },
    {
        'filename': 'placeholder_5.jpg',
        'color': '#EBE7E0', # Champagne Ivory
        'text_color': '#2C2C2C',
        'label': 'HANA PEARL ABAYA',
        'sub': 'Eid & Occasion Wear',
        'bg_gradient': ('#FAF6F0', '#DDD7CE')
    },
    {
        'filename': 'placeholder_6.jpg',
        'color': '#2C3A32', # Forest Green / Emerald
        'text_color': '#FAF7F2',
        'label': 'ZARA BUTTERFLY',
        'sub': 'Dramatic Silhouette',
        'bg_gradient': ('#3A4D42', '#1C2620')
    }
]

# Generate placeholders
for i, config in enumerate(placeholders_config):
    filename = config['filename']
    filepath = os.path.join(static_placeholder_dir, filename)
    
    # If placeholder_1.jpg was already successfully copied from the beautiful AI image, skip generating a procedural replacement
    if i == 0 and os.path.exists(p1_dst):
        continue
        
    print(f"Generating premium placeholder: {filename}")
    
    # Create image with nice standard vertical editorial aspect ratio (600x800)
    w, h = 600, 800
    img = Image.new('RGB', (w, h), color=config['color'])
    draw = ImageDraw.Draw(img)
    
    # Draw an elegant gradient background
    c1 = Image.new('RGB', (w, h), color=config['bg_gradient'][0])
    c2 = Image.new('RGB', (w, h), color=config['bg_gradient'][1])
    for y in range(h):
        # Linear interpolation factor
        factor = y / h
        r = int(c1.getpixel((0,0))[0] * (1 - factor) + c2.getpixel((0,0))[0] * factor)
        g = int(c1.getpixel((0,0))[1] * (1 - factor) + c2.getpixel((0,0))[1] * factor)
        b = int(c1.getpixel((0,0))[2] * (1 - factor) + c2.getpixel((0,0))[2] * factor)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # Draw delicate gold borders
    draw.rectangle([20, 20, w-20, h-20], outline='#C9A96E', width=1)
    draw.rectangle([25, 25, w-25, h-25], outline='#C9A96E', width=1)
    
    # Render typography using default system font beautifully scaled
    # Draw logo header
    draw.text((w/2, 100), "DAR SAFEERA", fill='#C9A96E', anchor="mm")
    
    # Draw product name
    draw.text((w/2, h/2 - 20), config['label'], fill=config['text_color'], anchor="mm")
    # Draw collection subtitle
    draw.text((w/2, h/2 + 20), config['sub'], fill='#C9A96E', anchor="mm")
    
    # Draw minimal sign off
    draw.text((w/2, h - 100), "LUXURY MODEST WEAR", fill='#C9A96E', anchor="mm")
    
    # Save image
    img.save(filepath, 'JPEG', quality=95)
    print(f"✓ Generated {filename}")

print("\nAll placeholder assets initialized successfully!")
