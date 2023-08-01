import pymongo
import os
from datetime import datetime
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()
MONGODB_URL = os.environ["MONGODB_URL"]

client = pymongo.MongoClient(MONGODB_URL)
db = client.task_management

tasks = db.tasks
users = db.users

class Menu:
    def __init__(self) -> None:
        pass
    
    def show_menu(self):
        print("1. View tasks")
        print("2. Create task")
        print("3. Update task")
        print("4. Exit")
    
    def view_tasks(self, username):
        cursor = tasks.find({"assigned": username}, {"_id": 0, "title": 1})
        for i in cursor:
            print(i)
    
    def create_task(self, username):
        title = (input("Please enter a title of a task: "))
        description = (input("Please enter a description of the task: "))
        deadline = (input("Please enter a due date (DD MMM YYYY): "))
        created = datetime.today().strftime("%d %b %Y")
        tasks.insert_one(
            {"assigned": username, "title": title, "description": description,
             "created": created, "completed": "n/a", "deadline": deadline, "status": "no"}
        )

    def update_task(self):
        print("Updating a task")
    
    def handle_menu_choice(self, choice, username):
        if choice == 1:
            self.view_tasks(username)
        elif choice == 2:
            self.create_task(username)
        elif choice == 3:
            self.update_task()
        elif choice == 4:
            print("Exiting...")
            return False
        else:
            print("Invalid choice. Please try again.")
        return True

class AdminMenu(Menu):
    def __init__(self) -> None:
        super().__init__()
    
    def show_menu(self):
        print("1. View tasks")
        print("2. Create task")
        print("3. Update task")
        print("4. View statistics")
        print("5. Generate report")
        print("6. Register a user")
        print("7. Exit")
        

    def view_stats(self):
        print("Displaying statistics")
        
    def generate_reports(self):
        print("Generating report")
    
    def reg_user(self):
        print("Registering a user")
        
    def handle_menu_choice(self, choice, username):
        if choice == 1:
            self.view_tasks(username)
        elif choice == 2:
            self.create_task(username)
        elif choice == 3:
            self.update_task()
        elif choice == 4:
            self.view_stats()
        elif choice == 5:
            self.generate_reports()
        elif choice == 6:
            self.reg_user()
        elif choice == 7:
            print("Exiting...")
            return False
        else:
            print("Invalid choice. Please try again.")
        return True

class User():
    def __init__(self, username, password, user_group) -> None:
        self.username = username
        self.password = password
        self.user_group = user_group
    
    
def login():
    username = input("Please enter your login: \n")
    if users.find_one({"username": username}):
        password = input("Please type in your password: \n")
        match = users.find_one({"username": username, "password": password})
        if match:
            print("Success!")
            user_group = match["access"]
            return User(username, password, user_group)           
        else:
            print("Incorrect password, try again!")
    else:
        print("Incorrect login, try again!")


def main():
    user = login()
    if user.user_group == "master":
        menu = AdminMenu()
    else:
        menu = Menu()
    
    while True:
        menu.show_menu()
        choice = int(input("Enter your choice: "))
        if not menu.handle_menu_choice(choice, user.username):
            break

# Adding a user to a group of users in database
# docs = [
#     { "assigned": "miguel", "title": "Register Users with task_manager.py", "description": "Use task_manager.py to add the usernames and passwords for all team members.", "created": "10 Oct 2019", "completed": "17 Oct 201", "deadline": "20 Oct 2019", "status": "yes"},
#     {"assigned": "admin", "title": "Assign initial tasks", "description": "Use task_manager.py to assign each team member with appropriate tasks.", "created": "10 Oct 2019", "completed": "21 Oct 2019", "deadline": "25 Oct 2019", "status": "yes"},
#     {"assigned": "miguel", "title": "Find a new job", "description": "Use LinkedIn and other websites to look for a new job.", "created": "28 Nov 2022", "completed": "n/a", "deadline": "10 Mar 2023", "status": "no"}
#     ]

# tasks.insert_many(docs)

main()

client.close()
