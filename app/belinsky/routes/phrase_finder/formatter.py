"""Format phrase finder outputs."""


def bold_phrases(
    text: str, phrases: dict[str, list[list[int]]], tag: str = "<b>"
) -> str:
    """Highlight found phrases using <br> html tags.

    Args:
        text (str): Original text.
        phrases (list[list[int]]): Found phrases.
        tag (str): Tag to be added on found phrases.

    Returns:
        str:
            Formatted text
    """

    formatted_text = ""
    old_end = 0
    phrases = sum(phrases.values(), [])
    phrases.sort(key=lambda x: x[0])
    for start, end in phrases:
        end += 1
        formatted_text += text[old_end:start]
        formatted_text += tag
        formatted_text += text[start:end]
        formatted_text += tag[0] + "/" + tag[1:]
        old_end = end
    formatted_text += text[old_end:]

    return formatted_text
