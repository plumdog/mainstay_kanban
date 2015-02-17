from django.test import TestCase
from django.contrib.auth.models import User
from mainstay.test_utils import MainstayTest

from .models import Task


class KanbanTestCase(MainstayTest):
    fixtures = MainstayTest.fixtures + ['kanban_tasks']
    def test_user_loaded(self):
        user = User.objects.get()
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.is_superuser, True)

    def test_pages_loaded(self):
        self.assertEqual(Task.objects.count(), 3)
        task_names = {t.name for t in Task.objects.all()}
        self.assertEqual(task_names, {'TaskNew', 'TaskStarted', 'TaskCompleted'})

    def test_main_page(self):
        self.login()
        r = self.client.get('/kanban')
        self.assertEqual(len(r.context['todo']), 1)
        self.assertEqual(len(r.context['in_progress']), 1)
        self.assertEqual(len(r.context['completed']), 1)

    def test_add_task(self):
        self.login()
        post = {'name': 'MyTask',
                'content': 'MyContent'}
        r = self.client.post('/kanban/add/', post, follow=True)
        self.assertRedirects(r, '/kanban')
        self.assertEqual(len(r.context['todo']), 2)
        self.assertEqual(len(r.context['in_progress']), 1)
        self.assertEqual(len(r.context['completed']), 1)
