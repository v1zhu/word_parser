from datetime import date, timedelta
import re
import calendar

WORD_TO_NUM = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}

MONTH_MAP = {
    "january": 1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 8,
    "aug": 8,
    "september": 9,
    "sep": 9,
    "sept": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12,
}

ORDINAL_MAP = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
    "thirtieth": 30,
    "thirtyfirst": 31,
}

WEEKDAY_MAP = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def _parse_number(word: str) -> int | None:
    if word.isdigit():
        return int(word)
    return WORD_TO_NUM.get(word)


def _parse_day(s: str) -> int | None:
    s = s.lower()
    m = re.match(r"(\d{1,2})(?:st|nd|rd|th)?$", s)
    if m:
        return int(m.group(1))
    return ORDINAL_MAP.get(s) or WORD_TO_NUM.get(s)


def _parse_absolute_date(s: str) -> date | None:
    s = s.strip()
    m = re.match(
        r"([a-z]+\.?)\s+((?:\d{1,2}(?:st|nd|rd|th)?|[a-z]+)),?\s*(\d{4})",
        s,
        re.IGNORECASE,
    )
    if m:
        month = MONTH_MAP.get(m.group(1).lower().rstrip("."))
        day = _parse_day(m.group(2))
        if month is not None and day is not None:
            return date(int(m.group(3)), month, day)
    m = re.match(
        r"((?:\d{1,2}(?:st|nd|rd|th)?|[a-z]+))\s+([a-z]+\.?)\s+(\d{4})",
        s,
        re.IGNORECASE,
    )
    if m:
        month = MONTH_MAP.get(m.group(2).lower().rstrip("."))
        day = _parse_day(m.group(1))
        if month is not None and day is not None:
            return date(int(m.group(3)), month, day)
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})$", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})$", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return None


def _parse_offset(s: str) -> tuple[int, int, int]:
    years = months = days = 0
    parts = re.split(r"\s+and\s+", s)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.match(r"(\S+)\s+(year|years|month|months|week|weeks|day|days)", part)
        if not m:
            raise ValueError(f"Invalid offset part: {part}")
        num_str = m.group(1)
        unit = m.group(2)
        num = _parse_number(num_str)
        if num is None:
            raise ValueError(f"Invalid number: {num_str}")
        if unit in ("year", "years"):
            years += num
        elif unit in ("month", "months"):
            months += num
        elif unit in ("week", "weeks"):
            days += num * 7
        elif unit in ("day", "days"):
            days += num
    return years, months, days


def _apply_offset(ref: date, years: int, months: int, days: int, sign: int) -> date:
    years *= sign
    months *= sign
    days *= sign
    total_months = ref.year * 12 + ref.month - 1 + years * 12 + months
    year = total_months // 12
    month = total_months % 12 + 1
    day = min(ref.day, calendar.monthrange(year, month)[1])
    result = date(year, month, day)
    result += timedelta(days=days)
    return result


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s_lower = s.lower().strip()

    m = re.match(
        r"(next|last)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
        s_lower,
    )
    if m:
        direction = m.group(1)
        target = WEEKDAY_MAP[m.group(2)]
        current = today.weekday()
        if direction == "next":
            diff = target - current
            if diff <= 0:
                diff += 7
            return today + timedelta(days=diff)
        else:
            diff = current - target
            if diff < 0:
                diff += 7
            elif diff == 0:
                diff = 7
            return today - timedelta(days=diff)

    if s_lower == "today":
        return today
    if s_lower == "yesterday":
        return today - timedelta(days=1)
    if s_lower == "tomorrow":
        return today + timedelta(days=1)

    if s_lower.startswith("in "):
        offset_str = s_lower[3:]
        years, months, days = _parse_offset(offset_str)
        return _apply_offset(today, years, months, days, 1)

    if s_lower.endswith(" ago"):
        offset_str = s_lower[:-4]
        years, months, days = _parse_offset(offset_str)
        return _apply_offset(today, years, months, days, -1)

    parsed = _parse_absolute_date(s_lower)
    if parsed is not None:
        return parsed

    direction_match = re.search(r"\b(after|before|from)\b", s_lower)
    if not direction_match:
        raise ValueError(f"Invalid input: {s}")

    direction_word = direction_match.group(1)
    offset_str = s_lower[: direction_match.start()].strip()
    ref_str = s_lower[direction_match.end() :].strip()

    sign = 1 if direction_word in ("after", "from") else -1

    if ref_str == "today":
        ref_date = today
    elif ref_str == "yesterday":
        ref_date = today - timedelta(days=1)
    elif ref_str == "tomorrow":
        ref_date = today + timedelta(days=1)
    else:
        parsed = _parse_absolute_date(ref_str)
        if parsed is None:
            raise ValueError(f"Invalid reference: {ref_str}")
        ref_date = parsed

    years, months, days = _parse_offset(offset_str)
    return _apply_offset(ref_date, years, months, days, sign)
