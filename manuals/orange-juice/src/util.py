from typing import Optional


def plural(
    count: int,
    singular_word: str,
    plural_word: Optional[str] = None,
    template: str = "{count} {word}",
):
    plural_word = plural_word or (singular_word + "s")
    return template.replace("{count}", str(count)).replace(
        "{word}", singular_word if count == 1 else plural_word
    )
