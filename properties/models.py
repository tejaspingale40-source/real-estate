from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.files.storage import default_storage


def select_video_storage():
    if getattr(settings, 'CLOUDINARY_URL', None):
        try:
            from cloudinary_storage.storage import VideoMediaCloudinaryStorage
            return VideoMediaCloudinaryStorage()
        except Exception:
            pass
    return default_storage


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome or SVG icon identifier, e.g., 'fa-parking'")

    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ['name']

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Plot', 'Plot'),
        ('Commercial', 'Commercial'),
    ]

    PURPOSE_CHOICES = [
        ('Sale', 'For Sale'),
        ('Rent', 'For Rent'),
    ]

    FURNISHED_CHOICES = [
        ('Furnished', 'Furnished'),
        ('Semi Furnished', 'Semi Furnished'),
        ('Unfurnished', 'Unfurnished'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
        ('Rented', 'Rented'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    location = models.CharField(max_length=100, help_text="City / Area name, e.g. Solapur, Pune")
    address = models.TextField()
    
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default='House')
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='Sale')
    
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in sq.ft")
    
    parking = models.BooleanField(default=True, help_text="Has parking facility")
    furnished = models.CharField(max_length=30, choices=FURNISHED_CHOICES, default='Semi Furnished')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    featured = models.BooleanField(default=False)
    
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='properties')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - ₹{self.price:,.0f}"

    @property
    def cover_image(self):
        cover = self.images.filter(is_cover=True).first()
        if not cover:
            cover = self.images.first()
        return cover


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/images/')
    is_cover = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Image for {self.property.title}"





class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='properties/videos/', storage=select_video_storage, blank=True, null=True)
    video_url = models.URLField(max_length=500, blank=True, null=True, help_text="Direct Cloudinary, YouTube, or MP4 video URL")
    title = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for {self.property.title}"

    def get_video_url(self):
        if self.video:
            return self.video.url
        return self.video_url or ""


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="PERFECT HOMES")
    tagline = models.CharField(max_length=200, default="REAL ESTATE ADVISORY • RERA CERTIFIED")
    phone = models.CharField(max_length=50, default="+91 7083150302")
    email = models.EmailField(default="dhairyashilmelage@gmail.com")
    address = models.CharField(max_length=255, default="101 Prime Plaza, VIP Road, Pune & Solapur, Maharashtra")
    
    # About Page Content Settings
    about_subtitle = models.CharField(max_length=255, default="Leading real estate consultancy delivering trust, transparency, and top-tier properties since 2010.", help_text="Subtitle on top of About page")
    about_vision_heading = models.CharField(max_length=200, default="Redefining Property Advisory", help_text="Heading for story section")
    about_vision_text = models.TextField(default="Founded by Dnyaneshwar Melage, Perfect Homes is a premier real estate consultancy dedicated to helping buyers, sellers, and investors navigate property decisions with trust, transparency, and expert market intelligence.", help_text="Main description text on About page")
    about_quote = models.CharField(max_length=255, default="Your property, our responsibility.", help_text="Highlighted tagline quote on About page")
    about_founder_name = models.CharField(max_length=100, default="Dnyaneshwar Melage", help_text="Founder Name")

    # Contact Page Content Settings
    contact_subtitle = models.CharField(max_length=255, default="Have questions or want to discuss property investments? Send us a message or visit our office.", help_text="Subtitle on top of Contact page")
    contact_address = models.TextField(default="101 Prime Plaza, VIP Road, Solapur - 413001, Maharashtra", help_text="Full address for contact page")
    contact_hours = models.CharField(max_length=100, default="Monday - Saturday: 9:00 AM - 7:00 PM", help_text="Working hours")
    google_maps_url = models.URLField(max_length=500, default="https://maps.google.com/maps?q=101+Prime+Plaza+VIP+Road+Solapur+Maharashtra&t=&z=15&ie=UTF8&iwloc=&output=embed", help_text="Google Maps Embed URL")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"Site Settings: {self.site_name}"

