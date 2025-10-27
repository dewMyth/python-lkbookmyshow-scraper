from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Error
from db import find, save_data
from logger import logger



def scrape_movies():
    try:
        logger.info('Scraping Movies...')
        movies = []


        url = 'http://www.scopecinemas.com/movies'
        #url = 'https://lk.bookmyshow.com/movies'

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            #page.goto(url)
            #page.wait_for_selector("div.movie-card-container")


            try:
                response = page.goto(url, timeout=120000)

                if response is None:
                    logger.error(f"Navigation failed: No response received. Possible network issue for URL: {url}")
                elif response.status >= 400:
                    logger.error(f"HTTP Error {response.status} for URL: {url}")
                else:
                    try:
                        page.wait_for_selector("div.movie-card-container", timeout=10000)
                        logger.info("Page loaded and selector found successfully.")
                    except TimeoutError:
                        logger.error(f"Selector not found on page within timeout for URL: {url}")

            except Error as e:  # Playwright network or navigation errors
                logger.error(f"Network or navigation error occurred: {e}")
            except Exception as e:  # Catch-all for any other unexpected errors
                logger.error(f"Unexpected error: {e}")

            soup = BeautifulSoup(page.content(), "html.parser")

            # Select all movie card containers
            movie_cards = movie_divs = soup.select("div.col-xl-3.col-lg-3.col-md-3.first")

            # Get Already Added movies
            movies_added = find()

            for card in movie_cards:
                # Extract movie title
                try:
                    title = card.select_one(".movie-name").get_text(strip=True)
                    img = card.select_one("img.img-fluid")["src"]
                    info_link = card.select_one("a.single-page-main-link")["href"]
                    buy_link = card.select_one("a.buy-tickets")["href"]

                    movies.append({
                        "name": title,
                        "image": img,
                        "info_link": info_link,
                        "buy_link": buy_link
                    })
                except Exception as e:
                    print("Error parsing movie:", e)

                added_titles = [added_movie["title"] for added_movie in movies_added]

                if title not in added_titles:
                    logger.info(f"Adding New Movie - {title}...")
                    # Append to movies list
                    movies.append({
                        "title": title,
                        "link": info_link,
                        "buy_link": buy_link,
                        "image": img
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