from datetime import datetime
from typing import Dict


class TaskValidation:

    VALID_PRIORITY = {'Низкий', 'Средний', 'Высокий'}
    VALID_STATUS = {'Не выполнена', 'Выполнена'}
    seen_ids = set()

    @classmethod
    def validate_task(
            cls, data: Dict[str, str | int]
    ) -> Dict[str, str | int] | bool:
        if data['id'] in cls.seen_ids or not data['id']:
            print('В файле повторяются id задач/у задачи отсутствует id')
        cls.seen_ids.add(data['id'])
        task_data = {
                'id': data['id'],
                'title': cls._validate_non_null_str(
                    data.get('title', '')
                ),
                'description': cls._validate_non_null_str(
                    data.get('description', '')
                ),
                'category': cls._validate_non_null_str(
                    data.get('category', '')
                ),
                'due_date': cls._validate_due_date(
                    data.get('due_date', '')
                ),
                'priority': cls._validate_priority(
                    data.get('priority', '')
                ),
                'status': cls._validate_status(
                    data.get('status', 'Не выполнена')
                )
            }

        if any(value is False for value in task_data.values()):
            return False

        return task_data

    @staticmethod
    def _validate_due_date(due_date: str) -> str | bool:
        try:
            datetime.strptime(due_date, "%d-%m-%Y")
            return due_date
        except ValueError:
            print("[ОШИБКА ВАЛИДАЦИИ] Дата должна быть в формате ДД-ММ-YYYY.")
            return False

    @staticmethod
    def _validate_non_null_str(data: str) -> str | bool:
        if not data or len(data.strip()) == 0:
            print("[ОШИБКА ВАЛИДАЦИИ] Данные не могут быть пустыми")
            return False
        return data.strip()

    @classmethod
    def _validate_priority(cls, priority: str) -> str | bool:
        if priority not in cls.VALID_PRIORITY:
            print(
                "[ОШИБКА ВАЛИДАЦИИ] Приоритет должен быть:"
                " 'Низкий', 'Средний', 'Высокий'"
            )
            return False
        return priority

    @classmethod
    def _validate_status(cls, status: str) -> str | bool:
        if status not in cls.VALID_STATUS:
            print(
                "[ОШИБКА ВАЛИДАЦИИ] Статус должен быть:"
                " 'Не выполнена' либо 'Выполнена'"
            )
            return False
        return status
