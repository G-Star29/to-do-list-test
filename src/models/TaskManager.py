import json
import re
import os

from collections import defaultdict
from typing import List, Dict, Iterable, Set, Tuple
from .Task import Task
from .TaskValidation import TaskValidation


class TaskManager:
    def __init__(self, file: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/tasks.json'))):
        self.file: str = file
        self.id_index_tasks: Dict[int, Task]\
            = self._load_tasks()
        self.category_index_tasks: Dict[str, List[Task]]\
            = self._build_category_index()
        self.current_id: int = self._get_max_id()

    def _build_category_index(self) -> Dict[str, List[Task]]:
        index = defaultdict(list)
        for task in self.id_index_tasks.values():
            index[task.category.lower()].append(task)
        return index

    def _load_tasks(self) -> dict[int, Task]:
        try:
            with open(self.file, 'r', encoding='utf-8') as file_to_load:
                try:
                    data = json.load(file_to_load)
                except json.decoder.JSONDecodeError:
                    print(f'Файл {self.file} пуст')
                    data = []
                validate_data = []
                for data_item in data:
                    if TaskValidation.validate_task(data_item):
                        validate_data.append(data_item)
                    else:
                        raise ValueError(
                            f'[ОШИБКА ВАЛИДАЦИИ] В файле {self.file}'
                            f' задача ID: {data_item["id"]} содержит ошибку!'
                        )
                return {
                    validate_data_item['id']: Task(**validate_data_item)
                    for validate_data_item in validate_data
                }
        except FileNotFoundError:
            raise FileNotFoundError(f'{self.file} не найден')

    def _get_max_id(self) -> int:
        if not self.id_index_tasks.keys():
            return 0
        return max(self.id_index_tasks.keys())

    def add_task(self, data: Dict[str, str | int]) -> bool:
        task_id = self.current_id
        data['id'] = task_id + 1
        validate_data = (TaskValidation.
                         validate_task(data))
        if validate_data:
            self.current_id += 1
            (self.category_index_tasks[data['category']]
             .append(Task(**validate_data)))
            self.id_index_tasks[data['id']] = Task(**validate_data)
            return True
        return False

    def find_task_by_id(self, id: int) -> Task | None:
        task = self.id_index_tasks.get(id, None)
        return task if task else None

    def edit_task_by_id(self, id: int, data: Dict[str, str | int]) -> None:
        data['id'] = id
        validate_data = TaskValidation.validate_task(data)
        if validate_data:
            self.id_index_tasks[data['id']] = Task(**validate_data)
            self.category_index_tasks = self._build_category_index()

    def delete_task_by_id(self, id: int) -> None | bool:
        if not self.id_index_tasks.pop(id, None):
            return False
        self.category_index_tasks = self._build_category_index()

    def delete_tasks_by_category(self, category: str) -> None | bool:
        tasks_deleted = self.category_index_tasks.pop(category, None)
        if not tasks_deleted:
            return False
        for task in tasks_deleted:
            self.id_index_tasks.pop(task.id, None)

    def get_tasks(self) -> Iterable[Task]:
        return [task.to_dict() for task in self.id_index_tasks.values()]

    def get_tasks_by_category(self, category: str) -> List[Task] | None:
        if (category not in
                self.category_index_tasks):
            return None
        return [task.to_dict() for task in self.category_index_tasks[category]]

    def get_tasks_by_keywords(
            self, keywords: Set[str])\
            -> Tuple[Dict[int, Task], Dict[int, Task]]:
        matching_in_title = {}
        for task in self.id_index_tasks.values():
            title = task.title.lower()
            if keywords.intersection(re.split(r"[;, ]", title)):
                matching_in_title[task.id] = task.to_dict()

        matching_in_description = {}
        for task in self.id_index_tasks.values():
            description = task.description.lower().splitlines()
            description = ' '.join(description)
            if keywords.intersection(re.split(r"[;, ]", description)):
                matching_in_description[task.id] = task.to_dict()

        return matching_in_title, matching_in_description

    def get_tasks_by_status(self, status: str) -> Iterable[Task]:
        self.id_index_tasks.values()
        return [
            task.to_dict() for task in self.id_index_tasks.values()
            if task.status.lower() == status
        ]

    def save_tasks(self) -> None:
        with open(self.file, "w", encoding="utf-8") as file_to_save:
            json.dump(
                [task.to_dict() for task in self.id_index_tasks.values()],
                file_to_save,
                ensure_ascii=False,
                indent=4
            )
        print(f'Данные сохранены в файл {self.file}')