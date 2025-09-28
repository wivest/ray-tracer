# Ray Tracer

Ray tracer written in [**Taichi lang**](https://www.taichi-lang.org), **Python**. Customizable toy renderer using _BVH_ optimisation with must-have functionality. Example [scene](/examples/suzanne.glb) render:

![Example render](/examples/example.png)

## Features

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
