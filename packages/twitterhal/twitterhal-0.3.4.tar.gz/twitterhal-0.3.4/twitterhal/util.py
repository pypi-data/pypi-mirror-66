import datetime
import html
import re
from typing import TYPE_CHECKING

import emoji
from megahal.util import split_to_sentences


if TYPE_CHECKING:
    from typing import List, Pattern


emoji_pattern: "Pattern[str]" = emoji.get_emoji_regexp()
url_pattern = re.compile(
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
    flags=re.IGNORECASE
)


def strip_phrase(phrase: str) -> str:
    # Strip emojis
    phrase = emoji_pattern.sub("", phrase)
    # Unescape HTML entities
    phrase = html.unescape(phrase)
    # Strip URLs and mentions
    phrase = url_pattern.sub("", phrase)
    phrase = re.sub(r"@\w+", "", phrase)
    # Strip hashtags
    phrase = re.sub(r"#\w+", "", phrase)
    # Strip quotation marks
    phrase = re.sub(r"[”\"]", "", phrase)
    # Strip lines, stars & dots
    phrase = re.sub(r"\s*[|•*]\s*", " ", phrase)
    # Remote "RT : ", denoting retweet (it used to be a @handle there before
    # we stripped it above)
    phrase = re.sub(r"^rt : ", "", phrase, flags=re.IGNORECASE)
    # Convert non-space whitespace (\n, \t etc) to space
    phrase = re.sub(r"\s", " ", phrase)
    # Strip superfluous whitespace
    phrase = re.sub(r"\s{2,}", " ", phrase)
    # Remove trailing ellipsis + sentence that might have been cut off with it
    try:
        if phrase.strip()[-1] == "…":
            phrase = " ".join(split_to_sentences(phrase)[:-1])
    except IndexError:
        pass
    return phrase.strip()


def parse_time_string_list(string: str) -> "List[datetime.time]":
    result = []
    times = re.split(r",\s*", string)
    for t in times:
        try:
            result.append(datetime.datetime.strptime(t, "%H:%M:%S").time())
        except ValueError:
            result.append(datetime.datetime.strptime(t, "%H:%M").time())
    return result
