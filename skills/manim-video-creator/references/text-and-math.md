# Manim Text and Math Reference

## Table of Contents
1. [Text (Pango)](#text-pango)
2. [MarkupText](#markuptext)
3. [LaTeX (Tex/MathTex)](#latex-texmathtex)
4. [Code](#code)
5. [Numbers](#numbers)
6. [Common Patterns](#common-patterns)

---

## Text (Pango)

Basic text using Pango rendering (no LaTeX required).

### Basic Usage
```python
text = Text("Hello, World!")
text = Text("Hello", font_size=48)
text = Text("Colored", color=RED)
```

### Font Settings
```python
# Specify font (must be installed on system)
text = Text("Custom Font", font="Arial")
text = Text("Monospace", font="Courier New")

# List available fonts:
# import manimpango
# manimpango.list_fonts()
```

### Slant and Weight
```python
text = Text("Italic", slant=ITALIC)
text = Text("Bold", weight=BOLD)
# Weight options: NORMAL, BOLD, THIN, LIGHT, HEAVY, etc.
```

### Color by Character/Word
```python
# t2c: text to color mapping
text = Text("Hello World", t2c={"Hello": RED, "World": BLUE})

# By index
text = Text("Rainbow", t2c={"[0]": RED, "[1]": ORANGE, "[2]": YELLOW})

# By slice
text = Text("Highlight", t2c={"[2:5]": YELLOW})
```

### Gradient
```python
text = Text("Gradient", gradient=(RED, BLUE))
text = Text("Rainbow", gradient=(RED, ORANGE, YELLOW, GREEN, BLUE))

# t2g: partial gradient
text = Text("Partial", t2g={"art": (RED, BLUE)})
```

### Multi-language Support
```python
text = Text("Hello")
text = Text("Привет")  # Russian
text = Text("日本語")   # Japanese
text = Text("中文")     # Chinese
text = Text("العربية")  # Arabic
```

### Line Spacing
```python
multiline = Text("Line 1\nLine 2\nLine 3", line_spacing=1.5)
```

### Paragraph
```python
para = Paragraph(
    "First line",
    "Second line",
    "Third line",
    line_spacing=1.0,
    alignment="center"  # or "left", "right"
)
```

---

## MarkupText

HTML-like markup for rich text formatting.

```python
text = MarkupText('<b>Bold</b> and <i>Italic</i>')
text = MarkupText('<span foreground="red">Red</span>')
text = MarkupText('<u>Underlined</u>')
text = MarkupText('<s>Strikethrough</s>')
text = MarkupText('<span size="x-large">Large</span>')
text = MarkupText('<span font_family="serif">Serif</span>')

# Combined
text = MarkupText(
    '<span foreground="blue" font_family="monospace"><b>Bold Blue Mono</b></span>'
)
```

---

## LaTeX (Tex/MathTex)

### Tex (Mixed Text and Math)
```python
tex = Tex("Hello, $x^2 + y^2 = z^2$")
tex = Tex(r"The equation $E = mc^2$ is famous")
tex = Tex(r"\LaTeX{} is great!")
```

### MathTex (Pure Math Mode)
```python
# Everything is in math mode by default
eq = MathTex(r"x^2 + y^2 = z^2")
eq = MathTex(r"\int_0^1 x^2 \, dx = \frac{1}{3}")
eq = MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}")
```

### Color by Substring
```python
# Multiple arguments for easy coloring
eq = MathTex("x^2", "+", "y^2", "=", "z^2")
eq.set_color_by_tex("x", RED)
eq.set_color_by_tex("y", BLUE)

# Using {{ }} for automatic splitting
eq = MathTex(r"{{ a^2 }} + {{ b^2 }} = {{ c^2 }}")
eq[0].set_color(RED)  # a^2
eq[2].set_color(BLUE)  # b^2
```

### Isolate Substrings
```python
eq = MathTex(
    r"e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}",
    substrings_to_isolate=["x", "e"]
)
eq.set_color_by_tex("x", YELLOW)
```

### Custom LaTeX Packages
```python
from manim import TexTemplate

template = TexTemplate()
template.add_to_preamble(r"\usepackage{mathrsfs}")
template.add_to_preamble(r"\usepackage{amssymb}")

tex = MathTex(r"\mathscr{L}", tex_template=template)
```

### Font Templates
```python
from manim import TexFontTemplates

tex = Tex("Fancy Math", tex_template=TexFontTemplates.french_cursive)
# Available: american_typewriter, antykwa, apple_chancery,
# auriocus_kalligraphicus, baskervaldx, baskerville_it,
# comfortaa, comic_sans, french_cursive, ...
```

### Multi-line Equations
```python
# Using align* environment
eq = MathTex(r"""
    f(x) &= x^2 + 2x + 1 \\
         &= (x + 1)^2
""")
```

### BulletedList
```python
bullets = BulletedList(
    "First point",
    "Second point",
    "Third point",
    buff=0.5
)
```

### Title
```python
title = Title("My Presentation")
title = Title("Chapter 1", include_underline=True)
```

---

## Code

Display syntax-highlighted code.

```python
code = Code(
    "example.py",  # File path
    language="python",
    font="Monospace",
    background="window"  # or "rectangle"
)

# From string
code = Code(
    code="""
def hello():
    print("Hello, World!")
""",
    language="python"
)
```

### Parameters
- `file_name` or `code`: Source code
- `language`: Programming language
- `font`: Font family
- `font_size`: Size of text
- `background`: "window" or "rectangle"
- `insert_line_no`: Show line numbers

---

## Numbers

### DecimalNumber
```python
num = DecimalNumber(3.14159, num_decimal_places=2)
num = DecimalNumber(42, num_decimal_places=0)
```

### Integer
```python
num = Integer(42)
```

### Variable
Display variable with label.
```python
var = Variable(2, Text("x"), num_decimal_places=2)
# Shows: x = 2.00

# Update value
var.tracker.set_value(5)
```

### Animated Numbers
```python
tracker = ValueTracker(0)
num = DecimalNumber(0)
num.add_updater(lambda m: m.set_value(tracker.get_value()))

self.play(tracker.animate.set_value(100), run_time=3)
```

---

## Common Patterns

### Highlighting Equations
```python
eq = MathTex(r"E = mc^2")
box = SurroundingRectangle(eq, color=YELLOW)
self.play(Create(box))
```

### Equation Transformation
```python
eq1 = MathTex(r"x^2 - 1")
eq2 = MathTex(r"(x-1)(x+1)")
self.play(TransformMatchingTex(eq1, eq2))
```

### Split and Animate Parts
```python
eq = MathTex("a", "+", "b", "=", "c")
self.play(Write(eq[0]))      # Write "a"
self.play(Write(eq[1:3]))    # Write "+ b"
self.play(Write(eq[3:]))     # Write "= c"
```

### Debug: Show Indices
```python
eq = MathTex(r"a^2 + b^2 = c^2")
self.add(index_labels(eq))  # Show index of each part
```

### CJK Support (Chinese/Japanese/Korean)
```python
from manim import TexTemplateLibrary

# For Chinese
tex = Tex(
    r"中文内容",
    tex_template=TexTemplateLibrary.ctex
)

# For Japanese (requires appropriate LaTeX setup)
text = Text("日本語テキスト", font="Noto Sans JP")
```
