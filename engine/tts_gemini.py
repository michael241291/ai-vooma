"""Gemini 3.1 Flash TTS narration for Tiny Chaos.

Reads the API key from the environment variable GEMINI_KEY (never write the key to the repo: it is public).
Usage (module): synth(text, out_wav, voice='Puck', style='...') -> duration in seconds (44.1 kHz mono wav)
Usage (CLI):    GEMINI_KEY=... python3 engine/tts_gemini.py lines.json out_dir
                lines.json = {"voice": "Puck", "style": "...", "lines": {"id": "text", ...}}
                writes out_dir/<id>.wav and out_dir/durations.json
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request

import numpy as np

MODEL = 'gemini-3.1-flash-tts-preview'
URL = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent'
SR_OUT = 44100


def synth(text, out_wav, voice='Puck', style=None, retries=6):
    key = os.environ['GEMINI_KEY']
    prompt = f'{style}: {text}' if style else text
    body = {'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'responseModalities': ['AUDIO'],
                                 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': voice}}}}}
    last = None
    for _ in range(retries):
        try:
            req = urllib.request.Request(URL, data=json.dumps(body).encode(), method='POST',
                                         headers={'x-goog-api-key': key, 'Content-Type': 'application/json',
                                                  'User-Agent': 'curl/8.5.0'})
            with urllib.request.urlopen(req, timeout=120) as r:
                res = json.load(r)
            part = res['candidates'][0]['content']['parts'][0]['inlineData']
            pcm = np.frombuffer(base64.b64decode(part['data']), dtype='<i2')
            rate = int(part['mimeType'].split('rate=')[1].split(';')[0])
            break
        except Exception as e:  # noqa: BLE001  (429 = rate limit on the free tier: wait and retry)
            last = e
            time.sleep(35)
    else:
        raise RuntimeError(f'TTS failed: {last}')
    raw = out_wav + '.raw'
    pcm.tofile(raw)
    # trim leading/trailing silence and resample to 44.1 kHz
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(rate), '-ac', '1', '-i', raw,
                    '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
                           'silenceremove=start_periods=1:start_threshold=-45dB,areverse',
                    '-ar', str(SR_OUT), out_wav], check=True)
    os.remove(raw)
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out_wav],
                         capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def synth_script(lines, out_dir, voice='Puck', style=None, min_gap=0.32):
    """One TTS request for a whole script (the free tier allows only ~10 requests/day).
    lines: ordered {id: text}. Writes out_dir/full.wav and one wav per line (split on the pauses),
    returns {id: duration}. Falls back to splitting by character count if the pauses do not match."""
    import re
    os.makedirs(out_dir, exist_ok=True)
    keys = list(lines)
    script = '\n\n'.join(lines[k] + ' [pause]' for k in keys)
    full = os.path.join(out_dir, 'full.wav')
    total = synth(script.replace(' [pause]', ' ...'), full, voice, style)
    det = subprocess.run(['ffmpeg', '-i', full, '-af', f'silencedetect=noise=-40dB:d={min_gap}', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', det)]
    ends = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', det)]
    gaps = sorted(zip(starts, ends), key=lambda g: g[1] - g[0], reverse=True)[:len(keys) - 1]
    gaps = sorted(gaps)
    if len(gaps) == len(keys) - 1:
        cuts = [0.0] + [(a + b) / 2 for a, b in gaps] + [total]
    else:
        n = [len(lines[k]) for k in keys]; acc = 0; cuts = [0.0]
        for c in n:
            acc += c; cuts.append(total * acc / sum(n))
    durs = {}
    for i, k in enumerate(keys):
        dst = os.path.join(out_dir, f'{k}.wav')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', full, '-ss', f'{cuts[i]:.3f}', '-to', f'{cuts[i + 1]:.3f}',
                        '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
                               'silenceremove=start_periods=1:start_threshold=-45dB,areverse', dst], check=True)
        durs[k] = round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                              'csv=p=0', dst], capture_output=True, text=True).stdout), 3)
    json.dump(durs, open(os.path.join(out_dir, 'durations.json'), 'w'), indent=1)
    return durs


if __name__ == '__main__':
    if '--one-request' in sys.argv:
        spec = json.load(open(sys.argv[1]))
        print(synth_script(spec['lines'], sys.argv[2], spec.get('voice', 'Puck'), spec.get('style')))
        sys.exit(0)
    spec = json.load(open(sys.argv[1]))
    out_dir = sys.argv[2]; os.makedirs(out_dir, exist_ok=True)
    durs = {}
    for k, text in spec['lines'].items():
        dst = os.path.join(out_dir, f'{k}.wav')
        if os.path.exists(dst):
            durs[k] = round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                                  'csv=p=0', dst], capture_output=True, text=True).stdout), 3)
            continue
        durs[k] = round(synth(text, os.path.join(out_dir, f'{k}.wav'), spec.get('voice', 'Puck'), spec.get('style')), 3)
        print(k, durs[k], text)
    json.dump(durs, open(os.path.join(out_dir, 'durations.json'), 'w'), indent=1)
