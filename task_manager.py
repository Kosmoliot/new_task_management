#=====importing libraries====#
from datetime import datetime       # Using module to pull current date data

#====Global variables====#
users = {}      # Username and password will be stored as a key-value pair
tasks = {}      # Each line from task file will be stored as value in a dict
user_tasks = {} # Dictionary to store tasks for each user in 'user: task' pair
menu_input = ""
username = ""

#====File Access====#
def user_update():      # Function to create/update 'users' dictionary 
    with open("user.txt", "r") as file:
        for line in file:
            line = line.strip('\n')
            users[line.split(', ')[0]] = line.split(', ')[1]
           
def tasks_update():     # Function to create/update 'tasks' dictionary
    with open("tasks.txt", "r") as tasks_file:
        for key, line in enumerate(tasks_file, 1):  # Iterating throug lines in tasks.txt
            tasks[key] = line.strip("\n").split(", ")
    
#====Menu Items====#
def admin_menu():       # Menu to display if user is 'admin'
    global menu_input
    menu_input = input('''\nSelect one of the following Options below:
r\t-\tRegistering a user
a\t-\tAdding a task
va\t-\tView all tasks
vm\t-\tView my task
gr\t-\tGenerate reports
ds\t-\tDisplay Statistics
e\t-\tExit
: ''').lower()
    
def user_menu():        # Default menu to display for users
    global menu_input
    menu_input = input('''\nSelect one of the following Options below:
r\t-\tRegistering a user
a\t-\tAdding a task
va\t-\tView all tasks
vm\t-\tView my task
e\t-\tExit
: ''').lower()
    
def load_menu():        # Conditional check to display appropriate menu
    if username == 'admin':
        admin_menu()
    else:
        user_menu()

def display_menu():     # Function to call 'menu' funct and handle user's input
    while True:
        tasks_update()  # Updating both 'tasks' and 'users' dictionaries
        user_update()

        load_menu()     # Checking if user is 'admin' and requesting input
        
        if menu_input == 'r' and username == 'admin':
            reg_user()

        elif menu_input == 'a':
            add_task()

        elif menu_input == 'va':
            view_all()
        
        elif menu_input == 'vm':
            view_mine()
        
        elif menu_input == 'gr' and username == 'admin':
            generate_reports()
        
        elif menu_input == 'ds' and username == 'admin':
            display_stat()

        elif menu_input == 'e':
            print('Goodbye!!!')
            exit()
            
        else:
            print("\nYou have made a wrong choice, Please Try again")

#====Login Section====#
def validate_user():    # Checking if username is registered
    global username
    username = input("Please enter your username: ")
    while username not in users:
        username = input("Incorrect username, please try again: ")

def validate_pass():    # Validating user's password
    passw_input = input(f"Hello {username}! Please enter your password: ")
    while True:
        if passw_input == users[username]:
            print(f"Welcome back {username}!")
            break
        else:
            passw_input = input("Incorrect password, please try again: ")
            
def get_user_input():   # To be used to register new username and creating new task
    while True:
        user_input = input("Please enter a username who you want to assign task to: ")
        if user_input not in users.keys():
            print("There's no such username, please try again.")
        else:
            return(user_input)

def reg_user():         # Function to register a new usermame      
    with open("user.txt", "a") as file: 
        new_user = input("Please enter a new username: ")
        if new_user in users:   # Checking if username already exists
            print(f"\nUsername '{new_user}' already exists, please try again.\n")        
        else:
            new_pass = input("Please enter you new password: ")
            pass_check = input("Please confirm you new password: ")
            if pass_check != new_pass:
                print("Your passwords don't match, please start again.")
            elif pass_check == new_pass:    # If passwords match, saving the entry
                print("\nCongrats! You have created a new username!")
                file.write(f"\n{new_user}, {new_pass}")

#====Task Management====#
def task_templ(key, def_dict):      # Print template for 'view_all' and 'view_mine'
    print("_" * 70 + "\n")
    print(f"""Task nr. {key}:\t\t\t{def_dict[key][1]}
Assgined to:\t\t\t{def_dict[key][0]}\nDate assigned:\t\t\t{def_dict[key][3]}
Due date:\t\t\t{def_dict[key][4]}\nTask Complete?\t\t\t{def_dict[key][5]}
Task description:\n{def_dict[key][2]}
""")
        
def add_task():     # Function to create new task
    with open("tasks.txt", "a") as tasks_file:
        user_task = get_user_input()
        title_task = (input("Please enter a title of a task: "))
        descr_task = (input("Please enter a description of the task: "))
        due_date = (input("Please enter a due date (DD MMM YYYY): "))
        today_date = datetime.today().strftime("%d %b %Y")
        tasks_file.write(f"\n{user_task}, {title_task}, {descr_task}, {today_date}, ")
        tasks_file.write(f"{due_date}, No")    

def view_all():     # Reading all tasks from 'tasks' dictionary and printing them
    for key in tasks:
        task_templ(key, tasks)
    print("_" * 70 + "\n")
               
def view_mine():    # Iterating through 'tasks' dict to find tasks assigned to a user
    tasks_update()
    for key in tasks:
        if tasks[key][0] == username:
            task_templ(key, tasks)
    print("_" * 70 + "\n")
    task_select()   # Calling a function to select task for editing
    with open("tasks.txt", "w+") as tasks_file: # Writing all task to tasks.txt
        string = []
        for task_line in tasks.values():
            string.append(', '.join(task_line))
        tasks_file.write('\n'.join(string))

def task_select():  # Function to select a task for editing
    task_nr = int(input("Please choose task's nr to edit or type '-1' to exit: "))
    if task_nr in tasks.keys():
        task_options(task_nr)
    else:
        print("Incorrect task number, please try again.")

def task_options(task_nr):  # Function to choose task editing option
    task_opt = input("""\nPlease select one of the following options below
e\t-\tEdit task
c\t-\tMark as 'complete'
r\t-\tReturn to task selection
:""")
    if task_opt == 'e':
        task_edit(task_nr)
    elif task_opt == 'c':
        tasks[task_nr][5] = 'Yes'
        print(f"\nTask nr {task_nr} has been marked as complete.")
    elif task_opt == 'r':
        view_mine()     # Calls view_mine function to choose task or exit
        
def task_edit(task_nr): # Function to edit selected task
    if tasks[task_nr][5] == 'No':   # Only uncomplted task can be edited
        edit_opt = input("""Please select one of the following options below
u\t-\tChange username whom task is assigned to
d\t-\tChange task's due date
r\t-\tReturn to task selection
:""")
        if edit_opt == 'u':
            new_task_user = get_user_input()    # Calls function to request username
            tasks[task_nr][0] = new_task_user   # Edits coresponding item in tasks dict
        elif edit_opt == 'd':
            new_due_date = input("What is the new due date: ")
            tasks[task_nr][4] = new_due_date    # Changes due date in tasks dict
        elif edit_opt == 'r':
            task_options(task_nr)
    else:
        print("\nTask has been completed and therefore cannot be edited.")

#====Report Management====#
def generate_reports():     # Funtion to generate reports
    user_report_output()    
    task_report_output()

def get_file(file):     # Funtion to read .txt files and print them line by line
    with open(file, 'r') as user_file:
        for line in user_file:
            print(line.strip('\n'))
            
def display_stat():     # Function to generate reports and then display them on screen
    generate_reports()
    files = ['user_overview.txt', 'task_overview.txt']
    for file in files:
        get_file(file)
        
def report_calcul(source):      # Function to make calculations needed for reports
    global overdue_tasks, total_tasks, compl_tasks
    global overdue_perc, incomp_perc, compl_perc
    total_tasks = len(source)
    compl_tasks = 0
    overdue_tasks = 0
    
    for line in source.values():    # 'source' is either 'tasks' or 'user_tasks' dict
        due_date = datetime.today() > datetime.strptime(line[4], "%d %b %Y")
        if line[5] == "Yes":    # Counting amount of completed tasks
            compl_tasks += 1
        elif (line[5] == 'No') and due_date:
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

def user_report_template(username): # Report print template for each user
    report_calcul(user_tasks)   # Calling calculation function
    
    with open('user_overview.txt', 'a+') as t_reports:
        t_reports.write(f"""\n\t\t\t*** User's Statistics: {username} ***\n
Total number of tasks assigned:\t\t\t\t\t\t{total_tasks}      
The percentage of completed tasks:\t\t\t\t\t{round(compl_perc)}
The percentage of uncompleted tasks:\t\t\t\t\t{round(incomp_perc)}
The percentage of tasks that overdue:\t\t\t\t\t{round(overdue_perc)}\n\n""")
        
def user_report_output():   # Main individual user report function
    with open('user_overview.txt', 'w+') as file:
        file.truncate() # Creating file and emptying it so we could use '+a'
    user_update()       # for writing each user's report im succesion using for loop
    tasks_update()
    
    with open('user_overview.txt', 'w+') as user_file:
        user_file.write(f"""\t\t\t*** Overall User Statistics ***\n
Total amount of task in Task Manager:\t\t\t\t\t{len(tasks)}
Total amount of users in Task Manager:\t\t\t\t\t{len(users)}\n""")
        
    for username in users.keys():   # Interating through 'tasks' to check how
        user_tasks.clear()          # many task are assigned to a specific user
        for key in tasks.keys():
            if tasks[key][0] == username:
                user_tasks[key] = tasks[key]
        user_report_template(username)  # Writing output for each user to tasks.txt
                
def task_report_output():   # Generate report and write it to 'task_overview.txt'
    report_calcul(tasks)
        
    with open('task_overview.txt', 'w+') as t_reports:
        t_reports.write(f"""\t\t\t*** Overall Task Statistics ***\n
Total number of tasks:\t\t\t\t\t\t\t{total_tasks}
The total number of completed tasks:\t\t\t\t\t{compl_tasks}
The total number of uncompleted tasks:\t\t\t\t\t{total_tasks - compl_tasks}
The total number of uncompleted and overdue tasks:\t\t\t{overdue_tasks}
The percentage of tasks that are incomplete:\t\t\t\t{round(incomp_perc)}
The percentage of tasks that overdue:\t\t\t\t\t{round(overdue_perc)}""")

#====Main structure====#
user_update()   # Creating user dictionary with username: password pair
tasks_update()  # Creating tasks dictionary with int as key and task as value

validate_user() # Validating user
validate_pass() # Validating password

display_menu()  # Main while loop for menu