from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union

DEFAULT_RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"


def get_results_dir(explicit: Optional[Union[str, Path]] = None) -> Path:
    """Return the directory where experiment artifacts are stored."""
    if explicit:
        return Path(explicit).expanduser().resolve()

    env_path = os.getenv("STEGANOGRAPHY_RESULTS_DIR")
    if env_path:
        return Path(env_path).expanduser().resolve()

    return DEFAULT_RESULTS_DIR
