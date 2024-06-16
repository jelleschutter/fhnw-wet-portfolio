from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from .models import WorkExperience, Skill

class TestIndexView(TestCase):
    def setUp(self) -> None:
        self.work_experience = WorkExperience.objects.create(
            title='Software Developer',
            company='FHNW',
            start_date='2021-01-01',
            end_date='2021-12-31',
            description='Example description'
        )

        self.skill = Skill.objects.create(
            name='Python',
            proficiency=100
        )

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'About Me | Jelle Schutter')
        self.assertQuerysetEqual(response.context['work_experiences'], [
            self.work_experience
        ])
        self.assertQuerysetEqual(response.context['skills'], [
            self.skill
        ])

class TestContactView(TestCase):
    def test_contact_view(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertContains(response, 'Contact | Jelle Schutter')
        self.assertContains(response, 'jelle@schutter.xyz')

class TestSkillModel(TestCase):
    def test_skill_str(self):
        skill = Skill.objects.create(
            name='Python',
            proficiency=100
        )
        self.assertEqual(str(skill), 'Python')

    def test_skill_proficiency_constraint_min(self):
        with self.assertRaises(ValidationError):
            Skill(
                name='Python',
                proficiency=-1
            ).full_clean()
    
    def test_skill_proficiency_constraint_max(self):
        with self.assertRaises(ValidationError):
            Skill(
                name='Python',
                proficiency=101
            ).full_clean()
    
    def test_skill_proficiency_constraint_valid(self):
        Skill(
            name='Python',
            proficiency=100
        ).full_clean()