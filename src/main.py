import os

from typing import Dict

from models.TaskManager import TaskManager, Task


def task_form() -> Dict[str, str | int]:

    title: str = input('Введите название задачи: ')
    description: str = input('Введите описание задачи: ')
    category: str = input('Укажите категорию задачи: ')
    due_date: str = input('Укажите "дедлайн" ДД-ММ-YYYY: ')
    priority: str = input('Укажите приоритет задачи'
                          ' (Высокий, Средний, Низкий): ')

    task_keys = ['title', 'description', 'category', 'due_date', 'priority']
    task_values = [title, description, category, due_date, priority]

    return dict(zip(task_keys, task_values))


def get_task_by_id() -> Task | None:

    id_task = input('Укажите id задачи: ')
    try:
        id_task = int(id_task)
    except ValueError:
        print('ID - целое число')
        return None
    task = task_manager.find_task_by_id(id_task)
    if task is None:
        print(f'Задачи с ID:{id_task} не существует')
        return None

    return task


if __name__ == '__main__':
    task_manager = TaskManager()
    while True:
        os.system('cls||clear')
        print('1. Вывести все задачи')
        print('2. Просмотр задач по категориям')
        print('3. Добавить задачу')
        print('4. Изменить задачу по ее ID')
        print('5. Изменить статус задачи по ее ID')
        print('6. Удалить задачу')
        print('7. Поиск задач по ключевым словам,'
              ' категории или статусу выполнения')
        choice = input('Ваш выбор:')

        match choice:
            case '1':
                os.system('cls||clear')
                tasks_list = task_manager.get_tasks()
                for task in tasks_list:
                    print(f'{task}\n')
                temp = input()

            case '2':
                os.system('cls||clear')
                category = input('Введите категорию:')
                tasks_list = task_manager.get_tasks_by_category(
                    category=category.strip().lower()
                )
                if tasks_list is None:
                    print(f'Задач с категорией {category} не найдено')
                    temp = input()
                    continue
                for task in tasks_list:
                    print(f'{task}\n')
                temp = input()

            case '3':
                while True:
                    os.system('cls||clear')
                    task = task_form()
                    if task_manager.add_task(task):
                        print('Задача добавлена в список')
                        temp = input()
                    else:
                        print()
                        choice_add = input('Ошибка валидации,'
                                           ' повторить попытку? (y/n)')
                        if choice_add.strip().lower() == 'y':
                            continue
                        else:
                            break

            case '4':
                while True:
                    os.system('cls||clear')
                    task = get_task_by_id()
                    if task is None:
                        temp = input()
                        break
                    print(task.to_dict())
                    confirm_to_correct_task = input('Редактировать? (y/n): ')
                    if confirm_to_correct_task.strip().lower() == 'y':
                        task_new_data = task_form()
                        task_manager.edit_task_by_id(task.id, task_new_data)
                        print(task_manager.find_task_by_id(task.id).to_dict())
                        temp = input()
                        break
                    else:
                        break

            case '5':
                while True:
                    os.system('cls||clear')
                    task = get_task_by_id()
                    if task is None:
                        temp = input()
                        break
                    print(task.to_dict())
                    confirm_to_edit_status_of_task = input(
                        'Задать новый статус?'
                        ' (y/n): '
                    )
                    if confirm_to_edit_status_of_task.strip().lower() == 'y':
                        status = input(
                            'Укажите статус (цифрой):'
                            ' 1. Выполнена, 2. Не выполнена: '
                        )
                        try:
                            status = int(status)
                        except ValueError:
                            print('Необходимо целое число')
                        if status == 1:
                            task.mark_status(True)
                            break
                        elif status == 2:
                            task.mark_status(False)
                            break
                        else:
                            print('Необходимо целое число (1 или 2)')
                            temp = input()
                            break
                    elif confirm_to_edit_status_of_task.strip().lower() == 'n':
                        break
                    else:
                        continue

            case '6':
                while True:
                    os.system('cls||clear')
                    print('1.Удалить задачи по категории')
                    print('2.Удалить задачу по ID')
                    choice_delete = input('1/2?: ')
                    try:
                        choice_delete = int(choice_delete)
                    except ValueError:
                        print('Необходимо целое число')
                    if choice_delete == 1:
                        category_to_delete = input('Укажите категорию: ')
                        if task_manager.delete_tasks_by_category(
                                category_to_delete.strip().lower()
                        ):
                            print(
                                f'Задачи с категорией'
                                f' {category_to_delete} удалены'
                            )
                            temp = input()
                            break
                        else:
                            print(
                                f'Задачи с категорией'
                                f' {category_to_delete} не найдены'
                            )
                            temp = input()
                            break
                    elif choice_delete == 2:
                        task = get_task_by_id()
                        if task is None:
                            temp = input()
                            break
                        task_manager.delete_task_by_id(task.id)
                        break
                    else:
                        continue

            case '7':
                while True:
                    os.system('cls||clear')
                    print('1.Поиск задачи по ключевым словам')
                    print('2.Поиск задачи по статусу выполнения')
                    choice_search = input('1/2?: ')
                    try:
                        choice_search = int(choice_search)
                    except ValueError:
                        print('Необходимо целое число')
                    if choice_search == 1:
                        keywords = input(
                            'Введите ключевые слова через пробел: '
                        )
                        keywords = set(keywords.strip().lower().split(' '))
                        matching_in_title, matching_in_description\
                            = task_manager.get_tasks_by_keywords(keywords)
                        print('Соответствие в названии задач:\n')
                        for key in matching_in_title.keys():
                            print(
                                f'ID: {key},'
                                f' DATA: {matching_in_title[key]}\n'
                            )
                        print('Соответствие в описании задач:\n')
                        for key in matching_in_description.keys():
                            print(
                                f'ID: {key},'
                                f' DATA: {matching_in_description[key]}\n'
                            )
                        temp = input()
                    elif choice_search == 2:
                        status = input(
                            'Укажите статус выполнения'
                            ' (выполнена/не выполнена): '
                        )
                        if (status.strip().lower() == 'выполнена'
                                or status.strip().lower() == 'не выполнена'):
                            tasks = task_manager.get_tasks_by_status(status)
                            print(tasks)
                            temp = input()
                            break
                        else:
                            print('Неверный ввод')
                            temp = input()
                            break
