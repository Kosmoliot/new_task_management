import requests, pymongo
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()
MONGODB_URL = os.environ["MONGODB_URL"]

client = pymongo.MongoClient(MONGODB_URL)
db = client.task_management

collection = db.tasks
menu_text = db.text
users = db.users

class Menu():
    def __init__(self) -> None:
        pass

class User():
    def __init__(self, username, password, user_group) -> None:
        self.username = username
        self.password = password
        self.user_group = user_group
        
    
# Menu to display if user is 'admin'
def admin_menu() -> str:
    main_menu_txt  = menu_text.find_one({"menu": "admin"}, {"_id": 0, "text": 1})     
    menu_input = input(main_menu_txt).lower()
    return menu_input


# Default menu to display for users
def user_menu() -> str: 
    main_menu_txt  = menu_text.find_one({"menu": "main"}, {"_id": 0, "text": 1})    
    menu_input = input(main_menu_txt["text"]).lower()
    return menu_input
    

def login():
    username = input("Please enter your login: \n")
    if users.find_one({"username": username}):
        password = input("Please type in your password: \n")
        match = users.find_one({"username": username, "password": password})
        if match:
            print("Success!")
            user_group = match["access"]
            current_user = User(username, password, user_group)  
            return current_user         
        else:
            print("Incorrect password, try again!")
    else:
        print("Incorrect login, try again!")


def reg_user():
    pass

def add_task():
    pass

def view_all():
    pass

def view_mine():
    pass

def generate_reports():
    pass

def display_stat():
    pass


# Function to call 'menu' funct and handle user's input
# def display_menu(user):     
    # while True:
        
    #     if 
    #         reg_user()

    #     elif menu_input == 'a':
    #         add_task()

    #     elif menu_input == 'va':
    #         view_all()
        
    #     elif menu_input == 'vm':
    #         view_mine()
        
    #     elif menu_input == 'gr' and username == 'admin':
    #         generate_reports()
        
    #     elif menu_input == 'ds' and username == 'admin':
    #         display_stat()

    #     elif menu_input == 'e':
    #         print('Goodbye!!!')
    #         exit()
            
    #     else:
    #         print("\nYou have made a wrong choice, Please Try again")

# user_group("admin")

# for i in users.find({"users.username": "admin"}, {"_id":0, "users.username":1}):

# main_menu_txt  = menu_text.find_one({"menu": "main"}, {"_id": 0, "text": 1})    
# menu_input = input(main_menu_txt["text"]).lower()

# for i in users.find_one({"users.username": "admin"}, {"_id":0, "users.username":1}):
#     print(i)


# Adding a user to a group of users in database
# users.update_one(
#     {"_id": ObjectId("649cb45ccffda00e57610af3")},  # Specify the filter condition
#     {"$push": {"users": {"username": "miguel", "password": "pass"}}}  # Use $push to add the embedded document
# )


print(login().username)

client.close()
