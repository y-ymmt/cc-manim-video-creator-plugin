# Manim Animations Reference

## Table of Contents
1. [Creation Animations](#creation-animations)
2. [Fading Animations](#fading-animations)
3. [Transform Animations](#transform-animations)
4. [Movement Animations](#movement-animations)
5. [Indication Animations](#indication-animations)
6. [Animation Composition](#animation-composition)
7. [Updaters](#updaters)

---

## Creation Animations

### Create
Incrementally show a VMobject by drawing it.
```python
self.play(Create(circle))
self.play(Create(square, run_time=2))
```

### Write
Simulate handwriting effect for text/equations.
```python
self.play(Write(text))
self.play(Write(equation, run_time=3))
```

### Uncreate / Unwrite
Reverse of Create/Write.
```python
self.play(Uncreate(circle))
self.play(Unwrite(text))
```

### DrawBorderThenFill
Draw border first, then fill.
```python
self.play(DrawBorderThenFill(square))
```

### AddTextLetterByLetter / AddTextWordByWord
Typewriter-style text animation.
```python
self.play(AddTextLetterByLetter(text))
self.play(AddTextWordByWord(paragraph))
```

### TypeWithCursor / UntypeWithCursor
Type with visible cursor.
```python
self.play(TypeWithCursor(text, cursor="|"))
```

### SpiralIn
Objects spiral in from edges.
```python
self.play(SpiralIn(mobject))
```

### ShowIncreasingSubsets / ShowSubmobjectsOneByOne
Reveal submobjects progressively.
```python
self.play(ShowIncreasingSubsets(vgroup))
self.play(ShowSubmobjectsOneByOne(vgroup))
```

---

## Fading Animations

### FadeIn
```python
self.play(FadeIn(mobject))
self.play(FadeIn(mobject, shift=UP))      # Fade in from below
self.play(FadeIn(mobject, shift=DOWN))    # Fade in from above
self.play(FadeIn(mobject, scale=0.5))     # Grow while fading in
self.play(FadeIn(mobject, target_position=dot))  # Fade from position
```

### FadeOut
```python
self.play(FadeOut(mobject))
self.play(FadeOut(mobject, shift=UP))     # Fade out upward
self.play(FadeOut(mobject, scale=0.5))    # Shrink while fading
```

---

## Transform Animations

### Transform
Transform mobject into target (modifies original).
```python
self.play(Transform(circle, square))
# circle now looks like square, but is still the same object
```

### ReplacementTransform
Transform and replace in scene.
```python
self.play(ReplacementTransform(circle, square))
# circle is removed, square is added
```

### TransformFromCopy
Transform a copy, keeping original.
```python
self.play(TransformFromCopy(original, target))
```

### FadeTransform / FadeTransformPieces
Smooth fade between objects.
```python
self.play(FadeTransform(old_text, new_text))
```

### TransformMatchingShapes / TransformMatchingTex
Match similar parts between transforms.
```python
self.play(TransformMatchingTex(eq1, eq2))
self.play(TransformMatchingShapes(shape1, shape2))
```

### MoveToTarget
Use with `mobject.generate_target()`.
```python
mobject.generate_target()
mobject.target.shift(RIGHT * 2).scale(1.5)
self.play(MoveToTarget(mobject))
```

### ApplyMethod (deprecated, use .animate)
```python
# Old way:
self.play(ApplyMethod(circle.shift, UP))
# New way:
self.play(circle.animate.shift(UP))
```

### ApplyFunction
Apply arbitrary function to mobject.
```python
self.play(ApplyFunction(lambda m: m.scale(2).rotate(PI/4), mobject))
```

### ApplyMatrix
Apply transformation matrix.
```python
matrix = [[1, 1], [0, 1]]  # Shear matrix
self.play(ApplyMatrix(matrix, square))
```

### ApplyComplexFunction
Apply complex function to points.
```python
self.play(ApplyComplexFunction(lambda z: z**2, plane))
```

### ClockwiseTransform / CounterclockwiseTransform
Transform with rotation direction.
```python
self.play(ClockwiseTransform(a, b))
```

### CyclicReplace / Swap
Cycle or swap positions.
```python
self.play(CyclicReplace(a, b, c))  # a->b, b->c, c->a
self.play(Swap(a, b))
```

### ScaleInPlace / ShrinkToCenter
```python
self.play(ScaleInPlace(mobject, 2))
self.play(ShrinkToCenter(mobject))
```

### Restore
Restore to saved state.
```python
mobject.save_state()
# ... modify mobject ...
self.play(Restore(mobject))
```

---

## Movement Animations

### Rotate / Rotating
```python
self.play(Rotate(square, PI/2))
self.play(Rotate(square, PI, about_point=ORIGIN))
self.play(Rotating(square, radians=2*PI, run_time=3))
```

### MoveAlongPath
Move object along a path.
```python
path = Line(LEFT, RIGHT)
self.play(MoveAlongPath(dot, path))
```

### Homotopy / ComplexHomotopy
Continuous deformation.
```python
def homotopy(x, y, z, t):
    return [x + t, y + t*np.sin(x), z]
self.play(Homotopy(homotopy, mobject))
```

### PhaseFlow
Flow along vector field.
```python
self.play(PhaseFlow(lambda p: np.array([p[1], -p[0], 0]), mobject))
```

---

## Indication Animations

### Indicate
Briefly highlight an object.
```python
self.play(Indicate(equation))
self.play(Indicate(word, color=YELLOW))
```

### Circumscribe
Draw shape around object.
```python
self.play(Circumscribe(equation))
self.play(Circumscribe(text, Circle))  # Use circle instead of rectangle
```

### Flash
Flash effect at position.
```python
self.play(Flash(dot))
self.play(Flash(point, color=RED, line_length=0.5))
```

### FocusOn
Zoom focus effect.
```python
self.play(FocusOn(mobject))
```

### ShowPassingFlash
Flash travels along path.
```python
self.play(ShowPassingFlash(line))
```

### ApplyWave
Wave effect through mobject.
```python
self.play(ApplyWave(text))
```

### Wiggle
Wiggle back and forth.
```python
self.play(Wiggle(mobject))
```

### Blink
Blink effect.
```python
self.play(Blink(dot))
```

---

## Animation Composition

### AnimationGroup
Play animations together with timing control.
```python
self.play(AnimationGroup(
    Create(circle),
    Create(square),
    lag_ratio=0.5  # Start second at 50% of first
))
```

### LaggedStart
Staggered animation starts.
```python
self.play(LaggedStart(*[
    FadeIn(obj) for obj in objects
], lag_ratio=0.2))
```

### LaggedStartMap
Apply animation to each element with lag.
```python
self.play(LaggedStartMap(FadeIn, vgroup, lag_ratio=0.1))
```

### Succession
Play one after another.
```python
self.play(Succession(
    Create(circle),
    Transform(circle, square),
    FadeOut(circle)
))
```

---

## Updaters

### add_updater
Continuously update mobject.
```python
# Position updater
line.add_updater(lambda m: m.move_to(dot.get_center()))

# Time-based updater
mobject.add_updater(lambda m, dt: m.rotate(dt))
```

### UpdateFromFunc / UpdateFromAlphaFunc
Animation-based updates.
```python
self.play(UpdateFromFunc(
    mobject,
    lambda m: m.set_color(random_color())
))

self.play(UpdateFromAlphaFunc(
    mobject,
    lambda m, alpha: m.set_opacity(alpha)
))
```

### ValueTracker
Track and animate values.
```python
tracker = ValueTracker(0)
number.add_updater(lambda m: m.set_value(tracker.get_value()))
self.play(tracker.animate.set_value(10))
```

### always_redraw
Recreate mobject each frame.
```python
line = always_redraw(lambda: Line(dot1.get_center(), dot2.get_center()))
```

---

## Common Parameters

All animations support:
- `run_time` (float): Duration in seconds (default: 1)
- `rate_func`: Timing function (linear, smooth, there_and_back, etc.)
- `lag_ratio` (float): Delay between sub-animations

### Rate Functions
```python
from manim import *
# Built-in rate functions:
smooth           # Smooth acceleration/deceleration
linear           # Constant speed
rush_into        # Fast start
rush_from        # Fast end
there_and_back   # Go and return
wiggle           # Oscillate
double_smooth    # Extra smooth
```
