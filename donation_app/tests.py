from django.test import TestCase
from django.urls import reverse
from .models import Donation, Institution, Category
from .forms import DonationForm


class LandingPageViewTestCase(TestCase):
    """Test case for the landing page view."""

    def setUp(self):
        """Set up test data."""
        self.url = reverse('landing_page')

    def test_view_returns_200(self):
        """Test if the view returns a status code of 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test if the correct template is used."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')

    def test_view_contains_expected_data(self):
        """Test if the view contains expected data."""
        institution = Institution.objects.create(name="Test Institution", description="Test Description",
                                                 type=Institution.FOUNDATION)
        category = Category.objects.create(name="Test Category")
        donation = Donation.objects.create(quantity=10, institution=institution, address="Test Address",
                                           phone_number="123456789", city="Test City", zip_code="12345",
                                           pick_up_date="2024-04-10", pick_up_time="10:00:00",
                                           pick_up_comment="Test Comment")

        response = self.client.get(self.url)
        self.assertEqual(response.context['donation_count'], 10)
        self.assertEqual(response.context['supported_organizations_count'], 1)

    def test_landing_page_view_context_data(self):
        """Test if the landing page view contains the expected context data."""
        response = self.client.get(reverse('landing_page'))
        self.assertIn('donation_count', response.context)
        self.assertIn('supported_organizations_count', response.context)
        self.assertIn('foundations', response.context)
        self.assertIn('ngos', response.context)
        self.assertIn('local_collections', response.context)


class AddDonationViewTest(TestCase):
    """Test case for adding a donation view."""

    def test_add_donation_view_status_code(self):
        """Test if the add donation view returns a status code of 200."""
        response = self.client.get(reverse('add_donation'))
        self.assertEqual(response.status_code, 200)

    def test_add_donation_view_template(self):
        """Test if the correct template is used for the add donation view."""
        response = self.client.get(reverse('add_donation'))
        self.assertTemplateUsed(response, 'form.html')

    def test_add_donation_view_form(self):
        """Test if the add donation view contains the donation form."""
        response = self.client.get(reverse('add_donation'))
        self.assertIsInstance(response.context['form'], DonationForm)


class FormConfirmationViewTest(TestCase):
    """Test case for the form confirmation view."""

    def test_form_confirmation_view_status_code(self):
        """Test if the form confirmation view returns a status code of 200."""
        response = self.client.get(reverse('form_confirmation'))
        self.assertEqual(response.status_code, 200)

    def test_form_confirmation_view_template(self):
        """Test if the correct template is used for the form confirmation view."""
        response = self.client.get(reverse('form_confirmation'))
        self.assertTemplateUsed(response, 'form-confirmation.html')


class LoginViewTest(TestCase):
    """Test case for the login view."""

    def test_login_view_status_code(self):
        """Test if the login view returns a status code of 200."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_template(self):
        """Test if the correct template is used for the login view."""
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'login.html')


class LogoutViewTest(TestCase):
    """Test case for the logout view."""

    def test_logout_view_redirects_to_landing_page(self):
        """Test if the logout view redirects to the landing page."""
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('landing_page'))
