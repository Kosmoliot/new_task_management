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
        print("1. Create task")
        print("2. Delete task")
        print("3. View tasks")
        print("4. View statistics")
        print("5. Exit")
    
    def user_tasks(self, username):
        return tasks.find({"assigned": username}, {"_id": 0, "title": 1})
      
    def view_tasks(self, username):
        cursor = self.user_tasks(username)
        for index, task in enumerate(cursor, start=1):
            print(f"{index}. : {task}.")
        print("\n")
        
    def create_task(self, username):
        title = input("Please enter a title of a task: ")
        description = input("Please enter a description of the task: ")
        try:
            date_input = datetime.strptime(input("Please enter a due date (DD MMM YYYY): "), "%d %b %Y")
            deadline = date_input.strftime("%d %b %Y")
            created = datetime.today().strftime("%d %b %Y")
            tasks.insert_one(
            {"assigned": username, "title": title, "description": description,
             "created": created, "completed": "n/a", "deadline": deadline, "status": "no"}
            )
        except ValueError:
            print("Incorrect date format. Please try again.")

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
        
    def view_stats(self, username): # Report print template for each user
        results = self.report_calcul(list(tasks.find({"assigned": username})))   # Calling calculation function
        total_tasks, compl_tasks, overdue_tasks, compl_perc, incomp_perc, overdue_perc = results
        
        print(f"""\n\t\t\t*** User's Statistics: {username} ***\n
        Total number of tasks assigned:\t\t\t\t\t\t{total_tasks}      
        The percentage of completed tasks:\t\t\t\t\t{round(compl_perc)}
        The percentage of uncompleted tasks:\t\t\t\t\t{round(incomp_perc)}
        The percentage of tasks that overdue:\t\t\t\t\t{round(overdue_perc)}\n\n""")
            
    def report_calcul(self, source):
        total_tasks = len(source)
        compl_tasks = 0
        overdue_tasks = 0
        overdue_perc = 0
        
        for task in source:
            deadline = datetime.today() > datetime.strptime(task["deadline"], "%d %b %Y")
            if task["status"].lower() == "yes":    # Counting amount of completed tasks
                compl_tasks += 1
            elif (task["status"].lower() == "no") and deadline:
                overdue_tasks += 1  # Counting amount of overdue tasks
            
        if total_tasks != 0:    # Avoiding division by zero
            if total_tasks == compl_tasks:
                overdue_perc = 0
            else:
                overdue_perc = overdue_tasks * 100 / (total_tasks - compl_tasks)
                compl_perc = compl_tasks * 100 / total_tasks
                incomp_perc = 100 - compl_perc
        else:
            incomp_perc = 0
            compl_perc = 0
            overdue_perc = 0
            
        return total_tasks, compl_tasks, overdue_tasks, compl_perc, incomp_perc, overdue_perc 
               
    def handle_menu_choice(self, choice, username):
        if choice == 1:
            self.create_task(username)
        elif choice == 2:
            self.delete_task(username)
        elif choice == 3:
            self.view_tasks(username)
        elif choice == 4:
            self.view_stats(username)
        elif choice == 5:
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
        print("7. Delete a user")
        print("8. Exit")
        
    def generate_report(self):   # Generate report and write it to 'task_overview.txt'
        results = self.report_calcul(list(tasks.find()))
        total_tasks, compl_tasks, overdue_tasks, compl_perc, incomp_perc, overdue_perc = results
        
        print(f"""\t\t\t*** Overall Task Statistics ***\n
        Total number of tasks:\t\t\t\t\t\t\t{total_tasks}
        The total number of completed tasks:\t\t\t\t\t{compl_tasks}
        The total number of uncompleted tasks:\t\t\t\t\t{total_tasks - compl_tasks}
        The total number of uncompleted and overdue tasks:\t\t\t{overdue_tasks}
        The percentage of tasks that are incomplete:\t\t\t\t{round(incomp_perc)}
        The percentage of tasks that overdue:\t\t\t\t\t{round(overdue_perc)}""")
        
    def reg_user(self):         # Function to register a new usermame      
        new_user = input("Please enter a new username: ")
        if users.find_one({"username": new_user}):   # Checking if username already exists
            print(f"\nUsername '{new_user}' already exists, please try again.\n")        
        else:
            new_pass = input("Please enter you new password: ")
            access = input("Please enter access level (admin/guest): ")
            if access == "guest" or access == "admin" :
                users.insert_one(
                {"username": new_user, "password": new_pass, "access": access})
                print(f"Username {new_user} has been successfully created!")
            else:
                print("Incorrect access level, please start again.")
                    
    def del_user(self):
        user_list = users.find({}, {"_id": 0, "username": 1})
        for i, name in enumerate(user_list, start=1):
            print(f"{i}. {name['username']}")
        
        delete = input("Type the username to delete: ")
        if users.find_one({"username": delete}):
            users.delete_one({"username": delete})
            print(f"Username {delete} has been successfully deleted!")
        else:
            print("No such username. Please try again.")
            
    def handle_menu_choice(self, choice, username):
        if choice == 1:
            self.view_tasks(username)
        elif choice == 2:
            self.create_task(username)
        elif choice == 3:
            self.delete_task(username)
        elif choice == 4:
            self.view_stats(username)
        elif choice == 5:
            self.generate_report()
        elif choice == 6:
            self.reg_user()        
        elif choice == 7:
            self.del_user()
        elif choice == 8:
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
        if user.user_group == "admin":
            menu = AdminMenu()
        else:
            menu = Menu()
        
        while True:
            menu.show_menu()
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Input should be a number, try again.")
                continue
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
