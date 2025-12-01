import reflex as rx
from app.schemas.datasource import DataSource
from app.enums import DataSourceType, DataSourceStatus


class DataSourceState(rx.State):
    sources: list[DataSource] = [
        DataSource(
            id="ds1",
            name="Oura Ring",
            type=DataSourceType.WEARABLE,
            status=DataSourceStatus.CONNECTED,
            last_sync="10 mins ago",
            icon="ring",
        ),
        DataSource(
            id="ds2",
            name="Apple Health",
            type=DataSourceType.API,
            status=DataSourceStatus.CONNECTED,
            last_sync="1 hour ago",
            icon="activity",
        ),
        DataSource(
            id="ds3",
            name="LabCorp Results",
            type=DataSourceType.FILE,
            status=DataSourceStatus.DISCONNECTED,
            last_sync="2 weeks ago",
            icon="file-text",
        ),
    ]
    filter_type: str = "Devices & Wearables"
    filter_options: list[str] = [
        "Devices & Wearables",
        "File Imports",
        "API Connections",
        "Import History",
        "Connected Devices & Wearables",
    ]

    @rx.var
    def filtered_sources(self) -> list[DataSource]:
        if self.filter_type == "Devices & Wearables":
            return [s for s in self.sources if s.type == DataSourceType.WEARABLE]
        elif self.filter_type == "File Imports":
            return [s for s in self.sources if s.type == DataSourceType.FILE]
        elif self.filter_type == "API Connections":
            return [s for s in self.sources if s.type == DataSourceType.API]
        elif self.filter_type == "Connected Devices & Wearables":
            return [
                s
                for s in self.sources
                if s.status == DataSourceStatus.CONNECTED
                and s.type == DataSourceType.WEARABLE
            ]
        return self.sources

    @rx.event
    def set_filter_type(self, filter_type: str):
        self.filter_type = filter_type

    @rx.event
    def sync_source(self, source_id: str):
        return rx.toast("Sync started...")