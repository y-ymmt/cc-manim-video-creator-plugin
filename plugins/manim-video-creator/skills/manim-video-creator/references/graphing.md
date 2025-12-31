# Manim Graphing Reference

## Table of Contents
1. [Axes](#axes)
2. [Number Line](#number-line)
3. [Plotting Functions](#plotting-functions)
4. [Areas and Regions](#areas-and-regions)
5. [Coordinate Systems](#coordinate-systems)
6. [Charts and Graphs](#charts-and-graphs)
7. [Vector Fields](#vector-fields)

---

## Axes

### Basic Axes
```python
axes = Axes(
    x_range=[-3, 3, 1],     # [min, max, step]
    y_range=[-2, 2, 0.5],
    x_length=10,
    y_length=6,
    axis_config={"include_numbers": True}
)
```

### Axis Configuration
```python
axes = Axes(
    x_range=[0, 10, 2],
    y_range=[0, 100, 20],
    x_axis_config={
        "numbers_to_include": [2, 4, 6, 8, 10],
        "include_tip": True
    },
    y_axis_config={
        "include_numbers": True
    },
    tips=True  # Arrow tips on axes
)
```

### Axis Labels
```python
axes = Axes(x_range=[-3, 3], y_range=[-2, 2])
labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
# or
labels = axes.get_axis_labels(
    x_label=MathTex("t"),
    y_label=MathTex("v(t)")
)
```

### Coordinate Conversion
```python
# Point on axes -> scene coordinates
point = axes.coords_to_point(2, 3)
# Shorthand:
point = axes @ (2, 3)

# Scene coordinates -> axes point
coords = axes.point_to_coords([1, 0, 0])
```

---

## Number Line

### Basic Number Line
```python
number_line = NumberLine(
    x_range=[-10, 10, 2],
    length=10,
    include_numbers=True
)
```

### Custom Number Line
```python
number_line = NumberLine(
    x_range=[0, 5, 0.5],
    length=12,
    include_numbers=True,
    numbers_to_include=[0, 1, 2, 3, 4, 5],
    decimal_number_config={"num_decimal_places": 1},
    include_tip=True
)
```

### Point on Number Line
```python
dot = Dot(number_line.n2p(3))  # Number to point
```

---

## Plotting Functions

### Basic Plot
```python
axes = Axes(x_range=[-3, 3], y_range=[-1, 1])
graph = axes.plot(lambda x: np.sin(x), color=BLUE)
```

### Plot with Range
```python
graph = axes.plot(
    lambda x: x**2,
    x_range=[-2, 2],
    color=GREEN
)
```

### Parametric Plot
```python
curve = axes.plot_parametric_curve(
    lambda t: np.array([np.cos(t), np.sin(t), 0]),
    t_range=[0, 2 * PI],
    color=YELLOW
)
```

### Implicit Function
```python
implicit = axes.plot_implicit_curve(
    lambda x, y: x**2 + y**2 - 1,  # Circle: x^2 + y^2 = 1
    color=RED
)
```

### FunctionGraph (Standalone)
```python
graph = FunctionGraph(
    lambda x: np.sin(x),
    x_range=[-PI, PI],
    color=BLUE
)
```

### ParametricFunction (Standalone)
```python
curve = ParametricFunction(
    lambda t: np.array([np.cos(t), np.sin(t), 0]),
    t_range=[0, 2 * PI]
)
```

---

## Areas and Regions

### Area Under Curve
```python
axes = Axes(x_range=[-1, 5], y_range=[-1, 5])
graph = axes.plot(lambda x: x**2 / 4)

area = axes.get_area(
    graph,
    x_range=[0, 4],
    color=BLUE,
    opacity=0.5
)
```

### Riemann Rectangles
```python
rects = axes.get_riemann_rectangles(
    graph,
    x_range=[0, 4],
    dx=0.5,
    stroke_width=0.5,
    stroke_color=WHITE,
    fill_opacity=0.7
)
```

### Area Between Curves
```python
graph1 = axes.plot(lambda x: x**2)
graph2 = axes.plot(lambda x: x)

area = axes.get_area(
    graph1,
    x_range=[0, 1],
    bounded_graph=graph2,
    color=YELLOW,
    opacity=0.5
)
```

### Vertical/Horizontal Lines
```python
v_line = axes.get_vertical_line(axes.i2gp(2, graph))
h_line = axes.get_horizontal_line(axes.i2gp(2, graph))

# Or
v_line = axes.get_v_line(point)
h_line = axes.get_h_line(point)
```

---

## Coordinate Systems

### NumberPlane
```python
plane = NumberPlane(
    x_range=[-7, 7, 1],
    y_range=[-4, 4, 1],
    background_line_style={
        "stroke_color": BLUE_D,
        "stroke_width": 2,
        "stroke_opacity": 0.5
    }
)
```

### ComplexPlane
```python
complex_plane = ComplexPlane(
    x_range=[-3, 3],
    y_range=[-3, 3]
)

# Plot complex numbers
dot = Dot(complex_plane.n2p(1 + 2j))
```

### PolarPlane
```python
polar = PolarPlane(
    radius_max=3,
    size=6
)

# Polar coordinates
polar.polar_to_point(r=2, theta=PI/4)
```

---

## Charts and Graphs

### Bar Chart
```python
chart = BarChart(
    values=[3, 5, 2, 4, 6],
    bar_names=["A", "B", "C", "D", "E"],
    y_range=[0, 8, 2],
    y_length=4,
    x_length=6,
    bar_colors=[RED, BLUE, GREEN, YELLOW, PURPLE]
)
```

### Animated Bar Chart
```python
chart = BarChart(values=[1, 2, 3, 4])
self.play(Create(chart))

# Change values
self.play(chart.animate.change_bar_values([4, 3, 2, 1]))
```

### Line Graph
```python
axes = Axes(x_range=[0, 5], y_range=[0, 10])
line_graph = axes.plot_line_graph(
    x_values=[0, 1, 2, 3, 4, 5],
    y_values=[1, 3, 2, 5, 4, 6],
    line_color=GOLD,
    vertex_dot_radius=0.05,
    stroke_width=4
)
```

---

## Vector Fields

### ArrowVectorField
```python
field = ArrowVectorField(
    lambda pos: np.array([pos[1], -pos[0], 0]),  # Circular field
    x_range=[-3, 3],
    y_range=[-3, 3]
)
```

### StreamLines
```python
stream = StreamLines(
    lambda pos: np.array([pos[1], -pos[0], 0]),
    x_range=[-3, 3, 0.3],
    y_range=[-3, 3, 0.3],
    stroke_width=3,
    max_anchors_per_line=30
)
self.play(stream.create())
```

### Animated Stream Lines
```python
stream = StreamLines(func, stroke_width=3)
self.add(stream)
stream.start_animation(warm_up=True, flow_speed=1.5)
self.wait(3)
```

---

## Graphs (Network/Tree)

### Graph
```python
graph = Graph(
    vertices=[1, 2, 3, 4, 5],
    edges=[(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3)],
    layout="circular"
)

# Layout options: "circular", "kamada_kawai", "planar",
# "random", "shell", "spectral", "spring", "tree"
```

### DiGraph (Directed)
```python
digraph = DiGraph(
    vertices=[1, 2, 3],
    edges=[(1, 2), (2, 3), (3, 1)],
    layout="circular",
    edge_type=Arrow
)
```

### Custom Layout
```python
graph = Graph(
    vertices=[1, 2, 3],
    edges=[(1, 2), (2, 3)],
    layout={1: LEFT, 2: ORIGIN, 3: RIGHT}
)
```

---

## Table

### Basic Table
```python
table = Table(
    [["A", "B", "C"],
     ["1", "2", "3"],
     ["X", "Y", "Z"]],
    include_outer_lines=True
)
```

### MathTable
```python
table = MathTable(
    [[r"x", r"x^2", r"x^3"],
     [r"1", r"1", r"1"],
     [r"2", r"4", r"8"]],
    include_outer_lines=True
)
```

### Styled Table
```python
table = Table(
    [["A", "B"], ["C", "D"]],
    row_labels=[Text("R1"), Text("R2")],
    col_labels=[Text("C1"), Text("C2")],
    top_left_entry=Text("X")
)
table.add_highlighted_cell((1, 1), color=GREEN)
```

---

## Matrix

### Matrix Display
```python
matrix = Matrix(
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
)

# Integer matrix
int_matrix = IntegerMatrix([[1, 0], [0, 1]])

# Decimal matrix
dec_matrix = DecimalMatrix([[1.5, 2.7], [3.14, 4.0]])
```

### Matrix Operations
```python
matrix = Matrix([[1, 2], [3, 4]])
brackets = matrix.get_brackets()
entries = matrix.get_entries()
entry = matrix.get_entries()[0]  # First entry
```
