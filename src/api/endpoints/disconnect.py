import subprocess

from fastapi import APIRouter, HTTPException, status

from src.core.config import get_settings
from src.schemas.disconnect import DisconnectRequest, DisconnectResponse

router = APIRouter()
settings = get_settings()


@router.post("/disconnect", response_model=DisconnectResponse, summary="Disconnect a user from NAS")
def disconnect_user(request: DisconnectRequest):
    """
    Kirim Disconnect-Request ke NAS menggunakan **radclient**.

    Setara dengan perintah berikut:
    ```bash
    echo 'User-Name = "<username>"' | radclient -x <nas_ip>:<port> disconnect <secret>
    ```
    - `nas_ip` dan `radius_secret` bersifat opsional; jika tidak diisi akan
      menggunakan nilai dari konfigurasi server (`RADIUS_NAS_IP` / `RADIUS_SECRET`).
    - Membutuhkan `radclient` terinstal (`freeradius-utils`).
    """
    nas_ip = request.nas_ip or settings.RADIUS_NAS_IP
    secret = request.radius_secret or settings.RADIUS_SECRET
    port = request.port if request.port is not None else settings.RADIUS_COA_PORT

    command_input = f'User-Name = "{request.username}"'

    try:
        result = subprocess.run(
            ["radclient", "-x", f"{nas_ip}:{port}", "disconnect", secret],
            input=command_input,
            capture_output=True,
            text=True,
            timeout=10,
        )

        output = (result.stdout + result.stderr).strip()
        success = result.returncode == 0

        return DisconnectResponse(
            success=success,
            username=request.username,
            nas_ip=nas_ip,
            port=port,
            output=output,
            return_code=result.returncode,
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="radclient timed out. Pastikan NAS dapat dijangkau dari server.",
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="radclient tidak ditemukan. Install dengan: apt install freeradius-utils",
        )
