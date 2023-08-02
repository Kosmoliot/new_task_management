import pymongo, os
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
        print("3. Delete task")
        print("4. Exit")
    
    def user_tasks(self, username):
        return tasks.find({"assigned": username}, {"_id": 0, "title": 1})
    
        
    def view_tasks(self, username):
        cursor = self.user_tasks(username)
        for index, task in enumerate(cursor, start=1):
            print(f"{index}. : {task}.")
        print("\n")
        
    
    def create_task(self, username):
        title = (input("Please enter a title of a task: "))
        description = (input("Please enter a description of the task: "))
        deadline = (input("Please enter a due date (DD MMM YYYY): "))
        created = datetime.today().strftime("%d %b %Y")
        tasks.insert_one(
            {"assigned": username, "title": title, "description": description,
             "created": created, "completed": "n/a", "deadline": deadline, "status": "no"}
        )

    def delete_task(self, username):
        results = list(self.user_tasks(username))
        
        if not results:
            print("No documents found.")
            return

        print("Available documents:")
        for i, task in enumerate(results, start=1):
            print(f"{i}. {task}")

        try:
            selected_index = int(input("Enter the number of the document to delete: ")) - 1
            if selected_index < 0 or selected_index >= len(results):
                print("Invalid choice. Please select a valid number.")
                return

            selected_document = results[selected_index]
            tasks.delete_one({"assigned": username, "title": selected_document["title"]})
            print("Document deleted successfully.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        
    
    def handle_menu_choice(self, choice, username):
        if choice == 1:
            self.view_tasks(username)
        elif choice == 2:
            self.create_task(username)
        elif choice == 3:
            self.delete_task(username)
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
        print("3. Delete task")
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
            self.delete_task(username)
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
    if user != None:
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

# results = list(tasks.find({"assigned": "dima"}, {"_id": 0, "title": 1}))
# for i, task in enumerate(results, start=1):
#     print(f"{i}. {task}")

main()

client.close()
