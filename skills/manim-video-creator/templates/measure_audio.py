"""
Audio Duration Measurement Template

Use this script to measure the duration of each narration segment
before creating the Manim animation. This helps sync animations with narration.

Usage:
1. Update NARRATIONS list with your narration texts
2. Run: uv run python measure_audio.py
3. Use the measured durations to set wait() times in your Manim script
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

# Narration texts to measure
NARRATIONS = [
    "最初のナレーションテキスト。",
    "2番目のナレーションテキスト。",
    "3番目のナレーションテキスト。",
    # Add more narrations here...
]

# ============================================================
# IMPLEMENTATION - No need to modify below
# ============================================================


async def measure_duration(text: str, index: int) -> float:
    """Measure the duration of a text when spoken."""
    temp_path = f"temp_{index}.mp3"
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(temp_path)

    audio = AudioSegment.from_mp3(temp_path)
    duration = len(audio) / 1000.0  # Convert ms to seconds

    os.remove(temp_path)
    return duration


async def main():
    print(f"Measuring narration durations (Voice: {VOICE}, Rate: {RATE})")
    print("=" * 60)

    total = 0
    results = []

    for i, text in enumerate(NARRATIONS):
        duration = await measure_duration(text, i)
        total += duration
        results.append((i + 1, duration, text))
        print(f"{i+1:2d}. [{duration:5.2f}s] {text}")

    print("=" * 60)
    print(f"Total duration: {total:.2f}s ({total/60:.1f} min)")

    # Output in format ready for generate_audio.py
    print("\n" + "=" * 60)
    print("Copy this to generate_audio.py NARRATIONS list:")
    print("=" * 60)

    cumulative = 0.0
    for i, (num, duration, text) in enumerate(results):
        print(f'    ({cumulative:.2f}, "{text}"),')
        cumulative += duration


if __name__ == "__main__":
    asyncio.run(main())
