import base64
import io

import matplotlib.pyplot as plt
import numpy as np
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
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
    roots = np.sort(solved_roots[np.isreal(solved_roots)]).tolist()
    if len(roots) == 2:
        left_root, right_root = np.sort(solved_roots[np.isreal(solved_roots)]).tolist()
        window = right_root - left_root
        if window != 0:
            x = np.linspace(left_root - window * .1, right_root + window * .1, 200)
        else:
            window_roots = np.roots([a, b, c - 2 if a > 0 else c + 2])
            left_window, right_window = np.sort(window_roots[np.isreal(window_roots)]).tolist()
            x = np.linspace(left_window, right_window)
        y = a * np.power(x, 2) + b * x + c

        fig = plt.figure()

        plt.axvline(x=left_root, color='red', linestyle='--')
        plt.axvline(x=right_root, color='red', linestyle='--')
        plt.plot(x, np.zeros(len(x)), color='black')
        plt.plot(x, y)
        plt.scatter([left_root, right_root], [0, 0], color='red')

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
