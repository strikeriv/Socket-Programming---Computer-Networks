import socket

HOST = "127.0.0.1"
PORT = 8080

balance: int = 0
    
def deposit(amount: int):
    global balance 
    balance += amount
    
    return f'good:{balance}'
   
def withdraw(amount: int):
    global balance 
    
    if amount > balance:
        return 'bad:0'
    
    balance -= amount
    
    return f'good:{balance}'
 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    print('Server is running.\n')
    
    while True:
        conn, addr = s.accept()
        
        with conn:
            print(f"\nSocket has connected with address: {addr}.")
            
            while True:
                message = conn.recv(1024).decode()
                if not message:
                    break
                
                # split message by : to determine command
                [command, value] = message.split(':')
                
                if command == 'deposit':
                    message = deposit(int(value))

                    conn.sendall(message.encode())
                elif command == 'withdraw':
                    message = withdraw(int(value))
    
                    conn.sendall(message.encode())
                elif command == 'balance':
                    message = f'good:{balance}'

                    conn.sendall(message.encode())  
                else:
                    conn.sendall('bad:None'.encode()) 
                    
            print(f"Socket has disconnected with address: {addr}.\n")
            
            