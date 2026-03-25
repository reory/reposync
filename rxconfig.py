import reflex as rx
import os

config = rx.Config(
    app_name="reposync",
    api_url = os.getenv("REFLEX_BACKEND_URL", "http://localhost:8000"),
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
