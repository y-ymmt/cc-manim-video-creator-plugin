# Manim Mobjects Reference

## Table of Contents
1. [Basic Shapes](#basic-shapes)
2. [Lines and Arrows](#lines-and-arrows)
3. [Polygons](#polygons)
4. [Arcs and Circles](#arcs-and-circles)
5. [3D Objects](#3d-objects)
6. [Grouping](#grouping)
7. [Positioning Methods](#positioning-methods)
8. [Styling Methods](#styling-methods)

---

## Basic Shapes

### Dot
```python
dot = Dot()
dot = Dot(point=RIGHT, radius=0.1, color=RED)
```

### Square
```python
square = Square()
square = Square(side_length=2, color=BLUE, fill_opacity=0.5)
```

### Rectangle
```python
rect = Rectangle(width=4, height=2)
rect = Rectangle(width=4, height=2, color=GREEN, fill_opacity=0.8)
```

### RoundedRectangle
```python
rrect = RoundedRectangle(corner_radius=0.5, width=4, height=2)
```

### Circle
```python
circle = Circle()
circle = Circle(radius=2, color=RED)
circle.set_fill(BLUE, opacity=0.5)

# From three points
circle = Circle.from_three_points(p1, p2, p3)

# Surround another object
circle = Circle().surround(mobject, buffer_factor=1.2)
```

### Ellipse
```python
ellipse = Ellipse(width=4, height=2)
```

---

## Lines and Arrows

### Line
```python
line = Line(start=LEFT, end=RIGHT)
line = Line(ORIGIN, UP * 2, color=YELLOW)
```

### DashedLine
```python
dashed = DashedLine(LEFT, RIGHT, dash_length=0.2)
```

### Arrow
```python
arrow = Arrow(start=LEFT, end=RIGHT)
arrow = Arrow(LEFT, RIGHT, buff=0.1, stroke_width=5)
arrow = Arrow(LEFT, RIGHT, tip_shape=ArrowCircleFilledTip)
```

### DoubleArrow
```python
double_arrow = DoubleArrow(LEFT, RIGHT)
```

### Vector
```python
vector = Vector(direction=UP)
vector = Vector([1, 2, 0])
```

### CurvedArrow / CurvedDoubleArrow
```python
curved = CurvedArrow(LEFT, RIGHT, angle=TAU/4)
```

### TangentLine
```python
tangent = TangentLine(curve, alpha=0.5)  # Tangent at midpoint
```

---

## Polygons

### Polygon
```python
polygon = Polygon(LEFT, UP, RIGHT)  # Triangle
polygon = Polygon(*vertices, color=GREEN)
```

### Triangle
```python
triangle = Triangle()
```

### RegularPolygon
```python
pentagon = RegularPolygon(n=5)
hexagon = RegularPolygon(n=6, color=PURPLE)
```

### Star
```python
star = Star()
star = Star(n=5, outer_radius=2, inner_radius=1)
```

### Angle / RightAngle
```python
angle = Angle(line1, line2)
right_angle = RightAngle(line1, line2, length=0.4)
```

---

## Arcs and Circles

### Arc
```python
arc = Arc(radius=1, start_angle=0, angle=PI/2)
arc = Arc(radius=2, start_angle=0, angle=TAU, color=RED)
```

### ArcBetweenPoints
```python
arc = ArcBetweenPoints(LEFT, RIGHT, angle=PI/2)
```

### Annulus
```python
annulus = Annulus(inner_radius=1, outer_radius=2)
```

### Sector
```python
sector = Sector(outer_radius=2, inner_radius=1, angle=PI/3)
```

### AnnularSector
```python
sector = AnnularSector(inner_radius=1, outer_radius=2, angle=PI/2)
```

---

## 3D Objects

### Sphere
```python
sphere = Sphere(radius=1)
sphere = Sphere(radius=2, resolution=(32, 32))
```

### Cube
```python
cube = Cube(side_length=2)
cube = Cube(side_length=1, fill_opacity=0.7)
```

### Prism
```python
prism = Prism(dimensions=[1, 2, 3])
```

### Cylinder
```python
cylinder = Cylinder(radius=1, height=2)
```

### Cone
```python
cone = Cone(base_radius=1, height=2)
```

### Torus
```python
torus = Torus(major_radius=2, minor_radius=0.5)
```

### Arrow3D / Line3D / Dot3D
```python
arrow3d = Arrow3D(start=ORIGIN, end=[1, 1, 1])
line3d = Line3D(start=ORIGIN, end=[1, 1, 1])
dot3d = Dot3D(point=[1, 1, 1])
```

### Surface
```python
surface = Surface(
    lambda u, v: np.array([u, v, np.sin(u) * np.cos(v)]),
    u_range=[-PI, PI],
    v_range=[-PI, PI]
)
```

### Polyhedra
```python
tetra = Tetrahedron()
octa = Octahedron()
dodeca = Dodecahedron()
icosa = Icosahedron()
```

---

## Grouping

### VGroup
Group VMobjects together.
```python
group = VGroup(circle, square, triangle)
group = VGroup(*[Circle() for _ in range(5)])

# Arrange in row/column
group.arrange(RIGHT, buff=0.5)
group.arrange(DOWN, buff=0.3)

# Arrange in grid
group.arrange_in_grid(rows=2, cols=3, buff=0.5)

# Access elements
group[0]  # First element
group[-1]  # Last element
```

### Group
Group any Mobjects (including non-VMobjects).
```python
group = Group(image, shape)
```

### VDict
Dictionary-like access to VMobjects.
```python
vdict = VDict({"circle": Circle(), "square": Square()})
vdict["circle"]  # Access by key
```

---

## Positioning Methods

### Basic Movement
```python
mobject.shift(RIGHT * 2)
mobject.move_to(ORIGIN)
mobject.move_to([1, 2, 0])
```

### Relative Positioning
```python
mobject.next_to(other, RIGHT)
mobject.next_to(other, UP, buff=0.5)
mobject.next_to(other, DOWN + LEFT)
```

### Alignment
```python
mobject.align_to(other, UP)     # Align top edges
mobject.align_to(other, LEFT)   # Align left edges
mobject.align_to(other, UR)     # Align to upper-right corner
```

### Centering
```python
mobject.center()
mobject.to_edge(LEFT)
mobject.to_edge(UP, buff=0.5)
mobject.to_corner(UL)
```

### Get Positions
```python
mobject.get_center()
mobject.get_top()
mobject.get_bottom()
mobject.get_left()
mobject.get_right()
mobject.get_corner(UR)
mobject.get_edge_center(UP)
```

---

## Styling Methods

### Color
```python
mobject.set_color(RED)
mobject.set_color(color=[RED, BLUE])  # Gradient

# Named colors: RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK,
# TEAL, GOLD, MAROON, WHITE, BLACK, GREY/GRAY, etc.
```

### Stroke (Border)
```python
mobject.set_stroke(color=WHITE, width=4, opacity=1)
```

### Fill
```python
mobject.set_fill(color=BLUE, opacity=0.5)
```

### Opacity
```python
mobject.set_opacity(0.5)  # Both stroke and fill
mobject.set_fill_opacity(0.5)
mobject.set_stroke_opacity(0.8)
```

### Scale
```python
mobject.scale(2)           # Double size
mobject.scale(0.5)         # Half size
mobject.scale_to_fit_width(4)
mobject.scale_to_fit_height(3)
mobject.stretch_to_fit_width(4)
mobject.stretch_to_fit_height(3)
```

### Rotation
```python
mobject.rotate(PI/4)
mobject.rotate(PI/2, about_point=ORIGIN)
mobject.rotate(PI, axis=UP)  # 3D rotation
```

### Z-index
```python
mobject.set_z_index(1)  # Higher = in front
```

---

## Special Mobjects

### Brace / BraceLabel
```python
brace = Brace(mobject, direction=DOWN)
brace_label = BraceLabel(mobject, "label", brace_direction=DOWN)
```

### SurroundingRectangle
```python
rect = SurroundingRectangle(mobject, buff=0.1, color=YELLOW)
```

### BackgroundRectangle
```python
bg = BackgroundRectangle(text, fill_opacity=0.8)
```

### Cross
```python
cross = Cross(mobject, stroke_width=5)
```

### Underline
```python
underline = Underline(text)
```
