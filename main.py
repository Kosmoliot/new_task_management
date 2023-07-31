import requests, pymongo
import os
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
    
    def view_tasks(self):
        print("Displaying tasks")
    
    def create_task(self):
        print("Creating a task")

    def update_task(self):
        print("Updating a task")
    
    def handle_menu_choice(self, choice):
        if choice == 1:
            self.view_tasks()
        elif choice == 2:
            self.create_task()
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
        
    def handle_menu_choice(self, choice):
        if choice == 1:
            self.view_tasks()
        elif choice == 2:
            self.create_task()
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
        if not menu.handle_menu_choice(choice):
            break

# Adding a user to a group of users in database
# docs = [
#     {"auth": "miguel", "assigned": "miguel", "task_name": "Register Users with task_manager.py", "task_descr": "Use task_manager.py to add the usernames and passwords for all team members that will be using this program.", "d_created": "10 Oct 2019", "d_completed": "17 Oct 201", "d_deadline": "20 Oct 2019", "status": "yes"},
#     {"auth": "admin", "assigned": "admin", "task_name": "Assign initial tasks", "task_descr": "Use task_manager.py to assign each team member with appropriate tasks", "d_created": "10 Oct 2019", "d_completed": "21 Oct 2019", "d_deadline": "25 Oct 2019", "status": "yes"},
#     {"auth": "miguel", "assigned": "miguel", "task_name": "Find a new job", "task_descr": "Use LinkedIn and other websites to look for a new job", "d_created": "28 Nov 2022", "d_completed": "n/a", "d_deadline": "10 Mar 2023", "status": "no"}
#     ]


main()

client.close()
