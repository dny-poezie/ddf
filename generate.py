#!/usr/bin/env python3

"""Script that generates index.html

No Jinja2 because script dependencies suck.
"""

import datetime
import json
import sys
from pathlib import Path

SOURCE = Path("source.json")
TARGET = Path("index.html")
TEMPLATE = Path("index.html.template")


def format_timestamp(timestamp: datetime.datetime) -> str:
    """Translate timestamp to Czech-formatted date."""
    # Some systems do not have cs_CZ.UTF_8 locale available
    day: str = (
        "Pondělí",
        "Úterý",
        "Středa",
        "Čtvrtek",
        "Pátek",
        "Sobota",
        "Neděle",
    )[timestamp.weekday()]
    return f"{day} {timestamp.strftime('%-d. %-m., %H:%M')}"


def generate_event(event: dict) -> str:
    """Convert event dictionary into HTML"""
    try:
        timestamp = datetime.datetime.strptime(event["date"], "%Y-%m-%d %H:%M")

        result = r"""
        <div class='event' timestamp='{timestamp}'>
            <p class='title'>{title} &mdash; {author}
                <a href='{link}' alt='Facebook'><img src='facebook.svg' /></a>
            </p>
            <p class='when'>{date} {time} {place}</p>
            <p class='description'>{description}</p>
        </div>
        """

        result = result.format(
            timestamp=timestamp.strftime("%Y-%m-%d"),
            title=event["title"],
            author=", ".join(event["authors"]),
            link=event["facebook"],
            date=timestamp.strftime("%-d. %-m."),
            time=timestamp.strftime("%H:%M"),
            place=event["place"],
            description="<br>".join(event["description"]),
        )
        return result
    except Exception as exc:
        print(f"Skipping {event=}: {exc=}", file=sys.stderr)
        return ""


def generate():
    """Fill in a template with JSON data."""
    with TEMPLATE.open("r") as f:
        template = f.read()

    with SOURCE.open("r") as f:
        source = json.load(f)

    index = template
    index = (
        index.replace("{{title}}", source["title"])
        .replace("{{year}}", source["year"])
        .replace("{{facebook}}", source["facebook"])
        .replace("{{contact}}", source["contact"])
        .replace(
            "{{events}}", "\n".join(generate_event(d) for d in source["events"])
        )
    )

    with TARGET.open("w") as f:
        f.write(index)


if __name__ == "__main__":
    generate()
