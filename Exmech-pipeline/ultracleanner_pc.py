import socket

def start_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 8080))
    return udp_socket

def get_cleaner_gate():
    """
    Get the ultrasonic machine gate status
    Input: udp_socket
    on: open
    off: close
    """

    udp_socket = start_udp()
    esp32_addr = ('192.168.3.2', 7788)
    send_data = 'get_gate_state'
    udp_socket.sendto(send_data.encode('utf-8'), esp32_addr)
    recv_data, sender_info = udp_socket.recvfrom(1024)
    recv_data_str = recv_data.decode("utf-8")
    print("{} sent: Ultrasonic machine gate status is {}".format(sender_info, recv_data_str))
    udp_socket.close()
    return recv_data_str


def cleaner_gate_control(order, gate_state):
    """
    Control the ultrasonic machine gate
    Input: order
    open - open gate
    close - close gate
    """
    udp_socket = start_udp()
    esp32_addr = ('192.168.3.2', 7788)
    if order == gate_state:
        print("Collision risk")
    else:
        send_data = order
        udp_socket.sendto(send_data.encode('utf-8'), esp32_addr)
        recv_data, sender_info = udp_socket.recvfrom(1024)
        recv_data_str = recv_data.decode("utf-8")
        print("{} sent: {}".format(sender_info, recv_data_str))

    udp_socket.close()

