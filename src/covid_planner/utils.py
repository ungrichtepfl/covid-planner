import emoji

__all__ = ["emoji_print"]


def emoji_print(s: str):
    print(emoji.emojize(s))
