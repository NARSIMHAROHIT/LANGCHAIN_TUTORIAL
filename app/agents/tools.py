from typing import Annotated
import re

import httpx
from bs4 import BeautifulSoup
from langchain_core.tools import tool

from dataclasses import dataclass
#------------
# LOW-LEVEL WEB READER
# -----------------------------

def _fetch_and_extract_text(url: str) -> str:
    """
    Fetch a webpage and extract readable text.
    No reasoning, no guarantees, no citations.
    """
    with httpx.Client(timeout=10.0, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove non-content elements
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()

    return text


# -----------------------------
# TOOLS
# -----------------------------

@tool
def read_linux_documentation(
    command: Annotated[str, "Linux command name, e.g. ls, grep, systemctl"]
) -> str:
    """
    Read official Linux documentation pages and return raw extracted text.
    """
    urls = [
        f"https://man7.org/linux/man-pages/man1/{command}.1.html"
    ]

    combined_text = []

    for url in urls:
        try:
            text = _fetch_and_extract_text(url)
            if text:
                combined_text.append(text[:3000])  # safety cap
        except Exception:
            continue

    return "\n".join(combined_text)


@tool
def read_systemd_documentation(
    command: Annotated[str, "systemd command name"]
) -> str:
    """
    Read systemd documentation pages and return raw extracted text.
    """
    url = f"https://www.freedesktop.org/software/systemd/man/{command}.html"

    try:
        text = _fetch_and_extract_text(url)
        return text[:3000]
    except Exception:
        return ""


@tool
def read_generic_web_document(
    url: Annotated[str, "Documentation URL to read"]
) -> str:
    """
    Read any documentation webpage and return raw extracted text.
    """
    try:
        text = _fetch_and_extract_text(url)
        return text[:3000]
    except Exception:
        return ""
@tool
def execute_command(command: str, sudo: bool = False) -> str:
    """
    Execution is disabled.
    """
    return "Execution is disabled in documentation-only mode."

from dataclasses import dataclass

@dataclass
class Context:
    user_id: str
