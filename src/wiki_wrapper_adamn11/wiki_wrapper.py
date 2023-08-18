import sys
import os
# Add the project root to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from datetime import datetime, timedelta
from src.errors import NoDataException, ThrottlingException


class WikiWrapper:
    def __init__(self):
        self.user_agent_headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
        self.per_article_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/daily/{start_date}/{end_date}"
        self.top_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikisource/all-access/{year}/{month:02d}/{day}"

    def get_article_date_with_most_views(self, article_name: str) -> datetime:
        # The Wikimedia pageviews API has backfilled data to July 2015
        start_date = "2015070100"
        end_date = datetime.today().strftime("%Y%m%d00")
        article = self.__get_valid_article_name(article_name)

        url = self.per_article_url.format(article=article,
                                          start_date=start_date,
                                          end_date=end_date)
        data = self.__get_api_results(url)
        max_views = max(data, key=lambda views: views.get('views'))

        # Formatting timestamp returned from pageview API
        max_view_date = max_views.get("timestamp")
        formatted_date = datetime.strptime(max_view_date, "%Y%m%d%H")

        return formatted_date

    def get_view_count_of_article(self, article_name: str, granularity: str, year: int, month: int, day: int=1) -> int:
        self.__validate_dates(year, month, day)
        if granularity.lower() not in ["week", "month"]:
            raise Exception("Granularity input is incorrect. Week or Month value are only accepted.")
        if granularity.lower() == "month":
            dates = self.__get_month_dates(month, year)
        elif granularity.lower() == "week":
            dates = self.__get_week_dates(day, month, year)
        start, end = dates[0], dates[1]

        article = self.__get_valid_article_name(article_name)

        url = self.per_article_url.format(article=article,
                                          start_date=start,
                                          end_date=end)
        data = self.__get_api_results(url)

        total_view_count = 0
        for d in data:
            total_view_count += d.get('views')

        return total_view_count

    def get_list_of_most_viewed_articles_week(self, year: int, month: int, day: int=1, limit: int=10):
        self.__validate_dates(year, month, day)
        date = datetime(year, month, day)

        most_viewed_week = {}
        for _ in range(7):
            url = self.top_url.format(year=date.year,
                                      month=date.month,
                                      day='{:02d}'.format(date.day))
            request = self.__get_api_results(url)
            most_viewed_articles = request[0].get("articles")

            for article in most_viewed_articles:
                article_name = article.get("article")
                views = article.get("views")

                if article_name in most_viewed_week:
                    most_viewed_week[article_name] += views
                else:
                    most_viewed_week[article_name] = views

            date = date + timedelta(days=1)

        sorted_by_views = sorted(most_viewed_week.items(), key=lambda item: item[1], reverse=True)
        # This is to ensure that the limit does not exceed the length of response
        limit = limit if limit < len(sorted_by_views) else len(sorted_by_views)
        top_articles_week = [sorted_by_views[i][0] for i in range(limit)]

        return top_articles_week

    def get_list_of_most_viewed_articles_month(self, year: int, month: int, limit: int=10):
        self.__validate_dates(year, month)

        url = self.top_url.format(year=year,
                                  month=month,
                                  day='all-days')
        request = self.__get_api_results(url)
        most_viewed_month = request[0].get("articles")

        # This is to ensure that the limit does not exceed the length of response
        limit = limit if limit < len(most_viewed_month) else len(most_viewed_month)
        top_articles_month = [most_viewed_month[i].get("article") for i in range(limit)]

        return top_articles_month

    def __get_api_results(self, api_url: str):
        request = requests.get(api_url, headers=self.user_agent_headers)

        if request.status_code == 200:
            return request.json()["items"]
        elif request.status_code == 404:
            raise NoDataException("There are no data or the data has not been loaded yet")
        elif request.status_code == 429:
            raise ThrottlingException("Client has made too many requests")

    def __validate_dates(self, year: int, month: int, day: int = 1):
        try:
            datetime(year=year, month=month, day=day)
        except ValueError:
            return ValueError

    def __get_week_dates(self, day: int, month: int, year: int):
        date_object = datetime(year, month, day)
        start_of_week = date_object - timedelta(days=date_object.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return [start_of_week.strftime("%Y%m%d00"), end_of_week.strftime("%Y%m%d00")]

    def __get_month_dates(self, month: int, year: int):
        start_of_month = datetime(year, month, 1)
        # End of the month is calculated by getting the first day of next month and substracting 1 day
        next_month = start_of_month.replace(day=28) +timedelta(days=4)
        end_of_month = next_month - timedelta(days=next_month.day)
        return [start_of_month.strftime("%Y%m%d00"), end_of_month.strftime("%Y%m%d00")]

    def __get_valid_article_name(self, article: str) -> str:
        if article == "":
            raise ValueError("Article name is required.")

        # Converts article name to snake case
        words = article.split()
        snake_case_string = '_'.join(words)
        return snake_case_string
