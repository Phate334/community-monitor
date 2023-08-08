from datetime import datetime, timedelta

import arxiv
import meilisearch
from loguru import logger
from rocketry import Rocketry
from rocketry.args import Return
from rocketry.conds import after_success

from monitor.config import get_settings
from monitor.models.arxiv import ArxivArticle

settings = get_settings()
app = Rocketry()
logger.add("daily-job.log", backtrace=True, diagnose=True)

# Define an array of categories to search for
categories = ["cs.AI"]


@app.task("daily after 10:00")
def fetch_arxiv():
    articles = []
    today = datetime.today() - timedelta(days=2)  # UTC-5 timezone
    yesterday = today - timedelta(days=1)
    for category in categories:
        search = arxiv.Search(
            query=f"cat:{category} AND submittedDate:[{yesterday.strftime('%Y%m%d')} TO {today.strftime('%Y%m%d')}]",
            max_results=float("inf"),
        )
        for result in search.results():
            articles.append(
                ArxivArticle(
                    id=result.entry_id.split("/")[-1].replace(".", "-"),
                    arxiv_id=result.entry_id.split("/")[-1],
                    published=result.published.timestamp(),
                    title=result.title,
                    summary=result.summary.replace("\n", " "),
                    primary_category=result.primary_category,
                    tags=result.categories,
                )
            )

    return articles


@app.task(after_success(fetch_arxiv))
def upload_articles(articles=Return(fetch_arxiv)):
    logger.info("Uploading {} articles", len(articles))
    if not articles:
        return
    client = meilisearch.Client(settings.meilisearch_url, settings.meilisearch_api_key)
    index = client.index("arxiv")
    index.add_documents([article.dict() for article in articles])


if __name__ == "__main__":
    app.run()