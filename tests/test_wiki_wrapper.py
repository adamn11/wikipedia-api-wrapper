import sys
import os
# Add the project root to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from datetime import datetime
from src.wiki_wrapper import WikiWrapper, NoDataException


class TestWikiWrapper:
    instance = WikiWrapper()
    article_name = "Albert Einstein"
    article_name_invalid = "wwwwwwwww"
    granularity_week = "week"
    granularity_month = "month"
    granularity_missing = ""
    granularity_invalid = "invalid"
    year = 2016
    month = 10
    day = 10

    def test_get_view_count_of_article_for_week_successful(self):
        result = self.instance.get_view_count_of_article(self.article_name, self.granularity_week, self.year, self.month, self.day)
        assert result == 148013

    def test_get_view_count_of_article_for_month_successful(self):
        result = self.instance.get_view_count_of_article(self.article_name, self.granularity_month, self.year, self.month)
        assert result == 616742

    def test_get_view_count_of_article_invalid_article_name(self):
        with pytest.raises(NoDataException) as e_info:
            self.instance.get_view_count_of_article(self.article_name_invalid, self.granularity_month, self.year, self.month)
        assert str(e_info.value) == "There are no data or the data has not been loaded yet"

    def test_get_view_count_of_article_missing_granularity(self):
        with pytest.raises(Exception) as e_info:
            self.instance.get_view_count_of_article(self.article_name, self.granularity_missing, self.year, self.month)
        print(e_info.value)
        assert str(e_info.value) == "Granularity input is incorrect. Week or Month value are only accepted."

    def test_get_view_count_of_article_invalid_granularity(self):
        with pytest.raises(Exception) as e_info:
            self.instance.get_view_count_of_article(self.article_name, self.granularity_invalid, self.year, self.month)
        assert str(e_info.value) == "Granularity input is incorrect. Week or Month value are only accepted."

    def test_get_api_results_404_exception(self):
        # This requests data from before pageview API's backfill in 2015. Should return a 404 error
        year = 2012
        with pytest.raises(NoDataException) as e_info:
            self.instance.get_view_count_of_article(self.article_name, self.granularity_month, year, self.month)
        assert str(e_info.value) == "There are no data or the data has not been loaded yet"

    def test_invalid_dates(self):
        # Test invalid year
        invalid_year = -1000
        with pytest.raises(ValueError) as e_info:
            self.instance.get_view_count_of_article(self.article_name, self.granularity_week, invalid_year, self.month, self.day)
        assert str(e_info.value) == f"year {invalid_year} is out of range"

        # Test invalid month
        invalid_month = 14
        with pytest.raises(ValueError) as e_info:
            self.instance.get_view_count_of_article(self.article_name, self.granularity_week, self.year, invalid_month, self.day)
        assert str(e_info.value) == f"month must be in 1..12"

        # Test invalid day
        invalid_day = 100
        with pytest.raises(ValueError) as e_info:
            self.instance.get_view_count_of_article(self.article_name, self.granularity_week, self.year, self.month, invalid_day)
        assert str(e_info.value) == f"day is out of range for month"

    def test_get_article_date_with_most_views(self):
        result = self.instance.get_article_date_with_most_views(self.article_name)
        assert result == datetime(2018, 3, 14, 0, 0)

    def test_get_article_date_with_most_views_empty_article_name(self):
        article_name = ""
        with pytest.raises(ValueError) as e_info:
            self.instance.get_article_date_with_most_views(article_name)
        assert str(e_info.value) == "Article name is required."

    def test_get_article_date_with_most_views_invalid_article(self):
        with pytest.raises(NoDataException) as e_info:
            self.instance.get_article_date_with_most_views(self.article_name_invalid)
        assert str(e_info.value) == "There are no data or the data has not been loaded yet"
