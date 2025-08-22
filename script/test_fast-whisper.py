import sys
from pathlib import Path
from faster_whisper import WhisperModel

def main(audio_path: str) -> None:
    if not Path(audio_path).exists():
        print(f"文件不存在：{audio_path}", file=sys.stderr)
        sys.exit(1)

    try:
        model = WhisperModel("base", device="cpu")
        segments, info = model.transcribe(audio_path,task="transcribe",vad_filter=True,vad_parameters=dict(
        min_silence_duration_ms=1000,   # 静音≥500ms 才切分
        # threshold=0.5                # 置信阈值，默认即可
    ))
        for seg in segments:
            print(f"[{seg.start:.1f}s -> {seg.end:.1f}s] {seg.text}", flush=True)
    except Exception as e:
        print(f"转写出错：{e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python transcribe.py <音频文件>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])