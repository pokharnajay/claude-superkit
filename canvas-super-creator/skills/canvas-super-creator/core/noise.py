"""Perlin noise generation using numpy permutation table approach."""

import numpy as np
from PIL import Image


def _build_permutation(seed: int = 0) -> np.ndarray:
    """Build a 512-entry permutation table from seed."""
    rng = np.random.RandomState(seed)
    p = np.arange(256, dtype=int)
    rng.shuffle(p)
    return np.tile(p, 2)


def _fade(t: np.ndarray) -> np.ndarray:
    """Smoothstep fade curve: 6t^5 - 15t^4 + 10t^3."""
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def _lerp(a: np.ndarray, b: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Linear interpolation."""
    return a + t * (b - a)


_GRADIENTS_2D = np.array([
    [1, 1], [-1, 1], [1, -1], [-1, -1],
    [1, 0], [-1, 0], [0, 1], [0, -1],
], dtype=np.float64)


def _grad(hash_val: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Compute gradient dot product."""
    g = _GRADIENTS_2D[hash_val % 8]
    return g[..., 0] * x + g[..., 1] * y


def _perlin_single(x: np.ndarray, y: np.ndarray, perm: np.ndarray) -> np.ndarray:
    """Evaluate single-octave Perlin noise at (x, y) coordinate arrays."""
    xi = x.astype(int) & 255
    yi = y.astype(int) & 255
    xf = x - np.floor(x)
    yf = y - np.floor(y)

    u = _fade(xf)
    v = _fade(yf)

    aa = perm[perm[xi] + yi]
    ab = perm[perm[xi] + yi + 1]
    ba = perm[perm[xi + 1] + yi]
    bb = perm[perm[xi + 1] + yi + 1]

    x1 = _lerp(_grad(aa, xf, yf), _grad(ba, xf - 1, yf), u)
    x2 = _lerp(_grad(ab, xf, yf - 1), _grad(bb, xf - 1, yf - 1), u)

    return _lerp(x1, x2, v)


def perlin_noise_2d(
    width: int,
    height: int,
    scale: float = 100.0,
    octaves: int = 4,
    persistence: float = 0.5,
    seed: int = 0,
) -> np.ndarray:
    """Generate 2D Perlin noise array with values 0-1."""
    perm = _build_permutation(seed)
    ys, xs = np.meshgrid(np.arange(height), np.arange(width), indexing="ij")

    result = np.zeros((height, width), dtype=np.float64)
    amplitude = 1.0
    frequency = 1.0
    max_val = 0.0

    for _ in range(octaves):
        sx = xs * frequency / scale
        sy = ys * frequency / scale
        result += _perlin_single(sx, sy, perm) * amplitude
        max_val += amplitude
        amplitude *= persistence
        frequency *= 2.0

    result = (result / max_val + 1.0) / 2.0
    return np.clip(result, 0.0, 1.0)


def fractal_noise(
    width: int,
    height: int,
    octaves: int = 6,
    lacunarity: float = 2.0,
    gain: float = 0.5,
    seed: int = 0,
) -> np.ndarray:
    """Layered fractal noise for organic textures."""
    perm = _build_permutation(seed)
    ys, xs = np.meshgrid(np.arange(height), np.arange(width), indexing="ij")

    result = np.zeros((height, width), dtype=np.float64)
    amplitude = 1.0
    frequency = 1.0
    max_val = 0.0

    for _ in range(octaves):
        sx = xs * frequency / width
        sy = ys * frequency / height
        result += _perlin_single(sx, sy, perm) * amplitude
        max_val += amplitude
        amplitude *= gain
        frequency *= lacunarity

    result = (result / max_val + 1.0) / 2.0
    return np.clip(result, 0.0, 1.0)


def turbulence(
    width: int,
    height: int,
    scale: float = 100.0,
    octaves: int = 4,
    seed: int = 0,
) -> np.ndarray:
    """Absolute-value noise for cloud/smoke effects."""
    perm = _build_permutation(seed)
    ys, xs = np.meshgrid(np.arange(height), np.arange(width), indexing="ij")

    result = np.zeros((height, width), dtype=np.float64)
    amplitude = 1.0
    frequency = 1.0
    max_val = 0.0

    for _ in range(octaves):
        sx = xs * frequency / scale
        sy = ys * frequency / scale
        result += np.abs(_perlin_single(sx, sy, perm)) * amplitude
        max_val += amplitude
        amplitude *= 0.5
        frequency *= 2.0

    return np.clip(result / max_val, 0.0, 1.0)


def noise_to_image(
    noise: np.ndarray,
    color_a: tuple,
    color_b: tuple,
) -> Image.Image:
    """Map noise array to two-color gradient PIL Image."""
    h, w = noise.shape
    ca = np.array(color_a[:3], dtype=np.float64)
    cb = np.array(color_b[:3], dtype=np.float64)

    t = noise[..., np.newaxis]
    rgb = (1.0 - t) * ca + t * cb
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    alpha = np.full((h, w, 1), 255, dtype=np.uint8)
    rgba = np.concatenate([rgb, alpha], axis=2)
    return Image.fromarray(rgba, "RGBA")


def flow_field(
    width: int,
    height: int,
    scale: float = 50.0,
    seed: int = 0,
) -> np.ndarray:
    """Generate angle array (radians) for particle/flow effects."""
    noise = perlin_noise_2d(width, height, scale=scale, octaves=3, seed=seed)
    return noise * 2.0 * np.pi
