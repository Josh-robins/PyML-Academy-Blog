from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .models import Post
from .views import BlogView, PostDetailView


class PostModelTest(TestCase):
    """Tests for the Post model itself."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            password='secret123',
        )
        cls.post = Post.objects.create(
            title='A Test Post',
            author=cls.user,
            body='This is the body of the test post.',
        )

    def test_post_str(self):
        """__str__ returns the post title."""
        self.assertEqual(str(self.post), 'A Test Post')

    def test_post_has_created_at(self):
        """Post is automatically given a created_at timestamp."""
        self.assertIsNotNone(self.post.created_at)

    def test_get_absolute_url(self):
        """get_absolute_url returns the correct detail URL."""
        self.assertEqual(self.post.get_absolute_url(), f'/post/{self.post.pk}/')


class HomePageURLTest(TestCase):
    """Tests that the home page URL exists and resolves correctly."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser2',
            password='secret123',
        )
        Post.objects.create(
            title='Home Page Post',
            author=cls.user,
            body='Body content here.',
        )

    def test_home_url_exists(self):
        """GET / returns HTTP 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_url_by_name(self):
        """Reverse of 'home' URL name returns HTTP 200."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_to_correct_view(self):
        """/ resolves to BlogView."""
        view = resolve('/')
        self.assertEqual(view.func.view_class, BlogView)

    def test_home_uses_correct_template(self):
        """Home page uses home.html template."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_displays_post_title(self):
        """Home page renders the post title in content."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Home Page Post')

    def test_home_displays_author(self):
        """Home page renders 'Authored by:' with the author username."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Authored by:')
        self.assertContains(response, 'testuser2')

    def test_home_displays_truncated_body(self):
        """Home page shows a 'Read more' link (body is truncated)."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Read more')


class PostDetailURLTest(TestCase):
    """Tests that the post detail URL exists and resolves correctly."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser3',
            password='secret123',
        )
        cls.post = Post.objects.create(
            title='Detail Page Post',
            author=cls.user,
            body='Full body content visible on detail page.',
        )

    def test_detail_url_exists(self):
        """GET /post/<pk>/ returns HTTP 200."""
        response = self.client.get(f'/post/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_detail_url_by_name(self):
        """Reverse of 'post-detail' URL name returns HTTP 200."""
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_detail_url_resolves_to_correct_view(self):
        """/post/<pk>/ resolves to PostDetailView."""
        view = resolve(f'/post/{self.post.pk}/')
        self.assertEqual(view.func.view_class, PostDetailView)

    def test_detail_uses_correct_template(self):
        """Detail page uses post_detail.html template."""
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_detail_displays_full_title(self):
        """Detail page renders the post title."""
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertContains(response, 'Detail Page Post')

    def test_detail_displays_full_body(self):
        """Detail page renders the complete post body."""
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertContains(response, 'Full body content visible on detail page.')

    def test_detail_displays_author(self):
        """Detail page renders the author username."""
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertContains(response, 'testuser3')

    def test_detail_404_for_nonexistent_post(self):
        """Requesting a non-existent post pk returns HTTP 404."""
        response = self.client.get(reverse('post-detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)
