# Wikipedia API Wrapper Application
This is a wrapper around Wikipedia's PageView API with the following endpoints:
- Retrieves a list of the most viewed articles for a week or month
- Retrieves the view count for an article for a specified week or month
- Retrieve the day of the month where an article got the most page views

## Project Assumptions
- This project is using articles from **en.wikipedia** only
- Access type is **all-access** (view counts are spread across desktop, mobile-app, and mobile-web)
- Agent type is **user** for per-article requests
- Using coolbot as the user-agent

## Installation
You can install this package by using pip

`pip install wiki-api-wrapper`

## Getting Started
To start using this package, you need to import wiki-api-wrapper and then instantiate an instance of `WikiWrapper()`
```
import wiki-api-wrapper

wiki = WikiWrapper()
```

## Examples

### Get a list of the most viewed articles for the month of `October 2018`
```
wiki.get_list_of_most_viewed_articles_month(2022, 10)
```
Which should return a list like the one below
```
['Special:Search', 'Main_Page', 'Special:CreateAccount', '1911_Encyclopædia_Britannica/Bidpai,_Fables_of', 'National_Pledge_(India)', 'special:search', 'Atlas_of_the_World_Battle_Fronts_in_Semimonthly_Phases_to_August_15_1945', 'Special:ElectronPdf', 'Zodiac_Killer_letters', 'The_Rig_Veda']
```

### Get the view count for `Albert Einstein` for the month of `April 2022`
```
wiki.get_view_count_of_article("Albert Einstein", "month", 2022, 4)
```
Should return an int of `385712`

### Get the date where the page for `Albert Einstein` got the most views
```
wiki.get_article_date_with_most_views("Albert Einstein")
```

Should return a datetime of `2018-03-14 00:00:00`

## Endpoint Documentation
[Link to Docs](https://github.com/adamn11/wikipedia-api-wrapper/blob/main/docs/endpoints.md)


