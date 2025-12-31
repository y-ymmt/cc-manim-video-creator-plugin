# Manim 3D Scenes Reference

## Table of Contents
1. [ThreeDScene Basics](#threedscene-basics)
2. [Camera Control](#camera-control)
3. [3D Objects](#3d-objects)
4. [3D Axes and Graphs](#3d-axes-and-graphs)
5. [Fixed Frame Mobjects](#fixed-frame-mobjects)
6. [Lighting](#lighting)

---

## ThreeDScene Basics

Use `ThreeDScene` instead of `Scene` for 3D content.

```python
from manim import *

class My3DScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Sphere(radius=1)
        self.add(axes, sphere)
        self.wait()
```

### Default Camera Position
```python
# Default orientation: phi=0, theta=-PI/2
# Looking straight at the xy-plane
```

---

## Camera Control

### Set Camera Orientation
```python
self.set_camera_orientation(
    phi=75 * DEGREES,    # Angle from z-axis (vertical tilt)
    theta=-45 * DEGREES,  # Angle around z-axis (horizontal rotation)
    gamma=0,              # Roll angle
    zoom=1                # Zoom level
)
```

### Animate Camera Movement
```python
self.move_camera(
    phi=60 * DEGREES,
    theta=30 * DEGREES,
    run_time=3
)
```

### Ambient Camera Rotation
```python
# Start continuous rotation
self.begin_ambient_camera_rotation(rate=0.1)

# ... do animations ...

# Stop rotation
self.stop_ambient_camera_rotation()
```

### 3D Illusion Rotation
```python
self.begin_3dillusion_camera_rotation(rate=0.1)
# ...
self.stop_3dillusion_camera_rotation()
```

### Default Angled View
```python
self.set_to_default_angled_camera_orientation()
```

---

## 3D Objects

### Sphere
```python
sphere = Sphere(radius=1)
sphere = Sphere(
    radius=2,
    resolution=(32, 32),  # (u_res, v_res)
    fill_opacity=0.8
)
```

### Cube
```python
cube = Cube(side_length=2)
cube = Cube(
    side_length=1,
    fill_color=BLUE,
    fill_opacity=0.7,
    stroke_width=2
)
```

### Prism
```python
prism = Prism(dimensions=[2, 1, 3])  # width, height, depth
```

### Cylinder
```python
cylinder = Cylinder(
    radius=1,
    height=2,
    direction=UP,
    resolution=(24, 1)
)
```

### Cone
```python
cone = Cone(
    base_radius=1,
    height=2,
    direction=UP
)
```

### Torus
```python
torus = Torus(
    major_radius=2,
    minor_radius=0.5
)
```

### Line3D / Arrow3D / Dot3D
```python
line = Line3D(start=ORIGIN, end=[2, 2, 2])
arrow = Arrow3D(start=ORIGIN, end=[1, 1, 1])
dot = Dot3D(point=[1, 1, 1], radius=0.1)
```

### Surface (Parametric)
```python
surface = Surface(
    lambda u, v: np.array([
        u,
        v,
        np.sin(u) * np.cos(v)
    ]),
    u_range=[-PI, PI],
    v_range=[-PI, PI],
    resolution=(32, 32)
)
surface.set_fill_by_checkerboard(BLUE, GREEN)
```

### Polyhedra
```python
tetra = Tetrahedron()
octa = Octahedron()
dodeca = Dodecahedron()
icosa = Icosahedron()

# Custom polyhedron
poly = Polyhedron(
    vertex_coords=[...],
    faces_list=[...]
)
```

---

## 3D Axes and Graphs

### ThreeDAxes
```python
axes = ThreeDAxes(
    x_range=[-6, 6, 1],
    y_range=[-6, 6, 1],
    z_range=[-4, 4, 1],
    x_length=12,
    y_length=12,
    z_length=8
)
```

### Plot 3D Function
```python
axes = ThreeDAxes()

# Parametric curve
curve = ParametricFunction(
    lambda t: np.array([
        np.cos(t),
        np.sin(t),
        t / 4
    ]),
    t_range=[0, 4 * PI]
)

# Surface
surface = axes.plot_surface(
    lambda u, v: u * np.sin(v),
    u_range=[-1, 1],
    v_range=[0, 2 * PI]
)
```

### Surface with Color Gradient
```python
surface = Surface(
    lambda u, v: np.array([u, v, np.sin(u + v)]),
    u_range=[-2, 2],
    v_range=[-2, 2]
)
surface.set_fill_by_value(
    axes=axes,
    colors=[(RED, -1), (YELLOW, 0), (GREEN, 1)]
)
```

---

## Fixed Frame Mobjects

Keep certain objects fixed (e.g., labels) while camera moves.

### Fixed in Frame
```python
# Object won't move with camera
label = Text("Fixed Label").to_corner(UL)
self.add_fixed_in_frame_mobjects(label)
self.add(label)

# Remove from fixed
self.remove_fixed_in_frame_mobjects(label)
```

### Fixed Orientation
```python
# Object faces camera but can move in 3D
label = Text("Always Facing")
self.add_fixed_orientation_mobjects(label)

# Remove
self.remove_fixed_orientation_mobjects(label)
```

---

## Lighting

### Basic Light Setup
```python
# ThreeDScene has default lighting
# Ambient light illuminates all surfaces equally
# Point lights create directional shadows
```

### Adjust Light Position
```python
class CustomLighting(ThreeDScene):
    def construct(self):
        self.camera.light_source.move_to([3, 3, 3])

        sphere = Sphere()
        self.add(sphere)
```

### Shading
```python
# Surfaces automatically get shading based on light position
# Adjust surface properties for different effects
surface.set_fill(color=BLUE, opacity=0.8)
surface.set_stroke(color=WHITE, width=0.5)
```

---

## Example: Complete 3D Scene

```python
class Example3D(ThreeDScene):
    def construct(self):
        # Setup
        axes = ThreeDAxes()

        # Camera position
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Create surface
        surface = Surface(
            lambda u, v: np.array([u, v, np.sin(u) * np.cos(v)]),
            u_range=[-PI, PI],
            v_range=[-PI, PI],
            resolution=(30, 30)
        )
        surface.set_fill_by_checkerboard(BLUE_D, BLUE_E, opacity=0.8)

        # Fixed label
        title = Text("3D Surface").to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # Animate
        self.add(axes)
        self.play(Create(surface), Write(title))

        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
```

---

## SpecialThreeDScene

Extended 3D scene with additional features.

```python
class MySpecialScene(SpecialThreeDScene):
    def construct(self):
        # Has additional helper methods
        # for common 3D operations
        pass
```
