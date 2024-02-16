import pymongo, os
from datetime import datetime
from dotenv import load_dotenv

# Loading MongoDB connection string from .env file
load_dotenv()
MONGODB_URL = os.environ["MONGODB_URL"]

client = pymongo.MongoClient(MONGODB_URL)
db = client.task_management

tasks = db.tasks
users = db.users

# Creating User class that will be used for a guest users with limited functionality
class User():
    def __init__(self, username, password, user_group) -> None:
        self.username = username
        self.password = password
        self.user_group = user_group
    
    def show_menu(self):
        print("1. View your tasks")
        print("2. Create new task")
        print("3. Update task")
        print("4. Delete task")
        print("5. View statistics")
        print("6. Exit")
    
    # Function returning an object containing specific user tasks to be called 
    # in other class functions
    def user_tasks(self, username):
        cursor = tasks.find({"assigned": username}, {"_id": 0, "title": 1, "description": 1})
        return list(cursor)
      
    def view_tasks(self, username):
        results = self.user_tasks(username)
        for i, task in enumerate(results, start=1):
            print(f"{i}. {task}")
        print("\n")
    
    def update_task(self, username):  # Function to select a task for editing
        self.view_tasks(username)
        task_nr = int(input("Please choose task's nr to edit or type '-1' to exit: "))
        sel_tasks = self.user_tasks(username)
        if task_nr in range(1, len(sel_tasks) + 1):
            self.task_edit(username, sel_tasks[task_nr - 1])
        else:
            print("Incorrect task number, please try again.")
            
    def task_edit(self, username, sel_task): # Function to edit selected task
        if list(tasks.find({"assigned": username, "title": sel_task["title"]}))[0]['status'] != 'no':   # Only uncompleted task can be edited
            edit_opt = input("""Please select one of the following options below
    u\t-\tChange username whom task is assigned to
    d\t-\tChange task's due date
    r\t-\tReturn to task selection
    :""")
            if edit_opt == 'u':
                new_task_user = input("Type new user")    # Calls function to request username
                tasks[task_nr][0] = new_task_user   # Edits coresponding item in tasks dict
            elif edit_opt == 'd':
                new_due_date = input("What is the new due date: ")
                tasks[task_nr][4] = new_due_date    # Changes due date in tasks dict
            elif edit_opt == 'r':
                task_options(task_nr)
            elif edit_opt == 'c':                   # Changes status to "Complete"
                pass
        else:
            print("\nTask has been completed and therefore cannot be edited.")
            
    # Function to create a task for the logged-in user
    def create_task(self, username):
        title = input("Please enter a title of a task: ")
        description = input("Please enter a description of the task: ")
        try:    # Using try/except to catch incorrect value input
            # Formatting deadline date input
            date_input = datetime.strptime(input("Please enter a due date (DD MMM YYYY): "), "%d %b %Y")
            deadline = date_input.strftime("%d %b %Y")
            created = datetime.today().strftime("%d %b %Y")
            tasks.insert_one(
            {"assigned": username, "title": title, "description": description,
             "created": created, "completed": "n/a", "deadline": deadline, "status": "no"}
            )
        except ValueError:
            print("Incorrect date format. Please try again.")

    # Function to delete a task
    def delete_task(self, username):
        results = self.user_tasks(username)
        if not results:
            print("No documents found.")
            return
    # Displaying a list of tasks and using enumerate to create indexing so we could
    # delete a specific task chosen by the user from the list
        self.view_tasks(username)
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
        
    def view_stats(self, username):
        # Calling calculation function
        results = self.report_calcul(list(tasks.find({"assigned": username})))
        total_tasks, compl_tasks, overdue_tasks, compl_perc, incomp_perc, overdue_perc = results
        
        print(f"""\n\t\t\t*** User's Statistics: {username} ***\n
        Total number of tasks assigned:\t\t\t\t\t\t{total_tasks}      
        The percentage of completed tasks:\t\t\t\t\t{round(compl_perc)}
        The percentage of uncompleted tasks:\t\t\t\t\t{round(incomp_perc)}
        The percentage of tasks that overdue:\t\t\t\t\t{round(overdue_perc)}\n\n""")
            
    def report_calcul(self, source):
        total_tasks = len(source)
        compl_tasks, overdue_tasks, compl_perc, incomp_perc, overdue_perc = 0, 0, 0, 0, 0

        for task in source:
            deadline = datetime.today() > datetime.strptime(task["deadline"], "%d %b %Y")
            if task["status"].lower() == "yes":    # Counting amount of completed tasks
                compl_tasks += 1
            elif (task["status"].lower() == "no") and deadline:
                overdue_tasks += 1  # Counting amount of overdue tasks
            
        if total_tasks != 0:    # Avoiding division by zero
            if total_tasks == compl_tasks:
                overdue_perc = 0
                compl_perc = 100
            else:
                overdue_perc = overdue_tasks * 100 / (total_tasks - compl_tasks)
                compl_perc = compl_tasks * 100 / total_tasks
                incomp_perc = 100 - compl_perc
        else:
            incomp_perc, compl_perc, overdue_perc = 0, 0, 0
                
        return total_tasks, compl_tasks, overdue_tasks, compl_perc, incomp_perc, overdue_perc 
               
    def handle_menu_choice(self, choice, username):
        if choice == 1:
            self.view_tasks(username)
        elif choice == 2:
            self.create_task(username)
        elif choice == 3:
            self.update_task(username)
        elif choice == 4:
            self.delete_task(username)
        elif choice == 5:
            self.view_stats(username)
        elif choice == 6:
            print("Exiting...")
            return False
        else:
            print("Invalid choice. Please try again.")
        return True

# User child class with additional functionality
class Admin(User):
    def __init__(self, username, password, user_group) -> None:
        super().__init__(username, password, user_group)
    
    def show_menu(self):
        print("1. View your tasks")
        print("2. View all tasks")
        print("3. Create new task")
        print("4. Update task")
        print("5. Delete task")
        print("6. View statistics")
        print("7. Generate report")
        print("8. Register a user")
        print("9. Delete a user")
        print("10. Exit")
    
    
    def view_all_tasks(self): # View all tasks
        cursor = list(tasks.find({}, {"_id":0}))
        for i, task in enumerate(cursor, start=1):
            print(f"{i}. {task}")
        print("\n")
            
    def generate_report(self):   # Generate report by calling calculations function
        results = self.report_calcul(list(tasks.find()))
        total_tasks, compl_tasks, overdue_tasks, compl_perc, incomp_perc, overdue_perc = results
        
        print(f"""\t\t\t*** Overall Task Statistics ***\n
        Total number of tasks:\t\t\t\t\t\t\t{total_tasks}
        The total number of completed tasks:\t\t\t\t\t{compl_tasks}
        The total number of uncompleted tasks:\t\t\t\t\t{total_tasks - compl_tasks}
        The total number of uncompleted and overdue tasks:\t\t\t{overdue_tasks}
        The percentage of tasks that are incomplete:\t\t\t\t{round(incomp_perc)}
        The percentage of tasks that overdue:\t\t\t\t\t{round(overdue_perc)}\n""")
        
    def reg_user(self):     # Function to register a new usermame      
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
                    
    def delete_user(self):
        user_list = users.find({}, {"_id": 0, "username": 1})
        for i, name in enumerate(user_list, start=1):
            print(f"{i}. {name['username']}")
        
        delete_username = input("Type the username to delete: ")
        if users.find_one({"username": delete_username}):
            users.delete_one({"username": delete_username})
            print(f"Username {delete_username} has been successfully deleted!")
        else:
            print("No such username. Please try again.")
            
    def handle_menu_choice(self, choice, username):
        if choice == 1:
            self.view_tasks(username)
        elif choice == 2:
            self.view_all_tasks()
        elif choice == 3:
            self.create_task(username)
        elif choice == 4:
            self.update_task(username)
        elif choice == 5:
            self.delete_task(username)
        elif choice == 6:
            self.view_stats(username)
        elif choice == 7:
            self.generate_report()
        elif choice == 8:
            self.reg_user()        
        elif choice == 9:
            self.delete_user()
        elif choice == 10:
            print("Exiting...")
            return False
        else:
            print("Invalid choice. Please try again.")
        return True

    
def login():
    username = input("Please enter your login: \n")
    if users.find_one({"username": username}):
        password = input("Please type in your password: \n")
        match = users.find_one({"username": username, "password": password})
        if match:
            print("Success!")
            user_group = match["access"]
            return [username, password, user_group]      
        else:
            print("Incorrect password, try again!")
    else:
        print("Incorrect login, try again!")

def main():
    user_details = login()
    if user_details != None:
        if user_details[2] == "admin":
            user = Admin(*user_details)
        else:
            user = User(*user_details)
        
        while True:
            user.show_menu()
            try:
                choice = int(input("Enter your choice: \n"))
            except ValueError:
                print("Input should be a number, try again.")
                continue
            if not user.handle_menu_choice(choice, user.username):
                break

main()

client.close()
