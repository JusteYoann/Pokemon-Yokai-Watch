#!/usr/bin/env python3
"""Host reference for private m4a WaveData type 2 (not a standard WAV container).

131-byte independently seekable blocks: LE16 predictor, IMA step index,
255 low-first IMA nibbles. Header/rate/length/loop semantics remain native m4a.
No copyrighted audio is included here.
"""
import struct

STEPS = (7,8,9,10,11,12,13,14,16,17,19,21,23,25,28,31,34,37,41,45,50,55,
         60,66,73,80,88,97,107,118,130,143,157,173,190,209,230,253,279,
         307,337,371,408,449,494,544,598,658,724,796,876,963,1060,1166,
         1282,1411,1552,1707,1878,2066,2272,2499,2749,3024,3327,3660,
         4026,4428,4871,5358,5894,6484,7132,7845,8630,9493,10442,11487,
         12635,13899,15289,16818,18500,20350,22385,24623,27086,29794,32767)
INDEX_DELTA = (-1,-1,-1,-1,2,4,6,8)


def decode(data, count):
    """Return signed PCM8 values, matching the native decoder's rounding."""
    assert len(data) == ((count + 255) // 256) * 131
    output = []
    for offset in range(0, len(data), 131):
        predictor, index = struct.unpack_from('<hB', data, offset)
        assert index <= 88
        output.append(min(127, (predictor + 128) >> 8))
        for i in range(1, 256):
            byte = data[offset + 3 + ((i - 1) >> 1)]
            code = (byte & 15) if i & 1 else byte >> 4
            step = STEPS[index]
            difference = (step >> 3) + ((step >> 2) if code & 1 else 0)
            difference += (step >> 1) if code & 2 else 0
            difference += step if code & 4 else 0
            predictor += -difference if code & 8 else difference
            predictor = max(-32768, min(32767, predictor))
            index = max(0, min(88, index + INDEX_DELTA[code & 7]))
            output.append(min(127, (predictor + 128) >> 8))
    return output[:count]
