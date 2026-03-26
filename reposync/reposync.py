import reflex as rx
import requests
import os

# THE STATE: Pure GitHub Logic
class State(rx.State):
    github_username: str = "reory" 
    projects: list[dict] = []
    search_text: str = ""
    is_loading: bool = False

    def set_search_text(self, text: str):
        self.search_text = text

    def fetch_repos(self):
        self.is_loading = True
        yield
        try:
            # Fetching your real-time GitHub data
            url = f"https://api.github.com/users/{self.github_username}/repos?sort=updated"
            headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN', '')}"}
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                self.projects = [
                    {
                        "name": r["name"],
                        "description": r["description"] or "A modern Python project.",
                        "url": r["html_url"],
                        "language": r["language"] or "Misc",
                        "stars": r["stargazers_count"]
                    }
                    for r in res.json() if not r["fork"]
                ]
        except Exception as e:
            print(f"Error: {e}")
        self.is_loading = False

    @rx.var
    def filtered_projects(self) -> list[dict]:
        if not self.search_text:
            return self.projects
        search = self.search_text.lower()
        return [
            p for p in self.projects 
            if search in p["name"].lower() 
            or search in p["language"].lower()
        ]
    
    @rx.var
    def project_count(self) -> int:
        return len(self.filtered_projects)

# UI: REPO CARD
def repo_card(repo: dict):
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(repo["name"], size="4"),
                rx.spacer(),
                rx.badge(f"⭐ {repo['stars']}", color_scheme="yellow"),
            ),
            rx.text(repo["description"], size="2", color_short="gray"),
            rx.hstack(
                rx.badge(repo["language"], variant="outline", color_scheme="iris"),
                rx.spacer(),
                rx.link(
                    rx.button("Source", size="1", variant="ghost"),
                    href=repo["url"],
                    is_external=True,
                ),
            ),
            spacing="3",
            align="start",
        ),
        width="100%",
    )

# THE MAIN PAGE
def index():
    return rx.center(
        rx.vstack(
            # Header Section
            rx.vstack(
                rx.hstack(
                    rx.heading("Portfolio", size="9", weight="bold"),
                    rx.badge(
                        State.project_count, 
                        variant="soft", 
                        color_scheme="iris", 
                        size="3",
                        radius="full"
                    ),
                    align="center",
                    spacing="3",
                ),
                rx.text("Direct GitHub API Sync • Python 3.13", color_short="slate"),
                align="center",
            ),
            
            # Action Bar
            rx.hstack(
                rx.button(
                    "Sync GitHub", 
                    on_click=State.fetch_repos, 
                    loading=State.is_loading, 
                    color_scheme="iris"
                ),
                rx.input(
                    placeholder="Filter by name or language...",
                    on_change=State.set_search_text,
                    width="300px"
                ),
                spacing="4",
                margin_top="1em",
            ),
            
            rx.divider(margin_y="2em"),
            
            # The Repository Grid
            rx.grid(
                rx.foreach(State.filtered_projects, repo_card),
                columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                spacing="4",
                width="100%",
            ),
            
            spacing="5",
            padding="2em",
            max_width="1100px",
            align="center",
        )
    )

# APP 
app = rx.App(
    theme=rx.theme(appearance="dark", accent_color="iris")
)
app.add_page(index, title="RepoSync | Portfolio")