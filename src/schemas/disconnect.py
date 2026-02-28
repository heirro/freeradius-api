from pydantic import BaseModel, Field
from typing import Optional


class DisconnectRequest(BaseModel):
    username: str = Field(..., description="Username to disconnect from the NAS")
    nas_ip: Optional[str] = Field(
        None,
        description="NAS IP address. Uses RADIUS_NAS_IP from config if not provided.",
    )
    radius_secret: Optional[str] = Field(
        None,
        description="RADIUS shared secret. Uses RADIUS_SECRET from config if not provided.",
    )
    port: Optional[int] = Field(
        None,
        description="NAS CoA/Disconnect port (default: 3799).",
    )


class DisconnectResponse(BaseModel):
    success: bool = Field(..., description="True if radclient returned exit code 0")
    username: str
    nas_ip: str
    port: int
    output: str = Field(..., description="Combined stdout/stderr from radclient")
    return_code: int
