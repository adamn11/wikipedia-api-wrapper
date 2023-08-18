import sys
import os
# Add the project root to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from datetime import datetime
from src.wiki_wrapper import WikiWrapper, NoDataException
from src.errors import NoDataException


class TestWikiWrapper:
    instance = WikiWrapper()
    article_name = "Albert Einstein"
    article_name_invalid = "wwwwwwwww"
    granularity_week = "week"
    granularity_month = "month"
    granularity_missing = ""
    granularity_invalid = "invalid"
    year = 2018
    month = 10
    day = 10

    def test_get_list_of_most_viewed_articles_month_successful(self):
        result = self.instance.get_list_of_most_viewed_articles_month(self.year, self.month)
        assert result == ['Special:Search', 'Main_Page', 'Special:CreateAccount', '1911_Encyclopædia_Britannica/Bidpai,_Fables_of', 'National_Pledge_(India)', 'special:search', 'Atlas_of_the_World_Battle_Fronts_in_Semimonthly_Phases_to_August_15_1945', 'Special:ElectronPdf', 'Zodiac_Killer_letters', 'The_Rig_Veda']

    def test_get_list_of_most_viewed_articles_week_successful(self):
        result = self.instance.get_list_of_most_viewed_articles_week(self.year, self.month, self.day)
        assert result == ['Special:Search', 'Main_Page', '1911_Encyclopædia_Britannica/Bidpai,_Fables_of', 'The_Rig_Veda', 'special:search', 'Special:CreateAccount', 'National_Pledge_(India)', 'Atlas_of_the_World_Battle_Fronts_in_Semimonthly_Phases_to_August_15_1945', 'Tale_of_Two_Brothers', 'Special:RecentChanges']

    def test_get_list_of_most_viewed_articles_limit(self):
        result = self.instance.get_list_of_most_viewed_articles_month(self.year, self.month, 10)
        assert len(result) == 10

        result = self.instance.get_list_of_most_viewed_articles_month(self.year, self.month, 100)
        assert len(result) == 100

        result = self.instance.get_list_of_most_viewed_articles_month(self.year, self.month, 1000)
        assert len(result) <= 1000  # response returns a length of 994

    def test_get_view_count_of_article_for_week_successful(self):
        result = self.instance.get_view_count_of_article(self.article_name, self.granularity_week, self.year, self.month, self.day)
        assert result == 125837

    def test_get_view_count_of_article_for_month_successful(self):
        result = self.instance.get_view_count_of_article(self.article_name, self.granularity_month, self.year, self.month)
        assert result == 571772

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
