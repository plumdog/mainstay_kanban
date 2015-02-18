from django.test import TestCase
from django.contrib.auth.models import User
from mainstay.test_utils import MainstayTest

from .models import Task


class KanbanTestCase(MainstayTest):
    fixtures = MainstayTest.fixtures + ['kanban_tasks']
    def test_user_loaded(self):
        self.assertEqual(self.admin.username, 'admin')
        self.assertEqual(self.admin.is_superuser, True)

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

    def test_add_task_no_user(self):
        self.login()
        post = {'name': 'MyTask',
                'content': 'MyContent'}
        r = self.client.post('/kanban/add/', post, follow=True)
        self.assertRedirects(r, '/kanban')
        self.assertEqual(len(r.context['todo']), 2)
        self.assertEqual(len(r.context['in_progress']), 1)
        self.assertEqual(len(r.context['completed']), 1)

    def test_add_task_with_user_current_user(self):
        self.login()
        post = {'name': 'MyTask',
                'content': 'MyContent',
                'user': self.admin.id}
        r = self.client.post('/kanban/add/', post, follow=True)
        self.assertRedirects(r, '/kanban')
        self.assertEqual(len(r.context['todo']), 2)
        self.assertEqual(len(r.context['in_progress']), 1)
        self.assertEqual(len(r.context['completed']), 1)

    def test_add_task_with_user_other_user(self):
        self.login()
        post = {'name': 'MyTask',
                'content': 'MyContent',
                'user': self.user.id}
        r = self.client.post('/kanban/add/', post, follow=True)
        self.assertRedirects(r, '/kanban')

        # noting extra for the current user
        self.assertEqual(len(r.context['todo']), 1)
        self.assertEqual(len(r.context['in_progress']), 1)
        self.assertEqual(len(r.context['completed']), 1)

        # extra task for the delegated user
        self.login(username='user')
        r = self.client.get('/kanban')
        self.assertEqual(len(r.context['todo']), 2)
        self.assertEqual(len(r.context['in_progress']), 1)
        self.assertEqual(len(r.context['completed']), 1)

        todo_tasks = r.context['todo']
        delegated_task = [t for t in todo_tasks if t.delegated_by is not None][0]
        self.assertEqual(delegated_task.user, self.user)
        self.assertEqual(delegated_task.delegated_by, self.admin)
