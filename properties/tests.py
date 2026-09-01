from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from properties.models import Property, Amenity
from enquiries.models import Enquiry


class RealEstateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='admin_staff',
            email='admin@example.com',
            password='password123',
            is_staff=True
        )
        self.amenity = Amenity.objects.create(name="Garden", icon="fa-tree")
        self.property = Property.objects.create(
            title="Test Luxury Mansion",
            description="A test description of luxury mansion",
            price=15000000,
            location="Solapur",
            address="123 Test Street",
            property_type="Villa",
            purpose="Sale",
            bedrooms=4,
            bathrooms=4,
            area=3000,
            parking=True,
            furnished="Furnished",
            status="Available",
            featured=True
        )
        self.property.amenities.add(self.amenity)

    def test_property_creation_and_slug(self):
        self.assertEqual(self.property.slug, "test-luxury-mansion")
        self.assertEqual(str(self.property), "Test Luxury Mansion - ₹15,000,000")

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Luxury Mansion")

    def test_property_list_view_search_and_filter(self):
        response = self.client.get(reverse('property_list') + '?q=Mansion&location=Solapur')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Luxury Mansion")

    def test_property_detail_view(self):
        response = self.client.get(reverse('property_detail', kwargs={'slug': self.property.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Luxury Mansion")

    def test_enquiry_submission(self):
        response = self.client.post(
            reverse('property_detail', kwargs={'slug': self.property.slug}),
            {
                'name': 'Tester Person',
                'phone': '+91 9999988888',
                'email': 'tester@example.com',
                'message': 'Interested in buying',
                'property': self.property.id
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Enquiry.objects.count(), 1)
        enq = Enquiry.objects.first()
        self.assertEqual(enq.name, 'Tester Person')

    def test_dashboard_unauthenticated_redirect(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('dashboard_login'), response.url)

    def test_dashboard_login_page_renders(self):
        response = self.client.get(reverse('dashboard_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Staff & Administrative Dashboard Portal")

    def test_dashboard_login_authentication_success(self):
        response = self.client.post(reverse('dashboard_login'), {
            'username': 'admin_staff',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)

    def test_dashboard_authenticated_staff_access(self):
        self.client.login(username='admin_staff', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Real Estate Admin Dashboard")

