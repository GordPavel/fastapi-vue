import base64
import io
import os

import matplotlib.pyplot as plt
import numpy as np
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{os.environ['PUBLIC_HOST']}:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/solve")
async def solve_equation(request: Request, a: float = 0, b: float = 0, c: float = 0):
    solved_roots = np.roots([a, b, c])
    solved_roots = np.round(np.unique(solved_roots[np.isreal(solved_roots)]), decimals=5)
    return {
        "roots": solved_roots.tolist(),
    }


def get_plot_encoded(a: float = 0, b: float = 0, c: float = 0):
    solved_roots = np.roots([a, b, c])
    roots = list(np.sort(np.unique(solved_roots[abs(np.imag(solved_roots)) < 1e-5].real)))

    if len(roots) == 2:
        left_root, right_root = roots
        window = right_root - left_root
        left_window, right_window = left_root - window * .1, right_root + window * .1
    elif len(roots) == 1:
        left_root = right_root = roots[0]
        if a == 0:
            left_window, right_window = left_root - 2, right_root + 2
        else:
            left_window, right_window = np.roots([a, b, c - 2 if a > 0 else c + 2]).tolist()
    else:
        if b != 0:
            center_of_parabola_y = c - b ** 2 / (4 * a)
            center_of_parabola_x = np.unique(np.roots([a, b, c - center_of_parabola_y]).real)[0]
            left_window, right_window = center_of_parabola_x - 2, center_of_parabola_x + 2
        else:
            left_window, right_window = -5, 5
    x = np.linspace(left_window, right_window)
    y = a * np.power(x, 2) + b * x + c

    fig = plt.figure()
    for root in roots:
        plt.axvline(x=root, color='red', linestyle='--')
    plt.plot(x, np.zeros(len(x)), color='black')
    plt.plot(x, y)
    plt.scatter(roots, np.zeros(len(roots)), color='red', linestyle='--')

    png = io.BytesIO()
    fig.savefig(png)
    plot_base64 = base64.b64encode(png.getvalue()).decode('ascii')
    return plot_base64


@app.get("/get_plot")
async def get_plot(request: Request, a: float = 0, b: float = 0, c: float = 0):
    plot_base64 = get_plot_encoded(a, b, c)
    if plot_base64:
        return {
            'plot': plot_base64,
            'success': True
        }
    else:
        return {
            'success': False
        }
