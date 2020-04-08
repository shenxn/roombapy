from roomba.discovery import RoombaDiscovery, RoombaDiscoveryInfo


class TestDiscovery:

    def test_discovery_with_wrong_msg(self):
        # given
        discovery = RoombaDiscovery()

        # when
        discovery.broadcast_message = 'test'
        response = discovery.find()

        # then
        assert not response
