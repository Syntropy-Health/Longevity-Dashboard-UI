from pydantic import BaseModel
from app.enums import DataSourceType, DataSourceStatus


class DataSource(BaseModel):
    id: str
    name: str
    type: DataSourceType
    status: DataSourceStatus
    last_sync: str
    icon: str = "cpu"