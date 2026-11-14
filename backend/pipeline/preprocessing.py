
import html
import re


def clean_text(raw: str | None) -> str:
    """
    Clean article text while preserving meaningful information.
    """

    if not raw:
        return ""

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", raw)

    # Decode HTML entities such as &amp; and &nbsp;
    text = html.unescape(text)

    # Normalize multiple spaces and line breaks
    text = re.sub(r"\s+", " ", text)

    # Remove spaces at the beginning and end
    text = text.strip()

    return text
