import reflex as rx
import os

# This looks for the URL we set in the Render Environment tab
# If it can't find it, it defaults to localhost (so it still works for you locally!)
app_url = os.getenv("REFLEX_BACKEND_URL", "http://localhost:8000")

config = rx.Config(
    app_name="reposync",
    api_url="https://reposync.onrender.com",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)