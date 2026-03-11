from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .models import Post
from .views import BlogView, PostDetailView, PostUpdateView, PostDeleteView


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


class PostUpdateViewTest(TestCase):
    """Tests for the post edit/update view."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='edituser',
            password='secret123',
        )
        cls.post = Post.objects.create(
            title='Original Title',
            author=cls.user,
            body='Original body content.',
        )

    def test_edit_url_exists(self):
        """GET /post/<pk>/edit/ returns HTTP 200."""
        response = self.client.get(f'/post/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_edit_url_by_name(self):
        """Reverse of 'post-edit' URL name returns HTTP 200."""
        response = self.client.get(reverse('post-edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_edit_url_resolves_to_correct_view(self):
        """/post/<pk>/edit/ resolves to PostUpdateView."""
        view = resolve(f'/post/{self.post.pk}/edit/')
        self.assertEqual(view.func.view_class, PostUpdateView)

    def test_edit_uses_correct_template(self):
        """Edit page uses post_edit.html template."""
        response = self.client.get(reverse('post-edit', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(response, 'post_edit.html')

    def test_edit_form_prepopulated(self):
        """Edit page pre-fills the form with the existing title and body."""
        response = self.client.get(reverse('post-edit', kwargs={'pk': self.post.pk}))
        self.assertContains(response, 'Original Title')
        self.assertContains(response, 'Original body content.')

    def test_post_update_changes_title_and_body(self):
        """POSTing valid data updates the post and redirects to the detail page."""
        response = self.client.post(
            reverse('post-edit', kwargs={'pk': self.post.pk}),
            data={'title': 'Updated Title', 'body': 'Updated body content.'},
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.body, 'Updated body content.')
        self.assertRedirects(response, reverse('post-detail', kwargs={'pk': self.post.pk}))

    def test_edit_404_for_nonexistent_post(self):
        """Requesting edit for a non-existent pk returns HTTP 404."""
        response = self.client.get(reverse('post-edit', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)


class PostDeleteViewTest(TestCase):
    """Tests for the post delete view."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='deleteuser',
            password='secret123',
        )

    def setUp(self):
        # Recreate the post before each test so deletion tests are independent.
        self.post = Post.objects.create(
            title='Post To Delete',
            author=self.user,
            body='This post will be deleted.',
        )

    def test_delete_url_exists(self):
        """GET /post/<pk>/delete/ returns HTTP 200 (confirmation page)."""
        response = self.client.get(f'/post/{self.post.pk}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_delete_url_by_name(self):
        """Reverse of 'post-delete' URL name returns HTTP 200."""
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_delete_url_resolves_to_correct_view(self):
        """/post/<pk>/delete/ resolves to PostDeleteView."""
        view = resolve(f'/post/{self.post.pk}/delete/')
        self.assertEqual(view.func.view_class, PostDeleteView)

    def test_delete_uses_correct_template(self):
        """Delete confirmation page uses post_delete.html template."""
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(response, 'post_delete.html')

    def test_delete_confirmation_page_shows_post_title(self):
        """Delete confirmation page displays the post title."""
        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertContains(response, 'Post To Delete')

    def test_post_delete_removes_post_and_redirects_home(self):
        """POSTing to the delete URL removes the post and redirects to home."""
        pk = self.post.pk
        response = self.client.post(reverse('post-delete', kwargs={'pk': pk}))
        self.assertFalse(Post.objects.filter(pk=pk).exists())
        self.assertRedirects(response, reverse('home'))

    def test_delete_404_for_nonexistent_post(self):
        """Requesting delete for a non-existent pk returns HTTP 404."""
        response = self.client.get(reverse('post-delete', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)


class Custom404PageTest(TestCase):
    """Tests that a 404 response is returned for unknown URLs."""

    def test_unknown_url_returns_404(self):
        """A request to a URL that doesn't exist returns HTTP 404."""
        response = self.client.get('/this-url-does-not-exist/')
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_post_detail_returns_404(self):
        """Detail page for a missing pk returns HTTP 404."""
        response = self.client.get(reverse('post-detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_post_edit_returns_404(self):
        """Edit page for a missing pk returns HTTP 404."""
        response = self.client.get(reverse('post-edit', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_post_delete_returns_404(self):
        """Delete page for a missing pk returns HTTP 404."""
        response = self.client.get(reverse('post-delete', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)


class LoginViewTest(TestCase):
    """Tests for the login page."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='loginuser',
            password='secret123',
        )

    def test_login_url_exists(self):
        """GET /accounts/login/ returns HTTP 200."""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_by_name(self):
        """Reverse of 'login' URL name returns HTTP 200."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_uses_correct_template(self):
        """Login page uses registration/login.html template."""
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_page_has_signup_link(self):
        """Login page contains a link to the sign-up page."""
        response = self.client.get(reverse('login'))
        self.assertContains(response, reverse('signup'))

    def test_valid_login_redirects_to_home(self):
        """POSTing valid credentials logs the user in and redirects to home."""
        response = self.client.post(reverse('login'), data={
            'username': 'loginuser',
            'password': 'secret123',
        })
        self.assertRedirects(response, reverse('home'))

    def test_invalid_login_stays_on_login_page(self):
        """POSTing wrong credentials returns 200 and stays on login page."""
        response = self.client.post(reverse('login'), data={
            'username': 'loginuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logged_in_user_sees_greeting(self):
        """After login, homepage contains the username greeting."""
        self.client.login(username='loginuser', password='secret123')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'loginuser')


class LogoutViewTest(TestCase):
    """Tests for logout behaviour."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='logoutuser',
            password='secret123',
        )

    def test_logout_post_redirects_to_home(self):
        """POSTing to logout logs the user out and redirects to home."""
        self.client.login(username='logoutuser', password='secret123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

    def test_logout_get_returns_405(self):
        """GET request to logout returns 405 Method Not Allowed."""
        self.client.login(username='logoutuser', password='secret123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)

    def test_user_is_logged_out_after_logout(self):
        """After POSTing to logout, the user is no longer authenticated."""
        self.client.login(username='logoutuser', password='secret123')
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class SignUpViewTest(TestCase):
    """Tests for the sign-up page."""

    def test_signup_url_exists(self):
        """GET /accounts/signup/ returns HTTP 200."""
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_url_by_name(self):
        """Reverse of 'signup' URL name returns HTTP 200."""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_uses_correct_template(self):
        """Sign-up page uses registration/signup.html template."""
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_page_has_login_link(self):
        """Sign-up page contains a link to the login page."""
        response = self.client.get(reverse('signup'))
        self.assertContains(response, reverse('login'))

    def test_valid_signup_creates_user_and_redirects(self):
        """POSTing valid signup data creates a new user and redirects to login."""
        response = self.client.post(reverse('signup'), data={
            'username': 'brandnewuser',
            'password1': 'C0mpl3xPass!',
            'password2': 'C0mpl3xPass!',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(get_user_model().objects.filter(username='brandnewuser').exists())

    def test_invalid_signup_stays_on_signup_page(self):
        """POSTing mismatched passwords returns 200 and stays on sign-up page."""
        response = self.client.post(reverse('signup'), data={
            'username': 'baduser',
            'password1': 'C0mpl3xPass!',
            'password2': 'DifferentPass!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
