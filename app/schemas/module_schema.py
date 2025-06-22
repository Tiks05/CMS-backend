from pydantic import BaseModel

class BannerItem(BaseModel):
    banner_url: str
    path: str
