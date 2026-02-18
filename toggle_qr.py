import os
import sys
import time
from typing import Optional

import requests


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def toggle_qr(enable: bool, timeout_s: int = 20) -> None:
    base = _require_env("BASE").rstrip("/")
    username = _require_env("USERNAME")
    password = _require_env("PASSWORD")

    s = requests.Session()

    # 1) init_device_set (timestamp para evitar cache)
    ts = int(time.time() * 1000)
    s.get(f"{base}/init_device_set.fcgi", params={"_": ts}, timeout=timeout_s)

    # 2) login
    r_login = s.post(f"{base}/login.fcgi", data={"login": username, "password": password}, timeout=timeout_s)
    r_login.raise_for_status()
    session_data = r_login.json()
    session_token = session_data.get("session")
    if not session_token:
        raise RuntimeError("Login failed: no session token in response")

    # Set cookies
    s.cookies.set("login", username)
    s.cookies.set("session", session_token)

    print(f"✅ Login OK, session: {session_token}")

    # 3) Ler configuração atual
    get_payload = {
        "identifier": ["face_identification_enabled", "card_identification_enabled", "qrcode_identification_enabled", "pin_identification_enabled"]
    }
    r_get = s.post(f"{base}/get_configuration.fcgi", json=get_payload, timeout=timeout_s)
    r_get.raise_for_status()
    cfg = r_get.json()
    qr_atual = cfg.get("identifier", {}).get("qrcode_identification_enabled")
    status_atual = "DESATIVADO" if qr_atual == "0" else "ATIVADO"
    print(f"📥 QR Code atualmente: {status_atual}")

    # 4) Alterar configuração
    set_payload = {
        "identifier": {
            "qrcode_identification_enabled": "1" if enable else "0"
        }
    }
    start = time.time()
    r_set = s.post(f"{base}/set_configuration.fcgi", json=set_payload, timeout=timeout_s)
    elapsed_ms = int((time.time() - start) * 1000)
    print(f"🔧 POST {base}/set_configuration.fcgi -> status={r_set.status_code} elapsedMs={elapsed_ms}")
    r_set.raise_for_status()

    # 5) Confirmar mudança
    r_confirm = s.post(f"{base}/get_configuration.fcgi", json=get_payload, timeout=timeout_s)
    r_confirm.raise_for_status()
    cfg_nova = r_confirm.json()
    qr_novo = cfg_nova.get("identifier", {}).get("qrcode_identification_enabled")
    status_novo = "DESATIVADO" if qr_novo == "0" else "ATIVADO"
    print(f"✅ QR Code após alteração: {status_novo}")

    esperado = "1" if enable else "0"
    if qr_novo == esperado:
        print(f"🎉 SUCESSO: QR Code {'ativado' if enable else 'desativado'} via API!")
    else:
        raise RuntimeError(f"Falha: QR Code não foi {'ativado' if enable else 'desativado'}. Status esperado: {esperado}, atual: {qr_novo}")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("enable", "disable"):
        raise SystemExit("Usage: python toggle_qr.py [enable|disable]")

    enable = sys.argv[1] == "enable"
    toggle_qr(enable=enable)


if __name__ == "__main__":
    main()