  import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich import print as rprint

FILENAME = "tasks.json"
console = Console()


def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []


def save_tasks(tasks):
    """Save the current task list to the JSON file."""
    try:
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        rprint(f"[bold red]Error saving tasks:[/bold red] {e}")


def list_tasks(tasks):
    """Display tasks in a formatted table."""
    console.clear()
    if not tasks:
        msg = "[yellow]Your task list is empty. Add something![/yellow]"
        rprint(Panel(msg, title="Status"))
        return

    table = Table(title="Student Task Manager", show_header=True)
    table.add_column("#", style="dim", width=4)
    # Fix line 52-53: NO TRAILING WHITESPACE
    table.add_column(
        "Task Description",
        min_width=20
    )
    table.add_column("Status", justify="center")

    for idx, task in enumerate(tasks, 1):
        status = (
            "[green]✅ Done[/green]"
            if task["done"]
            else "[red]⏳ Pending[/red]"
        )
        style = "strike dim" if task["done"] else ""
        table.add_row(
            str(idx),
            task['description'],
            status,
            style=style
        )

    console.print(table)


def add_task(tasks):
    """Add a new task."""
    q = "\n[bold blue]What needs to be done?[/bold blue]"
    desc = Prompt.ask(q)
    if desc:
        tasks.append({"description": desc, "done": False})
        save_tasks(tasks)
        rprint("[bold green]✨ Task added successfully![/bold green]")


def mark_done(tasks):
    """Mark a task as completed."""
    list_tasks(tasks)
    if not tasks:
        return

    msg = "\n[bold magenta]Enter task number[/bold magenta]"
    num = IntPrompt.ask(msg)
    if 1 <= num <= len(tasks):
        tasks[num - 1]["done"] = True
        save_tasks(tasks)
        rprint(
            "[bold green]Check! "
            "Task marked as completed.[/bold green]"
        )


def main():
    """Main application loop."""
    tasks = load_tasks()

    while True:
        list_tasks(tasks)
        menu = (
            "\n[bold]1.[/bold] View "
            "[bold]2.[/bold] Add "
            "[bold]3.[/bold] Complete "
            "[bold]4.[/bold] Exit"
        )
        rprint(menu)

        choice = Prompt.ask(
            "Action",
            choices=["1", "2", "3", "4"],
            default="1"
        )
        if choice == '1':
            list_tasks(tasks)
            input("\nPress Enter to return...")
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            mark_done(tasks)
        elif choice == '4':
            rprint("[italic cyan]Goodbye![/italic cyan]")
            break


if __name__ == "__main__":
    main()
