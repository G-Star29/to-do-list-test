import os
from typing import Callable

from models.TaskManager import TaskManager, Task


def clear_screen():
    os.system('cls||clear')


def input_with_validation(
        prompt: str,
        validation: Callable[[str], bool] = None
        ) -> str:
    while True:
        user_input = input(prompt)
        if validation and not validation(user_input):
            print("Неверный ввод, попробуйте снова.")
        else:
            return user_input


def menu_view_tasks():
    clear_screen()
    tasks_list = task_manager.get_tasks()
    if tasks_list:
        for task in tasks_list:
            print(f'{task}\n')
    else:
        print("Задач пока нет.")
    input("Нажмите Enter, чтобы продолжить.")


def menu_add_task():
    clear_screen()
    while True:
        task = task_form()
        if task_manager.add_task(task):
            print("Задача добавлена успешно.")
        else:
            print("Ошибка валидации. Попробуйте снова.")
        if input("Добавить еще задачу? (y/n): ").strip().lower() != 'y':
            break


def menu_edit_task():
    clear_screen()
    task = get_task_by_id()
    if task:
        print(task.to_dict())
        if input("Редактировать задачу? (y/n): ").strip().lower() == 'y':
            new_data = task_form()
            task_manager.edit_task_by_id(task.id, new_data)
            print("Задача успешно обновлена.")
    input("Нажмите Enter, чтобы продолжить.")


def menu_delete_task():
    clear_screen()
    print("1. Удалить задачи по категории")
    print("2. Удалить задачу по ID")
    choice = input_with_validation(
        "Ваш выбор (1/2): ",
        lambda x: x in {'1', '2'}
    )
    if choice == '1':
        category = input("Введите категорию: ").strip().lower()
        if task_manager.delete_tasks_by_category(category):
            print(f"Задачи с категорией {category} удалены.")
        else:
            print(f"Задач с категорией {category} не найдено.")
    elif choice == '2':
        task = get_task_by_id()
        if task:
            task_manager.delete_task_by_id(task.id)
            print(f"Задача с ID {task.id} удалена.")
    input("Нажмите Enter, чтобы продолжить.")


def menu_find_tasks():
    clear_screen()
    print("1. Поиск задачи по ключевым словам")
    print("2. Поиск задачи по статусу выполнения")
    choice = input_with_validation(
        "Ваш выбор (1/2): ",
        lambda x: x in {'1', '2'}
    )
    if choice == '1':
        keywords = set(input("Введите ключевые слова через пробел: ").strip().lower().split())
        matching_in_title, matching_in_description = task_manager.get_tasks_by_keywords(keywords)
        print("Соответствие в названии задач:")
        for key, value in matching_in_title.items():
            print(f"ID: {key}, DATA: {value}")
        print("Соответствие в описании задач:")
        for key, value in matching_in_description.items():
            print(f"ID: {key}, DATA: {value}")
    elif choice == '2':
        status = input("Введите статус (выполнена/не выполнена): ").strip().lower()
        tasks = task_manager.get_tasks_by_status(status)
        if tasks:
            for task in tasks:
                print(task)
        else:
            print(f"Задач со статусом '{status}' не найдено.")
    input("Нажмите Enter, чтобы продолжить.")


def menu_save_tasks():
    clear_screen()
    task_manager.save_tasks()
    input("Нажмите Enter, чтобы продолжить.")


def task_form() -> dict:
    title = input("Введите название задачи: ").strip()
    description = input("Введите описание задачи: ").strip()
    category = input("Введите категорию задачи: ").strip()
    due_date = input("Введите дату (ДД-ММ-ГГГГ): ").strip()
    priority = input("Введите приоритет (Низкий, Средний, Высокий): ").strip()
    return {
        'title': title,
        'description': description,
        'category': category,
        'due_date': due_date,
        'priority': priority
    }


def get_task_by_id() -> Task | None:
    id_task = input_with_validation(
        "Введите ID задачи: ",
        lambda x: x.isdigit()
    )
    task = task_manager.find_task_by_id(int(id_task))
    if not task:
        print(f"Задача с ID {id_task} не найдена.")
    return task


# Главное меню
menu_actions = {
    '1': menu_view_tasks,
    '2': menu_add_task,
    '3': menu_edit_task,
    '4': menu_delete_task,
    '5': menu_find_tasks,
    '6': menu_save_tasks,
}


if __name__ == '__main__':
    task_manager = TaskManager()
    while True:
        clear_screen()
        print("Меню:")
        print("1. Просмотр всех задач")
        print("2. Добавить задачу")
        print("3. Редактировать задачу")
        print("4. Удалить задачу")
        print("5. Поиск задач")
        print("6. Сохранить данные в файл")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == '0':
            break
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор. Попробуйте снова.")
