"""
Manim Scene Template with Narration Sync

This template demonstrates how to structure a Manim scene
that is synchronized with TTS narration.

Key principles:
1. Each narration has a measured duration
2. Animation time + wait time = narration duration
3. Keep elements within the safe area to avoid cut-off
"""

from manim import *

# Japanese font setting (macOS)
# config.font = "Hiragino Sans"
# Linux: config.font = "Noto Sans CJK JP"
# Windows: config.font = "Yu Gothic"


class NarratedScene(Scene):
    """
    Template for a scene synchronized with narration.

    Narration timing (example):
    1. [5.57s] Introduction text
    2. [4.03s] Explanation text
    3. [4.70s] More content
    """

    def construct(self):
        # ===== Section 1: Title =====
        # Narration 1: [5.57s] "Introduction text"

        title = Text("Title Here", font_size=48)
        subtitle = Text("Subtitle Here", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)

        # Animation: 1.5s + 1s = 2.5s
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=1)
        # Wait: 5.57 - 2.5 = 3.07s
        self.wait(3.07)

        # ===== Section 2: Main Content =====
        # Narration 2: [4.03s] "Explanation text"

        # Clear previous content
        self.play(FadeOut(title), FadeOut(subtitle), run_time=1)

        # Section header
        section = Text("Section Title", font_size=36, color=YELLOW)
        section.to_edge(UP)
        self.play(Write(section), run_time=1)

        # Create axes (with safe positioning)
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=7,  # Smaller to leave margins
            y_length=5,
            axis_config={"color": GRAY, "include_numbers": False},
        )
        axes.shift(UP * 0.3)  # Move up to leave room below

        self.play(Create(axes), run_time=1.5)
        # Wait: 4.03 - 1 - 1.5 = 1.53s
        self.wait(1.53)

        # ===== Section 3: Additional Content =====
        # Narration 3: [4.70s] "More content"

        # Text below axes (within safe area)
        explanation = Text("Explanation text here", font_size=24)
        explanation.next_to(axes, DOWN, buff=0.3)  # Small buffer

        self.play(Write(explanation), run_time=1)
        # Wait: 4.70 - 1 = 3.70s
        self.wait(3.70)

        # ===== Cleanup =====
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)

        # ===== Ending =====
        thanks = Text("Thank you!", font_size=44)
        self.play(Write(thanks), run_time=1)
        self.wait(2)
        self.play(FadeOut(thanks), run_time=0.5)


# Alternative: Simple scene without narration sync
class SimpleScene(Scene):
    """Basic scene template without narration timing."""

    def construct(self):
        # Title
        title = Text("Simple Scene", font_size=48)
        self.play(Write(title))
        self.wait()

        # Transform to new content
        new_text = Text("New Content", font_size=48)
        self.play(Transform(title, new_text))
        self.wait()

        # Fade out
        self.play(FadeOut(title))
