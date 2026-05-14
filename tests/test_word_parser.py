from nldate import parse, date, timedelta


def test_using_words_like_week():
    assert parse(s="two weeks from today", today=date(2023, 10, 6)) == date(
        2023, 10, 20
    )


def test_using_numbers():
    assert parse(s="5 days before December 1st, 2025", today=date(2023, 10, 6)) == date(
        2025, 11, 26
    )


def test_using_year_and_month():
    assert parse(
        s="1 year and 2 months after yesterday", today=date(2023, 10, 6)
    ) == date(2024, 12, 5)


def test_next_tuesday():
    assert parse(s="next Tuesday", today=date(2023, 10, 6)) == date(2023, 10, 10)


def test_last_friday():
    assert parse(s="last Friday", today=date(2023, 10, 6)) == date(2023, 9, 29)


def test_no_input_date():
    assert parse(s="three days from today") == date.today() + timedelta(days=3)


def test_invalid_input():
    try:
        parse(s="invalid input", today=date(2023, 10, 6))
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid input")


def test_leap_year():
    assert parse(
        s="one day after February 28th, 2024", today=date(2023, 10, 6)
    ) == date(2024, 2, 29)


def test_end_of_month():
    assert parse(
        s="two days after January 30th, 2024", today=date(2023, 10, 6)
    ) == date(2024, 2, 1)


def test_end_of_year():
    assert parse(
        s="three days before January 1st, 2025", today=date(2023, 10, 6)
    ) == date(2024, 12, 29)


def test_month_boundary_day_clamping():
    assert parse("one month after January 31st, 2024", today=date(2023, 10, 6)) == date(
        2024, 2, 29
    )


def test_before_yesterday():
    assert parse("one day before yesterday", today=date(2023, 10, 6)) == date(
        2023, 10, 4
    )


def test_twenty_days():
    assert parse("twenty days from today", today=date(2023, 10, 6)) == date(
        2023, 10, 26
    )


def test_iso_date_after():
    assert parse("one day after 2024-03-15", today=date(2023, 10, 6)) == date(
        2024, 3, 16
    )


def test_iso_date_before():
    assert parse("5 days before 2025-01-10", today=date(2023, 10, 6)) == date(
        2025, 1, 5
    )


def test_iso_date_from():
    assert parse("two weeks from 2024-06-01", today=date(2023, 10, 6)) == date(
        2024, 6, 15
    )


def test_standalone_iso_date():
    assert parse("2025-02-01", today=date(2023, 10, 6)) == date(2025, 2, 1)


def test_slash_date_yyyy_mm_dd():
    assert parse("2025/12/04", today=date(2023, 10, 6)) == date(2025, 12, 4)


def test_slash_date_dd_mm_yyyy():
    assert parse("04/12/2025", today=date(2023, 10, 6)) == date(2025, 12, 4)


def test_day_month_word_yyyy():
    assert parse("15 January 2024", today=date(2023, 10, 6)) == date(2024, 1, 15)


def test_slash_date_in_offset():
    assert parse("three days after 2025/11/20", today=date(2023, 10, 6)) == date(
        2025, 11, 23
    )


def test_day_month_word_in_offset():
    assert parse("one week before 15 December 2025", today=date(2023, 10, 6)) == date(
        2025, 12, 8
    )


def test_non_padded_slash_day():
    assert parse("2025/12/3", today=date(2023, 10, 6)) == date(2025, 12, 3)


def test_non_padded_slash_month():
    assert parse("2025/1/15", today=date(2023, 10, 6)) == date(2025, 1, 15)


def test_non_padded_dd_mm_yyyy():
    assert parse("3/12/2025", today=date(2023, 10, 6)) == date(2025, 12, 3)


def test_non_padded_iso():
    assert parse("2025-1-5", today=date(2023, 10, 6)) == date(2025, 1, 5)


def test_non_padded_in_offset():
    assert parse("two days after 2025/12/3", today=date(2023, 10, 6)) == date(
        2025, 12, 5
    )


def test_abbrev_month_standalone():
    assert parse("Dec 1, 2025", today=date(2023, 10, 6)) == date(2025, 12, 1)


def test_abbrev_month_padded():
    assert parse("Dec 01, 2025", today=date(2023, 10, 6)) == date(2025, 12, 1)


def test_abbrev_month_no_comma():
    assert parse("Jan 15 2024", today=date(2023, 10, 6)) == date(2024, 1, 15)


def test_abbrev_month_in_offset():
    assert parse("three days after Dec 1, 2025", today=date(2023, 10, 6)) == date(
        2025, 12, 4
    )


def test_word_day_month_first():
    assert parse("December first, 2025", today=date(2023, 10, 6)) == date(2025, 12, 1)


def test_word_day_month_second():
    assert parse("January second 2024", today=date(2023, 10, 6)) == date(2024, 1, 2)


def test_word_day_before_month():
    assert parse("fifteenth March 2024", today=date(2023, 10, 6)) == date(2024, 3, 15)


def test_word_day_in_offset():
    assert parse("one day after December first, 2025", today=date(2023, 10, 6)) == date(
        2025, 12, 2
    )


def test_word_day_case_insensitive():
    assert parse("DECEMBER FIRST, 2025", today=date(2023, 10, 6)) == date(2025, 12, 1)


def test_dotted_abbrev_month():
    assert parse("Dec. 1, 2025", today=date(2023, 10, 6)) == date(2025, 12, 1)


def test_dotted_abbrev_month_day_before():
    assert parse("1 Jan. 2025", today=date(2023, 10, 6)) == date(2025, 1, 1)


def test_dotted_abbrev_month_in_offset():
    assert parse("two days after Dec. 15, 2025", today=date(2023, 10, 6)) == date(
        2025, 12, 17
    )


def test_standalone_today():
    assert parse("today", today=date(2023, 10, 6)) == date(2023, 10, 6)


def test_standalone_yesterday():
    assert parse("yesterday", today=date(2023, 10, 6)) == date(2023, 10, 5)


def test_standalone_tomorrow():
    assert parse("tomorrow", today=date(2023, 10, 6)) == date(2023, 10, 7)
