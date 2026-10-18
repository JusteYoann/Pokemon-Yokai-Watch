#!/usr/bin/env python3
"""Rebuild the integer mixer table from reviewed measured gains, no audio required."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
config=json.loads((ROOT/'data/yokai/mixer_calibration.json').read_text())
rows=sorted(config['tracks'],key=lambda r:r['song_id'])
assert len({r['song_id'] for r in rows})==len(rows)
assert all(64<=r['gain_q8']<=768 for r in rows)
text='/* Measured post-B13 mix calibration. Source: data/yokai/mixer_calibration.json. */\nstatic const u16 sYokaiSongGain[MUS_YOKAI_LAST + 1] = {\n    [0] = 256,\n'
text+=''.join(f"    [{r['constant']}] = {r['gain_q8']},\n" for r in rows)
text+='};\n';(ROOT/'src/data/yokai_mixer_gains.h').write_text(text)
