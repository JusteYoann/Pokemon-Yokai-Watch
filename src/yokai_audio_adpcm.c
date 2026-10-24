#include "global.h"
#include "gba/m4a_internal.h"

// Archived experiment; the delivered mixer uses the reference SDK decoder.
#ifdef YOKAI_EXPERIMENTAL_IMA

/* Private WaveData type 2: 256 samples / 131 bytes. Each independently seekable
 * block holds a signed LE16 predictor, an IMA index, then 255 low-first nibbles.
 * The last unused high nibble is zero. Native PCM/DPCM and their cache are intact.
 * 131 bytes replace 132 bytes of SDK DPCM, without changing rates or loop points.
 */
struct YokaiImaCache
{
    const struct WaveData *wave;
    u32 block;
    s8 samples[256];
};

struct YokaiImaCache gYokaiImaCache;

static const s16 sSteps[89] = {
    7,8,9,10,11,12,13,14,16,17,19,21,23,25,28,31,34,37,41,45,50,55,
    60,66,73,80,88,97,107,118,130,143,157,173,190,209,230,253,279,
    307,337,371,408,449,494,544,598,658,724,796,876,963,1060,1166,
    1282,1411,1552,1707,1878,2066,2272,2499,2749,3024,3327,3660,
    4026,4428,4871,5358,5894,6484,7132,7845,8630,9493,10442,11487,
    12635,13899,15289,16818,18500,20350,22385,24623,27086,29794,32767
};
static const s8 sIndexDelta[8] = {-1,-1,-1,-1,2,4,6,8};

static s8 OutputSample(s32 predictor)
{
    s32 value = (predictor + 128) >> 8;
    if (value > 127) value = 127;
    return value;
}

s32 YokaiImaDecodeSample(const struct WaveData *wave, u32 sample)
{
    u32 block = sample >> 8;
    const u8 *data = (const u8 *)wave->data + block * 131;
    s32 predictor = (s16)(data[0] | (data[1] << 8));
    s32 index = data[2];
    u32 i;

    if (index > 88) index = 88;
    gYokaiImaCache.samples[0] = OutputSample(predictor);
    for (i = 1; i < 256; i++)
    {
        u32 code = data[3 + ((i - 1) >> 1)];
        s32 step = sSteps[index];
        s32 difference = step >> 3;
        code = (i & 1) ? (code & 15) : (code >> 4);
        if (code & 1) difference += step >> 2;
        if (code & 2) difference += step >> 1;
        if (code & 4) difference += step;
        predictor += (code & 8) ? -difference : difference;
        if (predictor > 32767) predictor = 32767;
        if (predictor < -32768) predictor = -32768;
        index += sIndexDelta[code & 7];
        if (index < 0) index = 0;
        if (index > 88) index = 88;
        gYokaiImaCache.samples[i] = OutputSample(predictor);
    }
    gYokaiImaCache.wave = wave;
    gYokaiImaCache.block = block;
    return gYokaiImaCache.samples[sample & 255];
}

#endif // YOKAI_EXPERIMENTAL_IMA
