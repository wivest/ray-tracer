# Ray Tracer

Ray tracer written in [**Taichi lang**](https://www.taichi-lang.org), **Python**. Customizable toy renderer using _BVH_ optimisation with must-have functionality. Example [scene](/examples/suzanne.glb) render:

![Example render](/examples/example.png)

## Features

The project supports following features:

-   recognizing _glTF_ files (export from **Blender** possible)
-   preview mode with movable camera
-   renderer settings (_samples, ray bounces_ etc.)
-   _diffuse, specular and emission colors_ of materials
-   _point/sun light_ sampling

## Getting started

### Prerequisites

**Taichi** requires **Python** to run. To clone the project [**git**](https://git-scm.com/downloads) is needed (skip if downloading archive). Ensure `python` and `git` are on `PATH`.

> [!IMPORTANT]  
> Not all Python versions work with Taichi. Which specific do are listed on [official website](https://docs.taichi-lang.org/docs/hello_world#prerequisites). To avoid further conflicts [release 3.10.11](https://www.python.org/downloads/release/python-31011/) is recommended.

### Repository

Clone the repository from _GitHub_ using your terminal of choice

```
git clone https://github.com/wivest/ray-tracer.git
```

Then navigate to the repository itself

```
cd ray-tracer
```

> [!TIP]  
> _Optional step. Recommended to avoid package versions conflicts._<br>
> To manage Python packages **virtual environment** can be created. More information can be found [here](https://docs.python.org/3/library/venv.html).

Also some third-party packages are needed. After installing Python run

```
pip install -r requirements.txt
```

You're now ready to run the project! To get CLI help type

```
python main.py -h
```

## Usage

### Scenes

First, you need scenes to display (_scenes under [`/examples`](/examples) are ready to use_). Those can be exported from **Blender** in _glTF_ format. Go to `File > Export > glTF 2.0` and choose desired location to export, it will be passed to main program later.

> [!IMPORTANT]  
> There are some necessary checkboxes in export settings! In `Include > Data` check `Cameras` and `Punctual lights`. In `Data > Lightning` choose Lightning Mode `Unitless`.

### Modes and camera controls

The simplest command to run is

```
python main.py examples/suzanne.glb
```

which opens scene in _Scene preview_ mode. In this mode you can move, rotate camera and switch between lenses (_gray preview_ and _render_). Camera controls at a glance:

-   move: `WASD` (horizontal), `EX` (vertical) + `Shift` if using global space
-   switch camera modes: `M`
-   switch cameras (if there are many): `Tab`

_Scene preview_ mode is, as the name says, only a preview. To render an image you need to lauch the project in _scene render_ mode

```
python main.py examples/suzanne.glb -r
```

The window appears where you can see the render process. It is safe to quit with an _unfinished_ render, it will still be saved.
