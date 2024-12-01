import unittest

from src.models.Task import Task
from src.models.TaskManager import TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Создание экземпляра TaskManager с задачей для всех тестов"""
        self.task_manager = TaskManager('data/test_tasks.json')
        self.sample_task = {
            'id': 1,
            'title': 'тест',
            'description': 'тест',
            'category': 'тест',
            'due_date': '01-12-2024',
            'priority': 'Средний',
            'status': 'Не выполнена'
        }
        self.task = Task(**self.sample_task)
        self.task_manager.add_task(self.sample_task)

    def test_add_task_success(self):
        """Тест добавления задачи (успешно) """
        new_task_data = {
            'id': 2,
            'title': 'New Task',
            'description': 'New task description',
            'category': 'Work',
            'due_date': '02-12-2024',
            'priority': 'Высокий',
            'status': 'Не выполнена'
        }
        result = self.task_manager.add_task(new_task_data)
        self.assertTrue(result)
        task = self.task_manager.find_task_by_id(2)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, 'New Task')

    def test_add_task_failure(self):
        """Тест добавления задачи (не успешно, невалидные данные)"""
        invalid_task_data = {
            'id': 3,
            'title': '',
            'description': '',
            'category': '',
            'due_date': '22222',
            'priority': 'Чушь',
            'status': 'вып'
        }
        result = self.task_manager.add_task(invalid_task_data)
        self.assertFalse(result)

    def test_find_task_by_id(self):
        """Тест нахождения задачи по ее ID (ID существует)"""
        task = self.task_manager.find_task_by_id(1)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, 'тест')

    def test_find_task_by_non_existent_id(self):
        """Тест нахождения задачи по ее ID (ID не существует)"""
        task = self.task_manager.find_task_by_id(999)
        self.assertIsNone(task)

    def test_edit_task_by_id(self):
        """Тест обновления существующей задачи"""
        updated_task_data = {
            'id': 1,
            'title': 'Обновленная задача',
            'description': 'Обновленное описание',
            'category': 'новая категория',
            'due_date': '03-12-2024',
            'priority': 'Низкий',
            'status': 'Выполнена'
        }
        self.task_manager.edit_task_by_id(1, updated_task_data)
        task = self.task_manager.find_task_by_id(1)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, 'Обновленная задача')
        self.assertEqual(task.status, 'Выполнена')

    def test_delete_task_by_id(self):
        """Тест удаления задачи по ID (ID существует)"""
        self.task_manager.delete_task_by_id(1)
        task = self.task_manager.find_task_by_id(1)
        self.assertIsNone(task)

    def test_delete_task_by_non_existent_id(self):
        """Тест удаления задачи по ID (ID не существует)"""
        result = self.task_manager.delete_task_by_id(999)
        self.assertFalse(result)

    def test_get_tasks(self):
        """Тест получения всех задач"""
        tasks = list(self.task_manager.get_tasks())
        self.assertGreater(len(tasks), 0)

    def test_get_tasks_by_category(self):
        """Тест получения задач по категории (категория существует)"""
        tasks = self.task_manager.get_tasks_by_category('тест')
        self.assertIsNotNone(tasks)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], 'тест')

    def test_get_tasks_by_non_existent_category(self):
        """Тест получения задач по категории (категории не существует)"""
        tasks = self.task_manager.get_tasks_by_category('несуществует')
        self.assertIsNone(tasks)

    def test_get_tasks_by_status(self):
        """Тест получения задач по статусу"""
        tasks = self.task_manager.get_tasks_by_status('не выполнена')
        self.assertGreater(len(tasks), 0)

    def test_get_tasks_by_keywords(self):
        """Тест получения задач по ключевому слову"""
        keywords = {'тест', 'задача'}
        matching_in_title, matching_in_description = self.task_manager.get_tasks_by_keywords(keywords)
        self.assertIn(1, matching_in_title)
        self.assertIn(1, matching_in_description)


if __name__ == '__main__':
    unittest.main()
