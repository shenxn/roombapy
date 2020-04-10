import sys
from roomba.discovery import RoombaDiscovery
from roomba.getpassword import RoombaPassword


def discovery():
    print(_get_roomba_info())


def password():
    roomba_info = _get_roomba_info()
    _wait_for_input()
    roomba_password = _get_roomba_password(roomba_info)
    roomba_info.password = roomba_password
    print(roomba_info)


def _get_roomba_password(roomba_info):
    roomba_password = RoombaPassword(roomba_info.ip)
    return roomba_password.get_password()


def _wait_for_input():
    print('Roomba have to be on Home Base powered on.\n'
          'Press and hold HOME button until you hear series of tones.\n'
          'Release button, Wi-Fi LED should be flashing')
    input('Press Enter to continue...')


def _get_roomba_info():
    roomba_discovery = RoombaDiscovery()
    if len(sys.argv) == 1:
        return roomba_discovery.find()
    roomba_ip = str(sys.argv[1])
    return roomba_discovery.get_info(roomba_ip)
