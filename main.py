"""
main.py
-------
Entry point for the News Reader CLI application.

This module owns the interactive terminal experience:
    - Renders menus, prompts, and article listings using Rich.
    - Delegates all validation to `utils.py`.
    - Delegates all API communication to `news_service.py`.
    - Delegates configuration loading to `config.py`.

Run with:
    python main.py
"""

from __future__ import annotations

import sys
from typing import Any, Callable

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

from config import ConfigurationError, Settings, load_settings
from news_service import NewsAPIError, NewsService
from utils import (
    ValidationError,
    format_published_date,
    safe_get,
    truncate_text,
    validate_category,
    validate_country,
    validate_keyword,
    validate_page_size,
    validate_sort_by,
)

console = Console()

APP_TITLE = "📰  NEWS READER CLI"
APP_SUBTITLE = "Powered by NewsAPI.org"


def print_banner() -> None:
    """Render the application banner."""
    console.print()
    console.print(
        Panel.fit(
            f"[bold cyan]{APP_TITLE}[/bold cyan]\n[dim]{APP_SUBTITLE}[/dim]",
            border_style="cyan",
            padding=(1, 6),
        )
    )


def print_menu() -> None:
    """Render the main menu options."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("[bold cyan]1[/bold cyan]", "Search news by keyword")
    table.add_row("[bold cyan]2[/bold cyan]", "Top headlines by country")
    table.add_row("[bold cyan]3[/bold cyan]", "Top headlines by category")
    table.add_row("[bold cyan]4[/bold cyan]", "View supported categories")
    table.add_row("[bold cyan]5[/bold cyan]", "View supported countries")
    table.add_row("[bold cyan]0[/bold cyan]", "Exit")
    console.print(Panel(table, title="Main Menu", border_style="blue", expand=False))


def display_articles(articles: list[dict[str, Any]]) -> None:
    """
    Render a list of articles in a professional, readable format using Rich Panels.

    Args:
        articles: A list of article dictionaries as returned by NewsAPI.org.
    """
    if not articles:
        console.print(
            Panel(
                "[yellow]No articles were found for this request. "
                "Try a different keyword, category, or country.[/yellow]",
                border_style="yellow",
            )
        )
        return

    console.print(f"\n[bold green]Found {len(articles)} article(s):[/bold green]\n")

    for index, article in enumerate(articles, start=1):
        title = safe_get(article, "title", default="Untitled article")
        source = safe_get(article, "source", "name", default="Unknown source")
        author = safe_get(article, "author", default="Unknown author")
        published = format_published_date(article.get("publishedAt"))
        description = truncate_text(article.get("description"), max_length=220)
        url = safe_get(article, "url", default="N/A")

        body = Text()
        body.append(f"{description}\n\n", style="white")
        body.append("Source: ", style="bold")
        body.append(f"{source}    ", style="magenta")
        body.append("Author: ", style="bold")
        body.append(f"{author}\n", style="magenta")
        body.append("Published: ", style="bold")
        body.append(f"{published}\n", style="green")
        body.append("URL: ", style="bold")
        body.append(f"{url}", style="underline blue")

        console.print(
            Panel(
                body,
                title=f"[bold cyan]{index}. {title}[/bold cyan]",
                border_style="blue",
                padding=(1, 2),
            )
        )


def display_key_value_list(title: str, items: dict[str, str] | list[str]) -> None:
    """
    Render a simple reference table for categories or countries.

    Args:
        title: Table title.
        items: Either a dict of code -> display name, or a list of plain values.
    """
    table = Table(title=title, border_style="cyan", header_style="bold cyan")
    if isinstance(items, dict):
        table.add_column("Code")
        table.add_column("Name")
        for code, name in items.items():
            table.add_row(code, name)
    else:
        table.add_column("Value")
        for value in items:
            table.add_row(value)
    console.print(table)


# --------------------------------------------------------------------------- #
# Menu action handlers
# --------------------------------------------------------------------------- #


def handle_search(service: NewsService, settings: Settings) -> None:
    """Prompt for a keyword and display matching articles."""
    try:
        keyword = validate_keyword(Prompt.ask("[bold]Enter a search keyword[/bold]"))
        sort_choice = Prompt.ask(
            "[bold]Sort by[/bold]",
            choices=["relevancy", "popularity", "publishedAt"],
            default="publishedAt",
        )
        sort_by = validate_sort_by(sort_choice)
        page_size = validate_page_size(
            IntPrompt.ask("[bold]How many articles?[/bold]", default=settings.default_page_size)
        )
    except ValidationError as exc:
        console.print(f"[bold red]Input error:[/bold red] {exc}")
        return

    with console.status("[bold cyan]Searching NewsAPI.org...[/bold cyan]"):
        try:
            articles = service.search_news(keyword=keyword, sort_by=sort_by, page_size=page_size)
        except NewsAPIError as exc:
            console.print(f"[bold red]API error:[/bold red] {exc}")
            return

    display_articles(articles)


def handle_headlines_by_country(service: NewsService, settings: Settings) -> None:
    """Prompt for a country and display top headlines."""
    try:
        country = validate_country(
            Prompt.ask("[bold]Enter a country code[/bold] (e.g. us, gb, in)", default=settings.default_country)
        )
        page_size = validate_page_size(
            IntPrompt.ask("[bold]How many articles?[/bold]", default=settings.default_page_size)
        )
    except ValidationError as exc:
        console.print(f"[bold red]Input error:[/bold red] {exc}")
        return

    with console.status("[bold cyan]Fetching top headlines...[/bold cyan]"):
        try:
            articles = service.get_top_headlines(country=country, page_size=page_size)
        except NewsAPIError as exc:
            console.print(f"[bold red]API error:[/bold red] {exc}")
            return

    display_articles(articles)


def handle_headlines_by_category(service: NewsService, settings: Settings) -> None:
    """Prompt for a category (and optional country) and display top headlines."""
    try:
        category = validate_category(
            Prompt.ask("[bold]Enter a category[/bold] (e.g. technology, sports, health)")
        )
        country = validate_country(
            Prompt.ask("[bold]Enter a country code[/bold] (e.g. us, gb, in)", default=settings.default_country)
        )
        page_size = validate_page_size(
            IntPrompt.ask("[bold]How many articles?[/bold]", default=settings.default_page_size)
        )
    except ValidationError as exc:
        console.print(f"[bold red]Input error:[/bold red] {exc}")
        return

    with console.status("[bold cyan]Fetching top headlines...[/bold cyan]"):
        try:
            articles = service.get_top_headlines(country=country, category=category, page_size=page_size)
        except NewsAPIError as exc:
            console.print(f"[bold red]API error:[/bold red] {exc}")
            return

    display_articles(articles)


def handle_show_categories(_: NewsService, settings: Settings) -> None:
    """Display the list of supported news categories."""
    display_key_value_list("Supported Categories", settings.categories)


def handle_show_countries(_: NewsService, settings: Settings) -> None:
    """Display the list of supported country codes."""
    display_key_value_list("Supported Countries", settings.countries)


# --------------------------------------------------------------------------- #
# Application bootstrap
# --------------------------------------------------------------------------- #


def build_menu_actions() -> dict[str, Callable[[NewsService, Settings], None]]:
    """Map menu choice strings to their corresponding handler functions."""
    return {
        "1": handle_search,
        "2": handle_headlines_by_country,
        "3": handle_headlines_by_category,
        "4": handle_show_categories,
        "5": handle_show_countries,
    }


def run() -> None:
    """Main application loop: load settings, then repeatedly show the menu."""
    print_banner()

    try:
        settings = load_settings()
    except ConfigurationError as exc:
        console.print(Panel(f"[bold red]Configuration error:[/bold red] {exc}", border_style="red"))
        sys.exit(1)

    actions = build_menu_actions()

    with NewsService(settings) as service:
        while True:
            print_menu()
            choice = Prompt.ask("[bold]Select an option[/bold]", default="0")

            if choice == "0":
                console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
                break

            action = actions.get(choice)
            if action is None:
                console.print("[bold red]Invalid option. Please choose a number from the menu.[/bold red]")
                continue

            try:
                action(service, settings)
            except KeyboardInterrupt:
                raise
            except Exception as exc:  # noqa: BLE001 - top-level safety net for unexpected errors
                console.print(f"[bold red]Unexpected error:[/bold red] {exc}")

            console.print()  # spacing before next menu render


def main() -> None:
    """CLI entry point with top-level exception handling."""
    try:
        run()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Interrupted by user. Goodbye! 👋[/bold yellow]\n")
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001 - last-resort safety net
        console.print(f"\n[bold red]Fatal error:[/bold red] {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
