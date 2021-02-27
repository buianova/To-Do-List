from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm.session import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f'{self.id} {self.task}'


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

menu = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
"""

user_input = input(menu)
while user_input != "0":
    if user_input == '1':
        # print("Today:")
        today_rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        deadline = datetime.today().date()
        month = deadline.strftime('%b')
        day = deadline.today().day
        user_strptime = str(deadline)
        if today_rows:
            i = 1
            print(f'Today {month} {day}:')
            for row in today_rows:
                print(f'{i}. {row.task}')
                i += 1
        else:
            print("Nothing to do!")
        print()
        user_input = input(menu)

    if user_input == '2':
        print()
        for i in range(7):
            today = datetime.today()
            output_date = today + timedelta(days=i)
            deadline = output_date.date()
            month = deadline.strftime('%b')
            day = deadline.day
            deadline_weekday = weekdays[deadline.weekday()]
            print(f'{deadline_weekday} {month} {day}:')
            output_rows = session.query(Table).filter(Table.deadline == output_date.date()).all()
            if output_rows:
                i = 1
                for row in output_rows:
                    print(f'{i}. {row.task}')
                    i += 1
                print()
            else:
                print("Nothing to do!")
                print()
        user_input = input(menu)

    if user_input == '3':
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            i = 1
            for row in rows:
                deadline = row.deadline
                month = deadline.strftime('%b')
                day = deadline.day
                print(f'{i}. {row.task}. {day} {month}')
                i +=1
        else:
            print("Nothing to do!")
        print()
        user_input = input(menu)

    if user_input == '4':
        print()
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
        if rows:
            print("Missed tasks:")
            i = 1
            for row in rows:
                deadline = row.deadline
                month = deadline.strftime('%b')
                day = deadline.day
                print(f'{i}. {row.task}. {day} {month}')
                i +=1
        else:
            print("""
            Missed tasks: 
            Nothing is missed!
            """)
        print()
        user_input = input(menu)

    if user_input == '5':
        print()
        print("Enter task")
        task_input = input()
        print("Enter deadline")
        deadline_input = input()
        deadline_input_datetime = datetime.strptime(deadline_input, '%Y-%m-%d')
        new_row = Table(task=task_input, deadline=deadline_input_datetime)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
        # print()
        user_input = input(menu)

    if user_input == '6':
        print("Choose the number of the task you want to delete:")
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            i = 1
            for row in rows:
                deadline = row.deadline
                month = deadline.strftime('%b')
                day = deadline.day
                print(f'{i}. {row.task}. {day} {month}')
                i +=1
            delete_input = int(input())
            specific_row = rows[delete_input - 1]
            session.delete(specific_row)
            session.commit()
            print("The task has been deleted!")
        else:
            print("Nothing to do!")
        print()
        user_input = input(menu)

if user_input == '0':
    print("Bye!")
