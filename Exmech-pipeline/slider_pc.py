
import socket

def start_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 8080))
    return udp_socket


def slider_control(order, op_printer_id):
    """
    Slider control
    Input: order
    in - slide in
    out - slide out
    op_printer_id: int 1, 2, 3
    """

    esp32_addr = ('192.168.3.9', 7777)
    udp_socket = start_udp()
    # Send command, format: "1in"
    send_order = str(op_printer_id) + order
    send_data = send_order
    udp_socket.sendto(send_data.encode('utf-8'), esp32_addr)
    recv_data, sender_info = udp_socket.recvfrom(1024)
    recv_data_str = recv_data.decode("utf-8")
    # Print the received information
    print("{} sent: {}".format(sender_info, recv_data_str))

    udp_socket.close()



