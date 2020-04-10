import socket
import json
import logging


class RoombaDiscoveryInfo:
    def __init__(self, robot_name, ip, mac, firmware):
        self.firmware = firmware
        self.mac = mac
        self.ip = ip
        self.robot_name = robot_name


class RoombaDiscovery:
    udp_bind_address = ''
    udp_address = '<broadcast>'
    udp_port = 5678
    broadcast_message = 'irobotmcs'
    server_socket = None
    log = None

    def __init__(self):
        self.server_socket = self._get_socket()
        self.log = logging.getLogger(__name__)

    def find(self):
        self._start_server()
        self.log.debug("Socket server started, port %s", self.udp_port)
        self._broadcast_message()
        self.log.debug("Broadcast message sent")
        return self._get_response()

    def _get_response(self):
        try:
            while True:
                raw_response, addr = self.server_socket.recvfrom(1024)
                self.log.debug("Received: response: %s, address: %s", raw_response, addr)
                data = raw_response.decode()
                if self._is_from_irobot(data):
                    return self._decode_data(data)
        except socket.timeout:
            return None

    def _is_from_irobot(self, data):
        if data == self.broadcast_message:
            return False

        json_response = json.loads(data)
        if 'Roomba' in json_response['hostname'] or 'iRobot' in json_response['hostname']:
            return True

        return False

    def _broadcast_message(self):
        self.server_socket.sendto(self.broadcast_message.encode(), (self.udp_address, self.udp_port))

    def _start_server(self):
        self.server_socket.bind((self.udp_bind_address, self.udp_port))

    @staticmethod
    def _decode_data(data):
        json_response = json.loads(data)
        return RoombaDiscoveryInfo(
            robot_name=json_response['robotname'],
            ip=json_response['ip'],
            mac=json_response['mac'],
            firmware=json_response['sw'])

    @staticmethod
    def _get_socket():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.settimeout(2)
        return server_socket
