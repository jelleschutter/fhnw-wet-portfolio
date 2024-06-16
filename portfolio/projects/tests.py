from django.test import TestCase

from .models import Project, Tag

class TestProjectViews(TestCase):
    def setUp(self) -> None:
        self.tags = [
            Tag.objects.create(name='Example Tag'),
            Tag.objects.create(name='Another Tag'),
            Tag.objects.create(name='Third Tag')
        ]

        self.projects = [
            Project.objects.create(
                title='Example Project',
                content='Example content',
                image='candi-solar.jpg',
            ),
            Project.objects.create(
                title='Another Project',
                content='Another content',
                image='candi-solar.jpg',
            )
        ]

        self.projects[0].tags.add(self.tags[0], self.tags[1])
        self.projects[1].tags.add(self.tags[1], self.tags[2])
    
    def test_index_view(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/index.html')
        self.assertContains(response, 'Projects | Jelle Schutter')
        self.assertContains(response, self.projects[0].title)
        self.assertContains(response, self.projects[1].title)

    def test_project_view(self):
        response = self.client.get(f'/projects/project/{self.projects[0].id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_detail.html')
        self.assertContains(response, self.projects[0].title)
        self.assertNotContains(response, self.projects[1].title)

    def test_tag_view(self):
        response = self.client.get(f'/projects/tag/{self.tags[0].id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/tag_detail.html')
        self.assertContains(response, self.tags[0].name)
        self.assertNotContains(response, self.tags[1].name)
        self.assertContains(response, self.projects[0].title)
        self.assertNotContains(response, self.projects[1].title)

    def test_search_view(self):
        response = self.client.get('/projects/search/?query=Example')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/search.html')
        self.assertContains(response, 'Search | Jelle Schutter')
        self.assertContains(response, self.projects[0].title) # from project title
        self.assertNotContains(response, self.projects[1].title)

        response = self.client.get('/projects/search/?query=Another')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/search.html')
        self.assertContains(response, 'Search | Jelle Schutter')
        self.assertContains(response, self.projects[0].title) # from tag 1
        self.assertContains(response, self.projects[1].title) # from tag 1 and project title

        response = self.client.get('/projects/search/?query=Tag')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/search.html')
        self.assertContains(response, 'Search | Jelle Schutter')
        self.assertContains(response, self.projects[0].title) # from tag 0 and tag 1
        self.assertContains(response, self.projects[1].title) # from tag 1 and tag 2
