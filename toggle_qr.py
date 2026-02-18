import os
from urllib.parse import urlparse

import requests


def toggle_qr(enable: bool) -> None:
    base_url = os.getenv("BASE", "").strip().rstrip("/")
    username = os.getenv("USERNAME", "").strip()
    password = os.getenv("PASSWORD", "").strip()

    # Debug seguro (não vaza credenciais)
    if base_url:
        p = urlparse(base_url)
        print("DEBUG base_host =", p.netloc)
        print("DEBUG base_path =", p.path)
    else:
        print("DEBUG base_host = <EMPTY>")
        print("DEBUG base_path = <EMPTY>")

    print("DEBUG has_USERNAME =", bool(username))
    print("DEBUG has_PASSWORD =", bool(password))

    if not base_url or not username or not password:
        raise ValueError("Faltam variáveis: BASE, USERNAME, PASSWORD")

    # Se BASE já vier com /api, evita duplicar /api
    if base_url.endswith("/api"):
        url = f"{base_url}/qr/toggle"
    else:
        url = f"{base_url}/api/qr/toggle"

    print("DEBUG url =", url)

    r = requests.post(
        url,
        json={"enable": enable},
        auth=(username, password),
        timeout=30,
    )

    print("DEBUG status =", r.status_code)

    # Debug do corpo em caso de erro (limitado)
    if r.status_code >= 400:
        body = (r.text or "").strip()
        print("DEBUG response_body_first_200 =", body[:200])

    r.raise_for_status()