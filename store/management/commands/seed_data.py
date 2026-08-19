"""
Seed the database with sample products and download product images.
Run: python manage.py seed_data
"""
import os
import urllib.request
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from store.models import Category, Product


CATEGORIES = [
    {'name': 'Electronics', 'slug': 'electronics'},
    {'name': 'Clothing', 'slug': 'clothing'},
    {'name': 'Books', 'slug': 'books'},
    {'name': 'Home & Kitchen', 'slug': 'home-kitchen'},
    {'name': 'Sports', 'slug': 'sports'},
]

# image_url points to a specific free Unsplash photo (no API key needed for direct source URLs)
PRODUCTS = [
    # Electronics
    {
        'category': 'electronics',
        'name': 'Wireless Headphones',
        'slug': 'wireless-headphones',
        'description': 'Over ear headphones, bluetooth 5.0, about 20hrs battery. Good sound quality, comfortable for long sessions.',
        'price': '89.99',
        'stock': 25,
        'image_filename': 'headphones.jpg',
        'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80',
    },
    {
        'category': 'electronics',
        'name': 'Mechanical Keyboard',
        'slug': 'mechanical-keyboard',
        'description': 'TKL layout with blue switches. Has RGB but you can turn it off. Solid build, no wobble. USB-C cable included.',
        'price': '74.99',
        'stock': 15,
        'image_filename': 'keyboard.jpg',
        'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&q=80',
    },
    {
        'category': 'electronics',
        'name': 'USB-C Hub',
        'slug': 'usb-c-hub',
        'description': '7 ports - HDMI, 3x USB-A, SD card, microSD, and USB-C passthrough charging. Works fine with MacBook and most laptops.',
        'price': '34.99',
        'stock': 40,
        'image_filename': 'usb-hub.jpg',
        'image_url': 'https://images.unsplash.com/photo-1625895197185-efcec01cffe0?w=600&q=80',
    },
    {
        'category': 'electronics',
        'name': 'Smart Watch',
        'slug': 'smart-watch',
        'description': 'Tracks steps, heart rate, sleep. GPS built in. Battery lasts around 5-7 days depending on usage. Works with Android and iPhone.',
        'price': '129.99',
        'stock': 20,
        'image_filename': 'smartwatch.jpg',
        'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80',
    },
    {
        'category': 'electronics',
        'name': 'Bluetooth Speaker',
        'slug': 'bluetooth-speaker',
        'description': 'Small portable speaker, water resistant (IPX5). Decent bass for the size. Battery lasts ~10 hours. Good for outdoor use.',
        'price': '49.99',
        'stock': 30,
        'image_filename': 'speaker.jpg',
        'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&q=80',
    },

    # Clothing
    {
        'category': 'clothing',
        'name': 'Plain T-Shirt',
        'slug': 'plain-t-shirt',
        'description': 'Basic cotton t-shirt, slim fit. Washes well, doesnt shrink much. Available in a few colours.',
        'price': '19.99',
        'stock': 100,
        'image_filename': 'tshirt.jpg',
        'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80',
    },
    {
        'category': 'clothing',
        'name': 'Rain Jacket',
        'slug': 'rain-jacket',
        'description': 'Lightweight jacket, fully waterproof. Has a hood that packs into the collar. Good for hiking or just rainy days.',
        'price': '94.99',
        'stock': 18,
        'image_filename': 'jacket.jpg',
        'image_url': 'https://images.unsplash.com/photo-1544923246-77307dd654cb?w=600&q=80',
    },
    {
        'category': 'clothing',
        'name': 'Chino Trousers',
        'slug': 'chino-trousers',
        'description': 'Slim fit chinos with a bit of stretch. Smart enough for work, comfortable enough for weekends. True to size.',
        'price': '44.99',
        'stock': 50,
        'image_filename': 'chinos.jpg',
        'image_url': 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=600&q=80',
    },

    # Books
    {
        'category': 'books',
        'name': 'Clean Code',
        'slug': 'clean-code',
        'description': 'Book by Robert C. Martin about writing readable code. Good if you want to improve your coding habits. Some chapters are better than others.',
        'price': '29.99',
        'stock': 35,
        'image_filename': 'book-cleancode.jpg',
        'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&q=80',
    },
    {
        'category': 'books',
        'name': 'The Pragmatic Programmer',
        'slug': 'the-pragmatic-programmer',
        'description': 'Covers a lot of general software development advice. Easy to read, not too technical. Worth having on the shelf.',
        'price': '27.99',
        'stock': 28,
        'image_filename': 'book-pragmatic.jpg',
        'image_url': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=600&q=80',
    },
    {
        'category': 'books',
        'name': 'Designing Data-Intensive Applications',
        'slug': 'designing-data-intensive-applications',
        'description': 'Goes deep into databases, distributed systems, and data pipelines. Dense but very useful if you work on backend systems.',
        'price': '39.99',
        'stock': 20,
        'image_filename': 'book-ddia.jpg',
        'image_url': 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=600&q=80',
    },

    # Home & Kitchen
    {
        'category': 'home-kitchen',
        'name': 'Pour Over Coffee Kit',
        'slug': 'pour-over-coffee-kit',
        'description': 'Includes the glass dripper, a gooseneck kettle and a small kitchen scale. Makes noticeably better coffee than a standard machine.',
        'price': '54.99',
        'stock': 22,
        'image_filename': 'coffee-kit.jpg',
        'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80',
    },
    {
        'category': 'home-kitchen',
        'name': 'Bamboo Cutting Boards (set of 3)',
        'slug': 'bamboo-cutting-boards',
        'description': 'Three sizes - small, medium, large. Light and easy to clean. Dont use them in the dishwasher though, they warp.',
        'price': '24.99',
        'stock': 60,
        'image_filename': 'cutting-boards.jpg',
        'image_url': 'https://images.unsplash.com/photo-1590794056226-79ef3a8147e1?w=600&q=80',
    },
    {
        'category': 'home-kitchen',
        'name': 'Cast Iron Skillet',
        'slug': 'cast-iron-skillet',
        'description': '10 inch skillet, pre-seasoned. Gets better the more you use it. Heavy but worth it. Works on gas, electric and induction.',
        'price': '39.99',
        'stock': 15,
        'image_filename': 'skillet.jpg',
        'image_url': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&q=80',
    },

    # Sports
    {
        'category': 'sports',
        'name': 'Yoga Mat',
        'slug': 'yoga-mat',
        'description': '6mm thick, non-slip. Has faint alignment lines printed on it. Comes with a carry strap. Good for home workouts.',
        'price': '34.99',
        'stock': 45,
        'image_filename': 'yoga-mat.jpg',
        'image_url': 'https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=600&q=80',
    },
    {
        'category': 'sports',
        'name': 'Adjustable Dumbbells',
        'slug': 'adjustable-dumbbells',
        'description': 'Dial to select weight from 5 to 52.5 lbs. Saves a lot of space compared to a full rack. Takes a second to adjust but works well.',
        'price': '219.99',
        'stock': 10,
        'image_filename': 'dumbbells.jpg',
        'image_url': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80',
    },
    {
        'category': 'sports',
        'name': 'Water Bottle',
        'slug': 'water-bottle',
        'description': '750ml, BPA free. Squeeze bottle with a bite valve. Fits most cup holders. Good for running or the gym.',
        'price': '14.99',
        'stock': 80,
        'image_filename': 'water-bottle.jpg',
        'image_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&q=80',
    },
]


def download_image(url, filename, dest_dir):
    """Download image from url and save to dest_dir/filename. Returns the relative path or None on failure."""
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)

    if os.path.exists(dest_path):
        return f'products/{filename}'

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(dest_path, 'wb') as f:
                f.write(resp.read())
        return f'products/{filename}'
    except Exception as e:
        return None


class Command(BaseCommand):
    help = 'Seed database with sample categories and products'

    def handle(self, *args, **options):
        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')

        self.stdout.write('Creating categories...')
        cat_map = {}
        for c in CATEGORIES:
            obj, created = Category.objects.get_or_create(slug=c['slug'], defaults={'name': c['name']})
            cat_map[c['slug']] = obj
            if created:
                self.stdout.write(f'  + {obj.name}')

        self.stdout.write('Creating products...')
        for p in PRODUCTS:
            cat = cat_map.get(p['category'])

            # try to download the image
            image_path = None
            if p.get('image_url') and p.get('image_filename'):
                self.stdout.write(f'  downloading image for {p["name"]}...', ending=' ')
                image_path = download_image(p['image_url'], p['image_filename'], media_products_dir)
                if image_path:
                    self.stdout.write('ok')
                else:
                    self.stdout.write('failed (no image)')

            product, created = Product.objects.get_or_create(
                slug=p['slug'],
                defaults={
                    'name': p['name'],
                    'description': p['description'],
                    'price': p['price'],
                    'stock': p['stock'],
                    'category': cat,
                    'available': True,
                    'image': image_path or '',
                }
            )

            # update image if product already exists but has no image
            if not created and image_path and not product.image:
                product.image = image_path
                product.save()

            if created:
                self.stdout.write(f'  + {p["name"]}')

        self.stdout.write('Creating admin user...')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@store.dev', 'admin123')
            self.stdout.write('  username: admin / password: admin123')
        else:
            self.stdout.write('  admin already exists, skipping')

        self.stdout.write(self.style.SUCCESS('Done.'))
