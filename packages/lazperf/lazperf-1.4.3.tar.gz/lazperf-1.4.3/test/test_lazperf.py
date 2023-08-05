import json
import struct
import unittest

import numpy as np
from lazperf import Decompressor, Compressor, buildNumpyDescription

schema = [{u'type': u'floating', u'name': u'X', u'size': 8}, {u'type': u'floating', u'name': u'Y', u'size': 8},
          {u'type': u'floating', u'name': u'Z', u'size': 8}, {u'type': u'unsigned', u'name': u'Origin', u'size': 8},
          {u'type': u'unsigned', u'name': u'Intensity', u'size': 2},
          {u'type': u'unsigned', u'name': u'ReturnNumber', u'size': 1},
          {u'type': u'unsigned', u'name': u'NumberOfReturns', u'size': 1},
          {u'type': u'unsigned', u'name': u'ScanDirectionFlag', u'size': 1},
          {u'type': u'unsigned', u'name': u'EdgeOfFlightLine', u'size': 1},
          {u'type': u'unsigned', u'name': u'Classification', u'size': 1},
          {u'type': u'floating', u'name': u'ScanAngleRank', u'size': 4},
          {u'type': u'unsigned', u'name': u'UserData', u'size': 1},
          {u'type': u'unsigned', u'name': u'PointSourceId', u'size': 2},
          {u'type': u'floating', u'name': u'GpsTime', u'size': 8}]

len_compressed = 25691
len_uncompressed = 54112
expected_point_count = 1002


class TestLazPerf(unittest.TestCase):

    def test_decompressor(self):
        s = json.dumps(schema)

        with open('test/compressed.bin', 'rb') as f:
            data = f.read()

        with open('test/uncompressed.bin', 'rb') as f:
            original = f.read()

        self.assertEqual(len(data),
                         len_compressed,
                         "compressed file length is correct")
        self.assertEqual(len(original),
                         len_uncompressed,
                         "uncompressed file length is correct")

        # last four bytes are the point count
        compressed_point_count = struct.unpack('<L', data[-4:])[0]
        uncompressed_point_count = struct.unpack('<L', original[-4:])[0]

        self.assertEqual(compressed_point_count,
                         uncompressed_point_count,
                         "compressed point count matches expected")
        self.assertEqual(uncompressed_point_count,
                         expected_point_count,
                         "uncompressed point count matches expected")

        arr = np.frombuffer(data, dtype=np.uint8)
        dtype = buildNumpyDescription(json.loads(s))
        self.assertEqual(dtype.itemsize, 54)

        d = Decompressor(arr, s)
        decompressed = d.decompress(compressed_point_count)
        uncompressed = np.frombuffer(original[0:-4], dtype=dtype)

        self.assertEqual(uncompressed.shape[0], expected_point_count)
        self.assertEqual(decompressed.shape[0], expected_point_count)
        for i in range(len(uncompressed)):
            self.assertEqual(uncompressed[i], decompressed[i])

    def test_compressor(self):
        s = json.dumps(schema)

        with open('test/compressed.bin', 'rb') as f:
            data = f.read()

        with open('test/uncompressed.bin', 'rb') as f:
            original = f.read()

        self.assertEqual(len(data),
                         len_compressed,
                         "compressed file length is correct")
        self.assertEqual(len(original),
                         len_uncompressed,
                         "uncompressed file length is correct")

        # last four bytes are the point count
        compressed_point_count = struct.unpack('<L', data[-4:])[0]
        uncompressed_point_count = struct.unpack('<L', original[-4:])[0]

        self.assertEqual(compressed_point_count,
                         uncompressed_point_count,
                         "compressed point count matches expected")
        self.assertEqual(uncompressed_point_count,
                         expected_point_count,
                         "uncompressed point count matches expected")

        dtype = buildNumpyDescription(json.loads(s))

        uncompressed = np.frombuffer(original[0:-4], dtype=dtype)
        self.assertEqual(uncompressed.shape[0], expected_point_count)

        point_data = np.frombuffer(original[:-4], dtype=dtype)

        c = Compressor(s)

        compressed = c.compress(point_data)
        original_compressed = np.frombuffer(data[0:-4], dtype=np.uint8)

        self.assertEqual(len(original_compressed), len_compressed - 4)
        for i in range(len(compressed)):
            self.assertEqual(compressed[i], original_compressed[i])

    def test_full_loop(self):
        s = json.dumps(schema)

        with open('test/uncompressed.bin', 'rb') as f:
            original = f.read()

        dtype = buildNumpyDescription(json.loads(s))
        uncompressed = np.frombuffer(original[0:-4], dtype=dtype)

        c = Compressor(s)
        compressed = c.compress(uncompressed)

        d = Decompressor(compressed, s)
        decompressed = d.decompress(expected_point_count)
        self.assertEqual(len(decompressed), len(uncompressed))
        for i in range(len(decompressed)):
            self.assertEqual(decompressed[i], uncompressed[i])

        # confirm we can build from dtypes instead of json descriptions
        _ = Compressor(dtype)
        _ = Decompressor(compressed, dtype)


if __name__ == '__main__':
    unittest.main()
