"""Patient analytics reusable components."""

import reflex as rx
from ...data import BiomarkerCategory, BiomarkerMetric
from ...components.charts import TOOLTIP_PROPS
from ...styles.constants import GlassStyles


def trend_chart(data: list[dict], color: str) -> rx.Component:
    """Mini area chart for biomarker trends."""
    return rx.recharts.area_chart(
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.area(
            data_key="value",
            stroke=color,
            fill=color,
            type_="monotone",
            stroke_width=2,
            fill_opacity=0.2,
        ),
        rx.recharts.x_axis(data_key="date", hide=True),
        rx.recharts.y_axis(hide=True, domain=["auto", "auto"]),
        data=data,
        height=70,
        width="100%",
        margin={"top": 5, "right": 0, "bottom": 0, "left": 0},
    )


def status_badge(status: str) -> rx.Component:
    """Render a status badge with appropriate styling."""
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            ("Optimal", GlassStyles.STATUS_OPTIMAL),
            ("Warning", GlassStyles.STATUS_WARNING),
            ("Critical", GlassStyles.STATUS_CRITICAL),
            GlassStyles.STATUS_DEFAULT,
        ),
    )


def status_dot(status: str) -> rx.Component:
    """Render a small status indicator dot."""
    return rx.el.div(
        class_name=rx.match(
            status,
            ("Optimal", GlassStyles.DOT_OPTIMAL),
            ("Warning", GlassStyles.DOT_WARNING),
            ("Critical", GlassStyles.DOT_CRITICAL),
            GlassStyles.DOT_DEFAULT,
        )
    )


def metric_card(metric: BiomarkerMetric) -> rx.Component:
    """Render a biomarker metric card with trend chart."""
    color = rx.match(
        metric["status"],
        ("Optimal", "#2DD4BF"),
        ("Warning", "#FBBF24"),
        ("Critical", "#F87171"),
        "#94A3B8",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    metric["name"],
                    class_name=f"{GlassStyles.METRIC_LABEL} mb-3",
                ),
                rx.el.div(
                    rx.el.span(
                        metric["value"],
                        class_name=f"{GlassStyles.METRIC_VALUE} mr-1",
                    ),
                    rx.el.span(
                        metric["unit"],
                        class_name=GlassStyles.METRIC_UNIT,
                    ),
                    class_name="flex items-baseline mb-1",
                ),
            ),
            status_badge(metric["status"]),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            trend_chart(metric["history"], color),
            class_name="h-20 w-full mb-4 opacity-70 hover:opacity-100 transition-all duration-500 -ml-2",
        ),
        rx.el.div(
            status_dot(metric["status"]),
            rx.el.span(
                "OPTIMAL RANGE",
                class_name=GlassStyles.REFERENCE_LABEL,
            ),
            rx.el.span(
                metric["reference_range"],
                class_name=GlassStyles.REFERENCE_VALUE,
            ),
            class_name=GlassStyles.REFERENCE_RANGE_PILL,
        ),
        class_name=GlassStyles.BIOMARKER_CARD,
    )


def category_section(category: BiomarkerCategory) -> rx.Component:
    """Render a category section with its biomarker metrics."""
    return rx.el.div(
        rx.el.h3(
            category["category"],
            class_name=GlassStyles.SECTION_TITLE,
        ),
        rx.el.div(
            rx.foreach(category["metrics"], metric_card),
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
        ),
        class_name="mb-12",
    )
