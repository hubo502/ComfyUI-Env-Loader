from pathlib import Path
import os
import time


def find_comfy_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "custom_nodes").exists():
            return parent
    return Path.cwd()


def parse_env_file(path: Path) -> dict:
    result = {}
    if not path.exists() or not path.is_file():
        return result
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return result
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip()
        if v.startswith("\"") and v.endswith("\""):
            v = v[1:-1]
        elif v.startswith("'") and v.endswith("'"):
            v = v[1:-1]
        result[k] = v
    return result


ENV_PATH = find_comfy_root() / ".env"
print(f"[Env Loader] Loading env from {ENV_PATH}")
try:
    _loaded_keys = list(parse_env_file(ENV_PATH).keys())
    if _loaded_keys:
        print(f"[Env Loader] Loaded keys: {', '.join(_loaded_keys)}")
    else:
        print(f"[Env Loader] No keys found in .env file or file missing.")
except Exception as e:
    print(f"[Env Loader] Error loading env file: {e}")


class EnvKeySelector:
    @classmethod
    def INPUT_TYPES(cls):
        keys = list(parse_env_file(ENV_PATH).keys())
        if not keys:
            keys = [""]
        return {"required": {"key": (keys,)}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("value",)
    FUNCTION = "get_value"
    CATEGORY = "Utils"

    def get_value(self, key: str):
        values = parse_env_file(ENV_PATH)
        return (values.get(key, ""),)

    def IS_CHANGED(self, **kwargs):
        try:
            return os.path.getmtime(ENV_PATH)
        except Exception:
            return time.time()

