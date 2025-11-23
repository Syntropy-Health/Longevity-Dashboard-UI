import reflex as rx

config = rx.Config(
    app_name="longevity_clinic",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)