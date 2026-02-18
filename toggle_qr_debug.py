import os

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value

if __name__ == "__main__":
    base = _require_env("BASE")
    username = _require_env("USERNAME")
    password = _require_env("PASSWORD")

    print(f"DEBUG: BASE (inicio): {base[:15]}...")
    print(f"DEBUG: USERNAME: {username}")
    print(f"DEBUG: PASSWORD (tamanho): {len(password)}")

    raise RuntimeError("DEBUG STOP - Secrets OK (parando antes de chamar a API).")