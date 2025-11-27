import json
import socket
"""
Client - Main PC
Send instructions to server (UTM)
Receive experimental data returned by UTM
"""
# Initialize
# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(("0.0.0.0", 8888))
server_host = '192.168.3.86'
server_port = 8080
# Connect to the server
client_socket.connect((server_host, server_port))

def UTM_control(send_order, specimen_serial):
    """
    Communicate with the UTM control PC
    """
    # Send data
    message = send_order
    client_socket.sendall(message.encode())
    print('Test command sent')
    message = specimen_serial
    client_socket.sendall(message.encode())
    print('Specimen serial number sent')
    # Receive data
    mechanics_data = None
    while True:
        # Receive server response
        data = client_socket.recv(1024)  # Blocking
        data_str = data.decode()
        print(f"Message received from server: {data_str}")
        if data_str == 'Test_finished_sending_data':
            json_str = client_socket.recv(1024).decode()
            # Convert string to dictionary
            mechanics_data = json.loads(json_str)
        if data_str == 'over':
            # Close connection
            print('Session ended')
            break

    return mechanics_data

