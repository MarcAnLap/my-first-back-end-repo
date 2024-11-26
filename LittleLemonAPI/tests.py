from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import MenuItem, Category, Booking  # Import Category model
from decimal import Decimal
from datetime import date
from django.urls import reverse
from django.http import JsonResponse

import json

class MenuItemModelTest(TestCase):

    def setUp(self):
        """Create a category instance for the test."""
        self.category = Category.objects.create(title="Test Category", slug="test-category")  # Create a Category instance

    def test_menu_item_creation(self):
        """Test creating a MenuItem instance."""
        menu_item = MenuItem.objects.create(
            title="Test Item",
            price=Decimal('19.99'),
            featured=True,
            category=self.category,
            inventory=50
        )
        self.assertEqual(menu_item.title, "Test Item")
        self.assertEqual(menu_item.price, Decimal('19.99'))
        self.assertTrue(menu_item.featured)
        self.assertEqual(menu_item.category, self.category)
        self.assertEqual(menu_item.inventory, 50)

    def test_menu_item_str(self):
        """Test the string representation of the MenuItem."""
        menu_item = MenuItem.objects.create(
            title="Test Item",
            price=Decimal('19.99'),
            featured=True,
            category=self.category,
            inventory=50
        )
        self.assertEqual(str(menu_item), "Test Item")

    def test_menu_item_inventory_validation(self):
        """Test that inventory cannot be negative."""
        with self.assertRaises(ValidationError):
            menu_item = MenuItem.objects.create(
                title="Invalid Item",
                price=Decimal('19.99'),
                featured=False,
                category=self.category,
                inventory=-5
            )
            menu_item.full_clean()  # To trigger validation



class BookingModelTest(TestCase):

    def setUp(self):
        """Create a booking instance for the test."""
        self.booking = Booking.objects.create(
            first_name="John",
            last_name="Doe",
            reservation_date=date(2024, 12, 15),
            reservation_slot="Dinner",
            guest_number=4,
            comment="Looking forward to the meal!"
        )

    def test_booking_creation(self):
        """Test creating a Booking instance."""
        self.assertEqual(self.booking.first_name, "John")
        self.assertEqual(self.booking.last_name, "Doe")
        self.assertEqual(self.booking.reservation_date, date(2024, 12, 15))
        self.assertEqual(self.booking.reservation_slot, "Dinner")
        self.assertEqual(self.booking.guest_number, 4)
        self.assertEqual(self.booking.comment, "Looking forward to the meal!")

    def test_booking_str(self):
        """Test the string representation of the Booking."""
        self.assertEqual(str(self.booking), "John Doe")
        
    def test_booking_no_guest_number(self):
        """Test booking creation without guest number (optional field)."""
        booking_without_guest_number = Booking.objects.create(
            first_name="Jane",
            last_name="Doe",
            reservation_date=date(2024, 12, 16),
            reservation_slot="Lunch",
            guest_number=None,  # guest_number is optional
            comment="Excited!"
        )
        self.assertEqual(booking_without_guest_number.guest_number, None)


class HomeViewTest(TestCase):

    def test_home_view(self):
        """Test the home view."""
        response = self.client.get(reverse('home'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class AboutViewTest(TestCase):

    def test_about_view(self):
        """Test the about view."""
        response = self.client.get(reverse('about'))  
        self.assertTemplateUsed(response, 'about.html')


class BookViewTest(TestCase):

    def test_book_view_get(self):
        """Test the GET request to render the booking form."""
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book.html')

    def test_book_view_post_valid(self):
        """Test POST request with valid form data."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'reservation_date': '2024-12-15',
            'reservation_slot': 'Dinner',
            'guest_number': 4,
            'comment': 'Looking forward to the meal!'
        }
        response = self.client.post(reverse('book'), data)
        self.assertEqual(response.status_code, 200)  # Redirect on success
        self.assertTrue(Booking.objects.filter(first_name='John').exists())

    def test_booking_page_view(self):
        """Test the booking page view."""
        response = self.client.get(reverse('bookingpage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings.html')

class BookingsViewTest(TestCase):

    def test_bookings_view_get(self):
        """Test GET request for bookings on a specific date."""

        Booking.objects.create(
            first_name="John",
            last_name="Doe",
            reservation_date=date(2024, 12, 15),
            reservation_slot="Dinner",
            guest_number=4,
            comment="Looking forward to the meal!"
        )

        response = self.client.get(reverse('bookings') + '?date=2024-12-15')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')

    def test_bookings_view_post(self):
        """Test POST request for creating or updating a booking."""
        data = {
            'first_name': 'Jane',
            'reservation_date': '2024-12-15',
            'reservation_slot': 'Lunch',
            'guest_number': 3
        }
        response = self.client.post(reverse('bookings'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'success': 1})



    # def test_book_view_post_invalid(self):
    #     """Test POST request with invalid form data (e.g., missing fields)."""
    #     # Define data with missing 'last_name'
    #     data = {
    #         'first_name': 'John',
    #         'reservation_date': '2024-12-15',
    #         'reservation_slot': 'Dinner',
    #         'guest_number': 4
    #     }
        
    #     # Make a POST request with JSON data
    #     response = self.client.post(
    #         reverse('book'), 
    #         data=json.dumps(data), 
    #         content_type='application/json'
    #     )

    #     # Ensure the response status code is 200 (handled properly)
    #     self.assertEqual(response.status_code, 400)

    #     # Check that the response contains an error
    #     response_data = response.json()
    #     self.assertIn('error', response_data)
    #     self.assertEqual(response_data['error'], 1)

    #     # Ensure no booking was created
    #     self.assertFalse(Booking.objects.filter(first_name='John').exists())



# class MenuViewTest(TestCase):

    # def test_menu_view(self):
    #     """Test the menu view."""

    #     MenuItem.objects.create(
    #         title="Test Item 1",
    #         price=Decimal('19.99'),
    #         featured=True,
    #         category_id=1,
    #         inventory=10
    #     )
    #     MenuItem.objects.create(
    #         title="Test Item 2",
    #         price=Decimal('29.99'),
    #         featured=False,
    #         category_id=1,
    #         inventory=5
    #     )

    #     response = self.client.get(reverse('menu_item'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'menu.html')
    #     self.assertContains(response, 'Test Item 1')
    #     self.assertContains(response, 'Test Item 2')



# class DisplayMenuItemViewTest(TestCase):

#     def setUp(self):
#         """Create a menu item instance for testing."""
#         self.menu_item = MenuItem.objects.create(
#             title="Test Menu Item",
#             price=Decimal('9.99'),
#             featured=True,
#             category_id=1,
#             inventory=10
#         )

#     def test_display_menu_item_view_valid(self):
#         """Test the view for an existing menu item."""
#         response = self.client.get(reverse('display_menu_item', kwargs={'pk': self.menu_item.pk}))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'menu_item.html')
#         self.assertContains(response, 'Test Menu Item')

#     def test_display_menu_item_view_invalid(self):
#         """Test the view for a non-existing menu item."""
#         response = self.client.get(reverse('display_menu_item', kwargs={'pk': 999}))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'menu_item.html')
#         self.assertContains(response, "")


