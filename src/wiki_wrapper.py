'''
Wikipedia's API Rules
1. Limit client requests to NO MORE than 200 requests per second
2. Set a unique User-Agent or Api-User-Agent (DONE)

Project Assumptions
- Project = en.wikipedia
- Web app counts only
- Using all-agents
- Using coolbot for user-agent

Notes:
- Article name is case sensitive. Barack Obama, Barack obama, barack obama will all return different results
'''
import requests
from datetime import datetime, timedelta


class NoDataException(Exception):
    "Raised when there are no data or the data has not been loaded yet"
    pass


class ThrottlingException(Exception):
    "Raised when the client has made too many requests and it is being throttled"
    pass


class WikiWrapper:
    def __init__(self):
        self.user_agent_headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
        self.per_article_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/daily/{start_date}/{end_date}"
        self.top_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikisource/all-access/{year}/{month:02d}/{day:02d}"

    def get_list_of_most_viewed_articles(self, granularity: str, year: int, month: int, day: int=1, limit: int=10):
        self.__validate_dates(year, month, day)
        if granularity.lower() not in ["week", "month"]:
            raise Exception("Granularity input is incorrect. Only 'week' or 'month' values are accepted.")
        # TODO: have each return their own dataset
        if granularity.lower() == "month":
            data = self.__get_most_viewed_month(year, month)
            top_articles = [d.get("article") for d in data]
            return top_articles[:limit]
        elif granularity.lower() == "week":
            start_date = datetime(year, month, day)
            data = self.__get_most_viewed_week(start_date)
            # return

    def __get_most_viewed_month(self, year, month):
        url = self.top_url.format(year=year,
                                  month=month,
                                  day='all-days')
        request = self.__get_api_results(url)
        most_viewed_month = request[0].get("articles")
        return most_viewed_month

    def __get_most_viewed_week(self, start_date):
        most_viewed_week = {}
        date = start_date

        for _ in range(7):
            url = self.top_url.format(year=date.year,
                                      month=date.month,
                                      day=date.day)
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

        # TODO: need to combine duplicate results into one entry then sort
        sorted_items = dict(sorted(most_viewed_week.items(), key=lambda item: item[1], reverse=True))
        return sorted_items

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

    def get_article_date_with_most_views(self, article_name: str) -> datetime:
        # The Wikimedia pageviews API has backfilled data to July 2015
        start_date = "2015070100"
        end_date = datetime.today().strftime("%Y%m%d00")
        article = self.__get_valid_article_name(article_name)

        url = self.per_article_url.format(article=article,
                                          start_date=start_date,
                                          end_date=end_date)
        data = self.__get_api_results(url)
        max_view = max(data, key=lambda views: views.get('views'))

        # Formatting timestamp returned from pageview API
        max_view_date = max_view.get("timestamp")
        formatted_date = datetime.strptime(max_view_date, "%Y%m%d%H")

        return formatted_date

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
        # I calculate the end of the month by getting the first day of next month and substracting 1 day
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


# driver code (remove in final code)
ww = WikiWrapper()
print(ww.get_article_date_with_most_views("Albert Einstein"))
