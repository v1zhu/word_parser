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
