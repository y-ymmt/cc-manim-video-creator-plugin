"""
TTS Audio Generation Template for Manim Videos

Usage:
1. Update NARRATIONS list with (start_time, text) tuples
2. Adjust VIDEO_DURATION_MS to match your video length
3. Run: uv run python generate_audio.py
4. Combine with video: ffmpeg -i video.mp4 -i narration.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest output.mp4 -y
"""

import asyncio
import edge_tts
from pydub import AudioSegment
import os

# ============================================================
# CONFIGURATION - Modify these settings
# ============================================================

# Voice options:
# Japanese: "ja-JP-NanamiNeural" (female), "ja-JP-KeitaNeural" (male)
# English: "en-US-JennyNeural" (female), "en-US-GuyNeural" (male)
VOICE = "ja-JP-NanamiNeural"

# Speech rate: "-20%" (slower), "+0%" (normal), "+20%" (faster)
RATE = "+0%"

# Total video duration in milliseconds
VIDEO_DURATION_MS = 120 * 1000

# Narrations with start times (seconds) - synced to animation
# Format: (start_time_seconds, "narration text")
NARRATIONS = [
    (0.0, "最初のナレーションテキスト。"),
    (5.0, "2番目のナレーションテキスト。"),
    (10.0, "3番目のナレーションテキスト。"),
    # Add more narrations here...
]

# ============================================================
# IMPLEMENTATION - No need to modify below
# ============================================================


async def generate_audio_segment(text: str, output_path: str):
    """Generate audio file from text using edge-tts."""
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(output_path)


async def main():
    # Create output directory
    audio_dir = "audio_segments"
    os.makedirs(audio_dir, exist_ok=True)

    # Create silent audio track
    final_audio = AudioSegment.silent(duration=VIDEO_DURATION_MS)

    print("Generating audio segments...")

    for i, (start_time, text) in enumerate(NARRATIONS):
        segment_path = f"{audio_dir}/segment_{i:02d}.mp3"
        print(f"  [{i+1}/{len(NARRATIONS)}] {start_time:.1f}s: {text[:30]}...")

        # Generate audio
        await generate_audio_segment(text, segment_path)

        # Load segment
        segment = AudioSegment.from_mp3(segment_path)

        # Overlay at specified position
        start_ms = int(start_time * 1000)
        final_audio = final_audio.overlay(segment, position=start_ms)

    # Export final audio
    print("\nExporting final audio track...")
    output_path = "narration.mp3"
    final_audio.export(output_path, format="mp3")
    print(f"Audio file created: {output_path}")

    # Cleanup temporary files
    for i in range(len(NARRATIONS)):
        segment_path = f"{audio_dir}/segment_{i:02d}.mp3"
        if os.path.exists(segment_path):
            os.remove(segment_path)
    os.rmdir(audio_dir)

    print("\nNext step: Combine with video using:")
    print("  ffmpeg -i video.mp4 -i narration.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest output.mp4 -y")

    return output_path


if __name__ == "__main__":
    asyncio.run(main())
