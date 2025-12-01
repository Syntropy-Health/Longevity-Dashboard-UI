import reflex as rx
from app.states.datasource_state import DataSourceState
from app.styles.glass_styles import GlassStyles
from app.schemas.datasource import DataSource
from app.enums import DataSourceStatus


def datasource_card(source: DataSource) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(source.icon, class_name="w-8 h-8 text-teal-400 mb-4"),
            rx.el.div(
                rx.el.span(
                    source.status,
                    class_name=f"text-xs font-bold uppercase tracking-wider px-2 py-1 rounded-full border {rx.cond(source.status == DataSourceStatus.CONNECTED, 'bg-teal-500/10 text-teal-400 border-teal-500/20', rx.cond(source.status == DataSourceStatus.SYNCING, 'bg-blue-500/10 text-blue-400 border-blue-500/20', 'bg-slate-500/10 text-slate-400 border-slate-500/20'))}",
                ),
                class_name="mb-4",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.h3(source.name, class_name="text-xl font-bold text-white mb-1"),
        rx.el.p(
            f"Last synced: {source.last_sync}", class_name="text-sm text-slate-400 mb-6"
        ),
        rx.el.button(
            rx.cond(source.status == DataSourceStatus.CONNECTED, "Sync Now", "Connect"),
            on_click=lambda: DataSourceState.sync_source(source.id),
            class_name="w-full py-2 rounded-lg bg-white/5 hover:bg-teal-500/20 hover:text-teal-300 text-slate-300 border border-white/10 transition-all",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex flex-col",
    )


def data_sources_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Data Sources", class_name="text-2xl font-bold text-white"),
            rx.el.button("+ Add Source", class_name=GlassStyles.BUTTON_PRIMARY),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.foreach(
                DataSourceState.filter_options,
                lambda option: rx.el.button(
                    option,
                    on_click=lambda: DataSourceState.set_filter_type(option),
                    class_name=rx.cond(
                        DataSourceState.filter_type == option,
                        "px-4 py-2 rounded-lg text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30 transition-all",
                        "px-4 py-2 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 transition-all",
                    ),
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6 bg-white/5 p-1 rounded-xl w-fit",
        ),
        rx.el.div(
            rx.cond(
                DataSourceState.filtered_sources,
                rx.el.div(
                    rx.foreach(DataSourceState.filtered_sources, datasource_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                rx.el.div(
                    rx.el.p(
                        "No data sources found for this category.",
                        class_name="text-slate-500 italic",
                    ),
                    class_name=f"{GlassStyles.PANEL} p-8 text-center w-full",
                ),
            ),
            class_name="min-h-[300px]",
        ),
        class_name="animate-in fade-in duration-500",
    )