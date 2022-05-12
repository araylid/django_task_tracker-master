# import json
# from django.test import TestCase
# from django.urls import reverse
# from catalog.models import User, Project, Task, Description
# from catalog.serializers import UserSerializer, ProjectSerializer, \
#     TaskSerializer, DescriptionSerializer
#
#
# class TasksListViewTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_get_tasks_list(self):
#         resp = self.client.get(reverse('root'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertContains(resp, 'Filter by or search:')
#         self.assertContains(resp, 'Tasks list:')
#         tasks_number = Task.objects.count()
#         self.assertEqual(tasks_number, 10)
#         for i in range(tasks_number):
#             self.assertContains(resp, 'purpose{}'.format(i+1))
#             self.assertContains(resp, 'firstname{} lastname{}'.
#                                 format(i+1, i+1))
#
#
# class TaskDetailViewTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_get_detail_task(self):
#         tasks_number = Task.objects.count()
#         for i in range(tasks_number):
#             id = i+1
#             resp = self.client.get(reverse('task-detail', args=[str(id)]))
#             self.assertEqual(resp.status_code, 200)
#             self.assertContains(resp, 'purpose{}'.format(id))
#             self.assertContains(resp, 'firstname')
#             self.assertContains(resp, 'lastname')
#             self.assertContains(resp, 'Create new description')
#             self.assertContains(resp, 'Update this task')
#             self.assertContains(resp, 'Delete this task')
#
#     def test_delete_detail_task(self):
#         id = 1
#         resp = self.client.delete(reverse('task-detail', args=[str(id)]))
#         self.assertEqual(resp.status_code, 405)
#
#
# class CreateTaskViewTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_get_creating_form(self):
#         resp = self.client.get(reverse('create_task'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertContains(resp, 'Please fill out the form to create a task:')
#         self.assertContains(resp, 'Task purpose:')
#         self.assertContains(resp, 'Submit')
#
#     def test_post_create_task(self):
#         data = {
#             "purpose": "some_test_purpose",
#             "project": 1,
#             "status": "New",
#             "author": 2,
#             "worker": 3,
#         }
#         resp = self.client.post(reverse('create_task'), data=data)
#         self.assertEqual(resp.status_code, 302)
#         new_task_object = Task.objects.filter(purpose='some_test_purpose')
#         self.assertEqual(len(new_task_object), 1)
#         self.assertEqual(Task.objects.count(), 11)
#
#     def test_try_put(self):
#         resp = self.client.put(reverse('create_task'))
#         self.assertEqual(resp.status_code, 405)
#
#
# class CreateDescriptionViewTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_get_create_descr_form(self):
#         task_id = 1
#         resp = self.client.get(reverse('create_description', args=[task_id]))
#         self.assertEqual(resp.status_code, 200)
#         self.assertContains(resp, 'Please fill out the form')
#         self.assertContains(resp, 'Submit')
#
#     def test_post_create_descr(self):
#         task_id = 1
#         author_id = 1
#         resp = self.client.post(reverse('create_description', args=[task_id]),
#                                 {
#                                     'description': 'some_test_description',
#                                     'author': author_id
#                                 })
#         self.assertEqual(resp.status_code, 302)
#         new_descr_object = Description.objects.filter(
#             description='some_test_description')
#         self.assertEqual(len(new_descr_object), 1)
#         self.assertEqual(Description.objects.count(), 101)
#
#     def test_try_delete(self):
#         task_id = 1
#         resp = self.client.delete(reverse('create_description', args=[task_id]))
#         self.assertEqual(resp.status_code, 405)
#
#
# class DeleteTaskViewTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_delete_task(self):
#         task_id = 1
#         resp = self.client.delete(reverse('delete_task', args=[task_id]))
#         self.assertEqual(resp.status_code, 302)
#         deleted_obj = Task.objects.filter(id=task_id)
#         self.assertEqual(len(deleted_obj), 0)
#
#     def test_try_get(self):
#         task_id = 1
#         resp = self.client.get(reverse('delete_task', args=[task_id]))
#         self.assertEqual(resp.status_code, 405)
#
#
# class UpdateTaskViewTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_get_update_form(self):
#         task_id = 1
#         resp = self.client.get(reverse('update_task', args=[task_id]))
#         self.assertEqual(resp.status_code, 200)
#         self.assertContains(resp, 'Please select new status or executor:')
#
#     def test_post_update_task(self):
#         task_id = 1
#         new_worker_id = 1
#         resp = self.client.post(reverse('update_task', args=[task_id]),
#                                 {'status': 'Ready', 'worker': new_worker_id})
#         self.assertEqual(resp.status_code, 302)
#         task = Task.objects.get(id=task_id)
#         self.assertEqual(task.status, 'Ready')
#         self.assertEqual(task.worker.id, new_worker_id)
#
#     def test_try_put(self):
#         task_id = 1
#         resp = self.client.put(reverse('update_task', args=[task_id]))
#         self.assertEqual(resp.status_code, 405)
#
#
# class API_UserListTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_api_get_user_list(self):
#         resp = self.client.get(reverse('users-list'))
#         serializer = UserSerializer(User.objects.all(), many=True)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(serializer.data, resp.data)
#
#     def test_api_post_create_user(self):
#         data = {"first_name": "TestFirstName", "last_name": "TestLastName"}
#         resp = self.client.post(reverse('users-list'), data=data)
#         self.assertEqual(resp.status_code, 201)
#         new_user = User.objects.get(first_name="TestFirstName")
#         self.assertEqual(new_user.last_name, 'TestLastName')
#
#
# class API_UserDetailTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_api_get_user_detail(self):
#         user_id = 1
#         resp = self.client.get(reverse('user-detail', args=[user_id]))
#         user = User.objects.get(id=user_id)
#         serializer = UserSerializer(user)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(serializer.data, resp.data)
#
#
# class API_ProjectDetailTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_api_get_project_detail(self):
#         project_id = 1
#         resp = self.client.get(reverse('project-detail', args=[project_id]))
#         project = Project.objects.get(id=project_id)
#         serializer = ProjectSerializer(project)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(serializer.data, resp.data)
#
#
# class API_TaskListTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_api_get_tasks_list(self):
#         resp = self.client.get(reverse('tasks-list'))
#         serializer = TaskSerializer(Task.objects.all(), many=True)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(serializer.data, resp.data)
#
#     def test_api_post_create_task(self):
#         data = {
#             "purpose": "TestPurpose",
#             "project": 1,
#             "status": "Canceled",
#             "author": 2,
#             "worker": 3,
#         }
#         resp = self.client.post(reverse('tasks-list'), data=data)
#         self.assertEqual(resp.status_code, 201)
#         new_task = Task.objects.get(purpose="TestPurpose")
#         self.assertEqual(new_task.status, "Canceled")
#
#
# class API_TaskDetailTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_api_get_detail_task(self):
#         task_id = 1
#         resp = self.client.get(reverse('api-task-detail', args=[task_id]))
#         task = Task.objects.get(id=task_id)
#         serializer = TaskSerializer(task)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(serializer.data, resp.data)
#
#     def test_api_put_update_task(self):
#         task_id = 1
#         data = {
#             "status": "Canceled",
#             "worker": 5
#         }
#         resp = self.client.put(reverse('api-task-detail', args=[task_id]),
#                                data, content_type="application/json")
#         task = Task.objects.get(id=task_id)
#         serializer = TaskSerializer(task)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(serializer.data, resp.data)
#
#     def test_api_delete_task(self):
#         task_id = 1
#         resp = self.client.delete(reverse('api-task-detail', args=[task_id]))
#         task = Task.objects.filter(id=task_id).all()
#         self.assertEqual(resp.status_code, 204)
#         self.assertEqual(len(task), 0)
#
#
# class API_DescriptionListTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_api_get_descr_list(self):
#         task_id = 1
#         resp = self.client.get(reverse('description-detail', args=[task_id]))
#         serializer = DescriptionSerializer(Description.objects.filter(
#                                             task_id=task_id).all(), many=True)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(serializer.data, resp.data)
#
#     def test_api_post_create_descr(self):
#         task_id = 1
#         data = {
#             "description": "TestDescription",
#             "task": task_id,
#             "author": 4
#         }
#         resp = self.client.post(reverse('description-detail', args=[task_id]),
#                                 data=data)
#         self.assertEqual(resp.status_code, 201)
#         new_desc = Description.objects.get(description="TestDescription")
#         self.assertEqual(new_desc.author.id, 4)
#
#
# class API_DescriptionStatisticsTest(TestCase):
#     fixtures = ['dumpdata.json']
#
#     def test_api_get_statistics(self):
#         task_id = 1
#         resp = self.client.get(reverse('descriptions_statistic', args=[task_id]))
#         data = {
#             "2019-05-10": {
#                 "diff_descriptions": 3,
#                 "diff_authors": 2
#             },
#             "2019-05-09": {
#                 "diff_descriptions": 3,
#                 "diff_authors": 3
#             },
#             "2019-05-07": {
#                 "diff_descriptions": 2,
#                 "diff_authors": 2
#             },
#             "2019-05-06": {
#                 "diff_descriptions": 2,
#                 "diff_authors": 2
#             }
#         }
#         self.assertEqual(json.dumps(resp.data), json.dumps(data))
