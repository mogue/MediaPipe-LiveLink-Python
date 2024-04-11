import struct
import numpy as np

class LiveLinkPacket:
    
    VERSION = 6

    PACKET_MIN_SIZE = 264
    PACKET_MAX_SIZE = 774

    def __init__(self):
        self.data = b''
        self.data_count = 61
        self.size = 0

        self.version = LiveLinkPacket.VERSION
        self.device_id    = 'WebCam'
        self.subject_name = 'BasicRole'
        self.frame_time   = {"frame_number":0, "sub_frame":0, "numerator":0, "denominator":0}
        self.np_data      = np.zeros(shape=[self.data_count], dtype='>f')

        self._premade_header = b''
        self._premade_timer  = b''

    def _serialize_header(self):
        self._premade_header = b''
        self._premade_header += struct.pack('>B', self.version) # uint8

        string_bytes = self.device_id.encode('utf8')
        string_bytes_length = len(string_bytes)
        self._premade_header += struct.pack('>l', string_bytes_length) # int32
        self._premade_header += struct.pack(f'>{string_bytes_length}s', string_bytes) # string

        string_bytes = self.subject_name.encode('utf8')
        string_bytes_length = len(string_bytes)
        self._premade_header += struct.pack('>l', string_bytes_length) # int32
        self._premade_header += struct.pack(f'>{string_bytes_length}s', string_bytes) # string

    def _serialize_timer(self):
        self._premade_timer  = b''
        value = self.frame_time
        self._premade_timer += struct.pack('>l', value['frame_number']) # int32
        self._premade_timer += struct.pack('>f', value['sub_frame']) # float
        self._premade_timer += struct.pack('>l', value['numerator']) # int32
        self._premade_timer += struct.pack('>l', value['denominator']) # int32

        self._premade_timer += struct.pack('>B', self.data_count) #uint8

    def _serialize(self):
        self.data = b''
        self.data += self._premade_header
        self.data += self._premade_timer
        self.data += self.np_data.tobytes()