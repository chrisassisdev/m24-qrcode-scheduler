# toggle_qr_debug.py
import os
import sys

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value

def toggle_qr_debug() -> None:
    """
    Função de debug para verificar se os secrets estão sendo lidos.
    Imprime informações parciais para não expor credenciais.
    """
    base = _require_env("BASE")
    username = _require_env("USERNAME")
    password = _require_env("PASSWORD")

    print(f"DEBUG: BASE (início): {base[:10]}...")  # Imprime só o início
    print(f"DEBUG: USERNAME: {username}")
    print(f"DEBUG: PASSWORD (tamanho): {len(password)}")  # Imprime só o tamanho

    # Para a execução com um erro intencional para não chamar a API real
    raise RuntimeError("DEBUG STOP - Secrets test successful, preventing API call.")

def main() -> None:
    toggle_qr_debug()

if __name__ == "__main__":
    main()