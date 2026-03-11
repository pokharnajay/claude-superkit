"""Core library for canvas-design: helpers for generating visual art with PIL/Pillow."""

# Noise generation
from .noise import (
    perlin_noise_2d,
    fractal_noise,
    turbulence,
    noise_to_image,
    flow_field,
)

# Gradient generation
from .gradients import (
    linear_gradient,
    radial_gradient,
    conic_gradient,
    multi_stop_gradient,
    noise_gradient,
)

# Texture overlays
from .textures import (
    grain_overlay,
    paper_texture,
    halftone,
    scanlines,
    stipple,
    crosshatch,
)

# Color manipulation
from .color_engine import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsl,
    hsl_to_rgb,
    tint,
    shade,
    desaturate,
    complementary,
    analogous,
    triadic,
    split_complementary,
    contrast_ratio,
    ensure_readable,
)

# Blend modes
from .blending import (
    blend_multiply,
    blend_screen,
    blend_overlay,
    blend_soft_light,
    blend_hard_light,
    blend_color_dodge,
    blend_color_burn,
    blend_difference,
    composite,
)

# Composition guides
from .composition import (
    rule_of_thirds,
    golden_ratio,
    fibonacci_spiral,
    safe_zone,
    modular_grid,
    margin_rect,
    diagonal_armature,
)

# Geometric drawing
from .geometry import (
    bezier_curve,
    wave_line,
    regular_polygon,
    star,
    concentric_circles,
    parallel_lines,
    rounded_rect,
)

# Image effects
from .effects import (
    drop_shadow,
    outer_glow,
    vignette,
    duotone,
    posterize,
    color_overlay,
)
