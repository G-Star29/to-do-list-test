
class Task:

    def __init__(self,
                 id: int,
                 title: str,
                 description: str,
                 category: str,
                 due_date: str,
                 priority: str,
                 status: str
                 ):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def mark_status(self, status: bool):
        if status:
            self.status = 'Выполнена'
        else:
            self.status = 'Не выполнена'

    def to_dict(self):
        return self.__dict__
