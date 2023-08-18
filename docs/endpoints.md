# Wiki Wrapper Endpoint Documentation

# Table of Content
1. [Get Article Date With Most Views](#get-article-date-with-most-views)
2. [Get View Count of Article](#get-view-count-of-article)
3. [Get List of Most Viewed Articles for a Month](#get-list-of-most-viewed-articles-for-a-month)
4. [Get List of Most Viewed Articles for a Week](#get-list-of-most-viewed-articles-for-a-week)
5. [Status Codes](#status-codes)

## Get Article Date With Most Views
By provoding an article name, this endpoint will return a date when that article got the most views

### Parameters
- `article_name` (string, required): The wiki page/subject

### Response
Response is of type datetime in the format of `YYYY-MM-DD hours:minutes:seconds` where the specified article has the most views. Note that PageView's API backfills to 2015 so any information requsted before that will return a 404 error.

### Example
```
# Get the date where Albert Einstein had the most views

wiki = WikiWrapper()
print(wiki.get_article_date_with_most_views("Albert Einstein"))
```
### Example Response
```
2018-03-14 00:00:00
```

## Get View Count of Article
By providing an article name as well as a date, this endpoint will return the view count of that article for the speicified date

### Parameters
- `article_name` (string, required): The wiki page/subject
- `granularity` (string, required): The value of either "week" or "month"
- `year` (integer, required): The year the user is looking for
- `month` (integer, required): The month the user is looking for
- `day` (integer, optional, default=1): The day the user is looking for

### Response
Response is an integer of the view counts that article has during the specified period

### Example
```
# Get the view count for Albert Einstein for the month of October 2022

wiki = WikiWrapper()
print(wiki.get_view_count_of_article("Albert Einstein", "month", 2022, 10))
```

### Example Repsonse
```
493091
```

## Get List of Most Viewed Articles for a Week
This endpoint will return a list of the most viewed articles for the specified period

### Parameters
- `year` (integer, required): The year the user is looking for
- `month` (integer, required): The month the user is looking for
- `day` (integer, optional, default=1): The day the user is looking for
- `limit` (integer, optional, default=10): The limit on how many articles the user wants to see

### Response
Response is a list of strings with the most viewed articles during the specified week

### Example
```
# Gets a list of the most viewed articles during the week of October 10th, 2022, with a limit of 5 articles

wiki = WikiWrapper()
print(wiki.get_list_of_most_viewed_articles_week(2022, 10, 10, 5))
```

### Example Response
```
['Main_Page', 'Special:Search', 'Constitution_of_the_Republic_of_South_Africa,_1996', 'Dictionary_of_spoken_Spanish', 'Category:Proofread']
```

## Get List of Most Viewed Articles for a Month

### Parameters
- `year` (integer, required): The year the user is looking for
- `month` (integer, required): The month the user is looking for
- `limit` (integer, optional, default=10): The limit on how many articles the user wants to see

### Response
Response is a list of strings with the most viewed articles during the specified month

### Example
```
# Gets a list of the most viewed articles during the month of October 2022, with a limit of 5 articles

wiki = WikiWrapper()
print(wiki.get_list_of_most_viewed_articles_month(2022, 10, 10, 5))
```

### Example Response
```
['Main_Page', 'Special:Search', 'Constitution_of_the_Republic_of_South_Africa,_1996', 'Dictionary_of_spoken_Spanish', 'Category:Proofread']
```

# Status Codes
When sending a request to PageView, you may receive the following status codes:
- **200**: Successful request and should return a response
- **404**: Either no data exists for the page you are looking for or the data has not been loaded yet
- **429**: You have made too many requests and are currently being throttled
