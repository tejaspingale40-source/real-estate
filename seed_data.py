import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import Property, PropertyImage, Amenity
from enquiries.models import Enquiry

# 1. Create Amenities
amenities_list = [
    ("Parking", "fa-parking"),
    ("Garden", "fa-tree"),
    ("Security", "fa-shield"),
    ("Water Supply", "fa-tint"),
    ("Electricity", "fa-bolt"),
    ("Road Access", "fa-road"),
    ("Gym", "fa-dumbbell"),
    ("Swimming Pool", "fa-swimming-pool"),
    ("Lift", "fa-elevator"),
]

amenity_objs = []
for name, icon in amenities_list:
    obj, _ = Amenity.objects.get_or_create(name=name, defaults={'icon': icon})
    amenity_objs.append(obj)

print(f"Created {len(amenity_objs)} Amenities")

# Copy placeholder image for sample properties
placeholder_src = r'e:\real-estate\static\images\banners\property_placeholder.jpg'
media_dest_dir = r'e:\real-estate\media\properties\images'
os.makedirs(media_dest_dir, exist_ok=True)
dest_img_path = os.path.join(media_dest_dir, 'sample_property.jpg')
shutil.copy(placeholder_src, dest_img_path)

# 2. Create Sample Properties
sample_properties = [
    {
        'title': 'Luxury 3 BHK Villa in Solapur',
        'description': 'A beautiful 3 BHK luxury independent villa located in VIP Road, Solapur. Comes with private swimming pool, landscaped garden, modular kitchen, and double covered car parking.',
        'price': 7500000,
        'location': 'Solapur',
        'address': 'Plot 42, VIP Road, Near Park Stadium, Solapur',
        'property_type': 'Villa',
        'purpose': 'Sale',
        'bedrooms': 3,
        'bathrooms': 3,
        'area': 2200,
        'parking': True,
        'furnished': 'Furnished',
        'status': 'Available',
        'featured': True,
    },
    {
        'title': 'Modern 2 BHK Apartment in Kothrud',
        'description': 'Spacious and well-ventilated 2 BHK apartment in prime Kothrud locality, Pune. Close to top schools, metro station, and tech parks. Includes 24/7 security and power backup.',
        'price': 6500000,
        'location': 'Pune',
        'address': 'Flat 402, Royal Residency, Kothrud, Pune',
        'property_type': 'Apartment',
        'purpose': 'Sale',
        'bedrooms': 2,
        'bathrooms': 2,
        'area': 1150,
        'parking': True,
        'furnished': 'Semi Furnished',
        'status': 'Available',
        'featured': True,
    },
    {
        'title': 'Premium Commercial Office Space',
        'description': 'Fully furnished corporate office space on main road, Solapur. Ideal for IT companies, consultancies, or banking branches. Equipped with high-speed elevator and central AC.',
        'price': 45000,
        'location': 'Solapur',
        'address': '3rd Floor, Commercial Tower, Station Road, Solapur',
        'property_type': 'Commercial',
        'purpose': 'Rent',
        'bedrooms': 0,
        'bathrooms': 2,
        'area': 1800,
        'parking': True,
        'furnished': 'Furnished',
        'status': 'Available',
        'featured': True,
    },
    {
        'title': 'Grand 4 BHK Independent House',
        'description': 'Exclusive 4 BHK bungalow with terrace garden and servant quarters. Premium marble flooring and automated security gates.',
        'price': 12500000,
        'location': 'Solapur',
        'address': 'Bungalow No. 12, Green Acres Colony, Solapur',
        'property_type': 'House',
        'purpose': 'Sale',
        'bedrooms': 4,
        'bathrooms': 4,
        'area': 3500,
        'parking': True,
        'furnished': 'Furnished',
        'status': 'Available',
        'featured': False,
    },
]

for item in sample_properties:
    prop, created = Property.objects.get_or_create(
        title=item['title'],
        defaults=item
    )
    if created:
        prop.amenities.set(amenity_objs[:6])
        PropertyImage.objects.create(
            property=prop,
            image='properties/images/sample_property.jpg',
            is_cover=True,
            order=0
        )
        print(f"Created property: {prop.title}")

# 3. Create Sample Enquiry
if Property.objects.exists():
    sample_prop = Property.objects.first()
    Enquiry.objects.get_or_create(
        email='john.doe@example.com',
        defaults={
            'property': sample_prop,
            'name': 'John Doe',
            'phone': '+91 98765 00000',
            'message': 'Hi, I would like to schedule a site visit for this property this weekend.',
            'status': 'New'
        }
    )

print("Data seeding completed successfully!")
