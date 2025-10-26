from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from db import find, save_data
from logger import logger



def scrape_movies():
    try:
        logger.info('Scraping Movies...')
        movies = []

        url = 'https://lk.bookmyshow.com/sri-lanka/movies'

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_selector("div.movie-card-container")

            soup = BeautifulSoup(page.content(), "html.parser")

            # Select all movie card containers
            movie_cards = soup.select("div.movie-card-container")

            # Get Already Added movies
            movies_added = find()

            for card in movie_cards:
                # Extract movie title
                title = card.get("data-title")

                # Extract link
                link_tag = card.find("a", href=True)
                link = f"https://lk.bookmyshow.com{link_tag['href']}" if link_tag else None

                # Extract image
                img_tag = card.find("img", {"class": "__poster"})
                img_src = img_tag.get("data-src") or img_tag.get("src") if img_tag else None
                if img_src and img_src.startswith("//"):
                    img_src = "https:" + img_src

                # Extract languages, genres, and dimensions from data attributes
                language_filter = card.get("data-language-filter", "")
                genre_filter = card.get("data-genre-filter", "")
                dimension_filter = card.get("data-dimension-filter", "")

                languages = [x for x in language_filter.split("|") if x]
                genres = [x for x in genre_filter.split("|") if x]
                dimensions = [x for x in dimension_filter.split("|") if x]

                added_titles = [added_movie["title"] for added_movie in movies_added]

                if title not in added_titles:
                    logger.info(f"Adding New Movie - {title}...")
                    # Append to movies list
                    movies.append({
                        "title": title,
                        "link": link,
                        "languages": languages,
                        "genres": genres,
                        "dimensions": dimensions,
                        "image": img_src
                    })
                else:
                    logger.info(f"Movie {title} already exists.")
                    continue

            browser.close()

            if movies is not None and len(movies) > 0:
                logger.info(f"Saving Movie - {len(movies)} Movies...")
                save_data(movies)
            else:
                logger.info("No new Movies found.")

            return movies

    except Exception as error:
        print(f"❌ Error scraping movies: {error}")
        return []