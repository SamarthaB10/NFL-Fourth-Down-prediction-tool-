# C++ Possession Simulator

The drive simulator runs in C++ for speed (Monte Carlo with thousands of trials) and is exposed to Python via **pybind11**. If the extension is not built, the API automatically falls back to an equivalent Python implementation.

## Build

From the `backend/` directory:

```bash
pip install pybind11
python setup_sim.py build_ext --inplace
```

This produces `nfl4d_sim.cpython-*.so` (or `.pyd` on Windows) in `backend/`.

Verify:

```bash
python -c "import nfl4d_sim; print(nfl4d_sim.simulate_possession(45, 4, 4, 900, 0, 0, 'go', 1))"
```

## API

`POST /simulate/possession` (requires Bearer token from `/auth/login`)

- User picks `go`, `punt`, or `field_goal` on 4th down
- Engine resolves that play, then simulates subsequent downs until the possession ends
- Returns mean points scored over `trials` runs plus one sample play-by-play log
