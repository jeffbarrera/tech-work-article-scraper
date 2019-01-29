# tech-work-article-scraper
News article content scraper for the WPUSA-UC Berkeley Labor Center Future of Work project

When we switched to Evernote for an article-tracking project, we needed to import a bunch of bookmarks from an old system. However, the old bookmarks didn't contain the full text of the articles, which meant we couldn't use Evernote's text search feature (very useful for finding articles where you remember some detail but not the title).

To solve this, I wrote a quick script to scrape the article content using the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and [Newspaper](https://github.com/codelucas/newspaper) libraries.