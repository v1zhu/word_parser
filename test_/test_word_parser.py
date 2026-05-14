import parser

def test_using_words_like_week():
    assert parser.word_parser(s = 'two weeks from today', today = parser.date(2023, 10, 6)) == parser.date(2023, 10, 20)

def test_using_numbers():
    assert parser.word_parser(s = '5 days before December 1st, 2025', today = parser.date(2023, 10, 6)) == parser.date(2025, 11, 26)

def test_using_year_and_month():
    assert parser.word_parser(s = "1 year and 2 months after yesterday", today = parser.date(2023, 10, 6)) == parser.date(2024, 12, 5)

def test_next_tuesday():
    assert parser.word_parser(s = "next Tuesday", today = parser.date(2023, 10, 6)) == parser.date(2023, 10, 10)

def test_last_friday():
    assert parser.word_parser(s = "last Friday", today = parser.date(2023, 10, 6)) == parser.date(2023, 9, 29)

def test_no_input_date():
    assert parser.word_parser(s = "three days from today") == parser.date.today() + parser.timedelta(days=3)

def test_invalid_input():
    try:
        parser.word_parser(s = "invalid input", today = parser.date(2023, 10, 6))
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid input")

def test_leap_year():
    assert parser.word_parser(s = "one day after February 28th, 2024", today = parser.date(2023, 10, 6)) == parser.date(2024, 2, 29)

def test_end_of_month():
    assert parser.word_parser(s = "two days after January 30th, 2024", today = parser.date(2023, 10, 6)) == parser.date(2024, 2, 1)

def test_end_of_year():
    assert parser.word_parser(s = "three days before January 1st, 2025", today = parser.date(2023, 10, 6)) == parser.date(2024, 12, 29)

def test_month_boundary_day_clamping():
    assert parser.word_parser("one month after January 31st, 2024", today=parser.date(2023, 10, 6)) == parser.date(2024, 2, 29)

def test_before_yesterday():
    assert parser.word_parser("one day before yesterday", today=parser.date(2023, 10, 6)) == parser.date(2023, 10, 4)

def test_twenty_days():
    assert parser.word_parser("twenty days from today", today=parser.date(2023, 10, 6)) == parser.date(2023, 10, 26)