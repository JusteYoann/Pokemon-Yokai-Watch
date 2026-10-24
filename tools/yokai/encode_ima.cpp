// Private WaveData type2 payload encoder. Input is mono PCM16LE; no WAV header.
// Choose a per-block IMA index by measured squared error, then greedily choose
// the closest reconstructed sample. All 256-sample blocks reset independently.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <limits>
#include <vector>

static const int steps[89] = {
    7,8,9,10,11,12,13,14,16,17,19,21,23,25,28,31,34,37,41,45,50,55,
    60,66,73,80,88,97,107,118,130,143,157,173,190,209,230,253,279,
    307,337,371,408,449,494,544,598,658,724,796,876,963,1060,1166,
    1282,1411,1552,1707,1878,2066,2272,2499,2749,3024,3327,3660,
    4026,4428,4871,5358,5894,6484,7132,7845,8630,9493,10442,11487,
    12635,13899,15289,16818,18500,20350,22385,24623,27086,29794,32767
};
static const int indexDelta[8] = {-1,-1,-1,-1,2,4,6,8};

int main(int argc, char **argv)
{
    if (argc != 3) return 2;
    std::ifstream input(argv[1], std::ios::binary);
    std::vector<int16_t> pcm;
    char low, high;
    while (input.get(low)) {
        if (!input.get(high)) return 3;
        pcm.push_back(static_cast<int16_t>(static_cast<uint8_t>(low)
                                        | (static_cast<uint8_t>(high) << 8)));
    }
    if (pcm.empty()) return 3;
    std::ofstream output(argv[2], std::ios::binary);
    if (!output) return 4;
    int delta[89][16];
    for (int i = 0; i < 89; ++i) {
        for (int code = 0; code < 16; ++code) {
            int step = steps[i];
            int difference = (step >> 3)
                           + ((code & 1) ? step >> 2 : 0)
                           + ((code & 2) ? step >> 1 : 0)
                           + ((code & 4) ? step : 0);
            delta[i][code] = (code & 8) ? -difference : difference;
        }
    }
    for (size_t base = 0; base < pcm.size(); base += 256) {
        std::array<uint8_t, 255> bestCodes{}, codes{};
        double bestError = std::numeric_limits<double>::infinity();
        int bestIndex = 0;
        auto trial = [&](int initialIndex) {
            int predictor = pcm[base], index = initialIndex;
            double error = 0;
            for (int sample = 1; sample < 256; ++sample) {
                int target = pcm[std::min(base + sample, pcm.size() - 1)];
                int bestCode = 0, closest = 1000000;
                for (int code = 0; code < 16; ++code) {
                    int difference = std::abs(target - std::clamp(
                        predictor + delta[index][code], -32768, 32767));
                    if (difference < closest) {
                        closest = difference;
                        bestCode = code;
                    }
                }
                predictor = std::clamp(predictor + delta[index][bestCode], -32768, 32767);
                index = std::clamp(index + indexDelta[bestCode & 7], 0, 88);
                codes[sample - 1] = bestCode;
                error += static_cast<double>(target - predictor) * (target - predictor);
            }
            if (error < bestError) {
                bestError = error;
                bestIndex = initialIndex;
                bestCodes = codes;
            }
        };
        for (int index = 0; index <= 88; index += 4) trial(index);
        int center = bestIndex;
        for (int index = std::max(0, center - 3); index <= std::min(88, center + 3); ++index)
            trial(index);
        output.put(pcm[base] & 255);
        output.put((pcm[base] >> 8) & 255);
        output.put(bestIndex);
        for (int sample = 0; sample < 255; sample += 2)
            output.put(bestCodes[sample] | ((sample + 1 < 255 ? bestCodes[sample + 1] : 0) << 4));
    }
    return output ? 0 : 4;
}
