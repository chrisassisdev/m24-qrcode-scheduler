import os
import requests

def toggle_qr(enable: bool):
    base_url = os.getenv("BASE", "").strip().rstrip("/")
    username = os.getenv("USERNAME", "").strip()
    password = os.getenv("PASSWORD", "").strip()

    if not base_url or not username or not password:
        raise ValueError("Faltam variáveis: BASE, USERNAME, PASSWORD")

    # BASE recomendado: https://dominio
    url = f"{base_url}/api/qr/toggle"
    print("DEBUG url =", url)

    r = requests.post(
        url,
        json={"enable": enable},
        auth=(username, password),
        timeout=30
    )
    print("DEBUG status =", r.status_code)
    if r.status_code >= 400:
        print("DEBUG body (first 200) =", (r.text or "")[:200])
    r.raise_for_status()