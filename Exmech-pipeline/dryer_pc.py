import socket

def start_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 8080))
    return udp_socket

def dryer_control(order):
    """
    Dryer workstation control
    Input: order
    in - slide in
    out - slide out
    run - slide in - perform blowing - slide out
    """

    esp32_addr = ('192.168.3.12', 7777)
    udp_socket = start_udp()
    # Send command, format: "1in"
    send_order = order
    send_data = send_order
    udp_socket.sendto(send_data.encode('utf-8'), esp32_addr)
    recv_data, sender_info = udp_socket.recvfrom(1024)
    # Decode and convert to str
    recv_data_str = recv_data.decode("utf-8")
    # Print received information
    print("{} sent: {}".format(sender_info, recv_data_str))

    udp_socket.close()

if __name__ == "__main__":
    order = 'run'
    dryer_control(order)
