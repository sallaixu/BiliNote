import sys
from faster_whisper import WhisperModel

input_path = sys.argv[1]

model = WhisperModel("medium", device="cuda")      # 有 GPU 就改成 "cuda"
segments, info = model.transcribe(input_path, language="zh")
for s in segments:
    print(f"[{s.start:.1f}s -> {s.end:.1f}s] {s.text}")