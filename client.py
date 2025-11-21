# Matthew Craddock 100443869

import socket
import sys

HOST = "127.0.0.1"
PORT = 8080

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connected to server.\n")
except ConnectionRefusedError:
    print("Could not connect to server.")
    sys.exit()

def print_menu() :
    divider = '+---------------------------+'
    
    print(divider)
    print('| Banking Application       |')
    print(divider)
    print('| Choose an option below:   |')
    print(divider)
    print('| 1. Deposit Money          |')
    print('| 2. Withdraw Money         |')
    print('| 3. View Account Balance   |')
    print('| 4. Exit Applicatgion      |')
    print(divider)
    print('\n')

def await_menu_input():
    choice = input("Selection: ")
    
    if choice == "1":
        deposit_money()
    elif choice == "2":
        withdraw_money()
    elif choice == "3":
        view_balance()
    elif choice == "4":
        exit()
    else:
        print("\nInput is invalid.\n")
        
    return True
        
def deposit_money():
    money_to_deposit = input("\nEnter an amount to deposit: $")
    
    try:
        int(money_to_deposit)
    except ValueError:
        print("Input is invalid.\n")
        
        deposit_money()
    
    # send message to server to process
    message = f"deposit:{money_to_deposit}"
    s.sendall(message.encode())
    
    # get response
    response = s.recv(1024).decode()
    [status, _] = response.split(':')
    
    if status == 'good':
        print(f'\nSuccessfully deposited ${money_to_deposit}.\n')
    else:
        print('\nSomething went wrong when depositing.\n')

def view_balance():
    # send message to server to process
    s.sendall("balance:None".encode())
     
    # get response
    response = s.recv(1024).decode()
    [status, balance] = response.split(':')
    
    if status == 'good':
        print(f'\nCurrent Balance: ${balance}.\n')
    else:
        print('\nSomething went wrong when depositing.\n')

def exit():
    print("\nExiting application.")
    sys.exit()

def withdraw_money():
    money_to_withdraw = input("\nEnter an amount to withdraw: $")
    
    try:
        int(money_to_withdraw)
    except ValueError:
        print("Input is invalid.\n")
        
        deposit_money()
    
    # send message to server to process
    message = f"withdraw:{money_to_withdraw}"
    s.sendall(message.encode())
    
    # get response
    response = s.recv(1024).decode()
    [status, code] = response.split(':')

    if status == 'good':
        print(f'\nSuccessfully withdrew ${money_to_withdraw}.\n')
    elif code == '0':
        print('\nInsufficient funds for withdraw.\n')
    else:
        print('\nSomething went wrong when withdrawing.\n')
        
              
def main():
    running = True
    
    while running:
        print_menu()

        running = await_menu_input() 

    s.close()
    
    
main()