from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class StudyCourseFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="student@example.com",
            password="test-password",
        )
        self.client.force_login(self.user)

    def test_study_page_starts_with_course_selection(self):
        response = self.client.get(reverse("study"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose your course")
        self.assertNotContains(response, "Your subjects")

    def test_available_course_shows_subjects(self):
        response = self.client.get(
            reverse("study"),
            {"year": "1", "semester": "1", "branch": "aiml"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["QUERY_STRING"], "")
        self.assertContains(response, "Your subjects")
        self.assertContains(response, "Linear Algebra")
        self.assertContains(response, "Machine Learning")

    def test_course_form_posts_and_redirects_without_query_parameters(self):
        response = self.client.post(
            reverse("study"),
            {"year": "1", "semester": "1", "branch": "aiml"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["QUERY_STRING"], "")
        self.assertContains(response, "Your subjects")
        self.assertContains(response, 'method="post"')

    def test_linear_algebra_has_five_units_and_unit_one_notes(self):
        response = self.client.get(reverse("linear_algebra"))

        self.assertEqual(response.status_code, 200)
        for unit_number in range(1, 6):
            self.assertContains(response, 'id="unit-{}"'.format(unit_number))
        self.assertContains(response, "Matrices, rank, and echelon forms")
        self.assertContains(response, "rank(A) = 2")

    def test_study_and_subject_pages_use_separate_styles(self):
        study_response = self.client.get(reverse("study"))
        self.assertContains(study_response, "<style>")
        self.assertContains(study_response, ".study-card")
        self.assertNotContains(study_response, "study.css")

        for subject in (
            "linear_algebra",
            "machine_learning",
            "digital_logic",
            "web_technology",
            "programming",
        ):
            with self.subTest(subject=subject):
                response = self.client.get(reverse(subject))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "<style>")
                self.assertNotContains(response, 'href="/static/css/study.css"')
                self.assertContains(response, "EduNexus")