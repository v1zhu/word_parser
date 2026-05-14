import parser

def test_using_words_like_week():
    assert parser.construct_feedback(s = 'two weeks from today', today = parser.date(2023, 10, 6)) == parser.date(2023, 10, 20)

def test_using_numbers():
    assert parser.construct_feedback(s = '5 days before December 1st, 2025', today = parser.date(2023, 10, 6)) == parser.date(2025, 11, 26)
    
def test_using_year_and_month():
    assert parser.construct_feedback(s = "1 year and 2 months after yesterday", today = parser.date(2023, 10, 6)) == parser.date(2025, 12, 5)

def test_next_tuesday():
    assert parser.construct_feedback(s = "next Tuesday", today = parser.date(2023, 10, 6)) == parser.date(2023, 10, 10)
    2023-10-10