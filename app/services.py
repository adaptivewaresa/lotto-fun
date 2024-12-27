import os
import re
import random
import requests
from bs4 import BeautifulSoup
import logging
import time
from functools import lru_cache
import threading
from logging.handlers import RotatingFileHandler

from app.fun_facts import get_random_fun_fact

home_directory = os.path.expanduser("~")

# Logger Configuration with RotatingFileHandler
LOG_FILE_PATH = os.path.join(
    home_directory, 'lottoscope.adaptiveware.dev', 'logs', 'debug.log')

log_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=3)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        log_handler,
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# URL for scraping lotto frequencies
LOTTO_URL = 'https://za.national-lottery.com/lotto/hot-numbers'


def fetch_html(url: str) -> str:
    """Helper function to fetch HTML content with error handling and retry logic."""
    try:
        logger.info(f"Fetching content from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for failed requests
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while fetching URL {url}: {e}")
        return None


def get_top_numbers(draw_frequencies, count, reverse=True):
    """Utility function to get top or bottom numbers from frequencies."""
    return [number for number, _ in sorted(draw_frequencies.items(), key=lambda item: item[1], reverse=reverse)[:count]]


@lru_cache(maxsize=1)
def fetch_draw_frequencies() -> dict:
    """Scrape lotto number frequencies with caching and error handling."""
    html_content = fetch_html(LOTTO_URL)

    if not html_content:
        return {}

    try:
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract frequencies
        table_cells = soup.find_all("div", class_="tableCell centred fluid")
        if not table_cells:
            raise ValueError("Unable to find table cells for lotto numbers.")

        frequencies = {}
        for cell in table_cells:
            try:
                ball = int(
                    cell.find("div", class_="ball lotto ball").text.strip())
                drawn_text = int(cell.find("strong").text.strip())
                frequencies[ball] = drawn_text
            except (ValueError, AttributeError):
                logger.warning("Skipped malformed cell during scraping.")

        logger.info("Successfully fetched draw frequencies.")
        return frequencies
    except Exception as e:
        logger.error(f"Error processing lotto draw frequencies: {e}")
        return {}


def get_lotto_jackpot(url: str = LOTTO_URL) -> str:
    """Fetch the current jackpot amount."""
    html_content = fetch_html(url)

    if not html_content:
        return None

    try:
        soup = BeautifulSoup(html_content, "html.parser")

        # The jackpot is within a span with a specific class.
        jackpot_element = soup.find("span", class_="jackpotTxt")

        if jackpot_element:
            jackpot_text = jackpot_element.text.strip()
            # Clean up the text (remove extra whitespace, etc.)
            jackpot_text = re.sub(r"\s+", " ", jackpot_text)
            return jackpot_text
        else:
            logger.warning(
                "Jackpot element not found on the page. The website structure may have changed.")
            return None

    except Exception as e:
        logger.error(f"Unexpected error while fetching jackpot: {e}")
        return None


def lucky_echo_bias(draw_frequencies, top_count=14, return_count=7):
    """Apply Lucky Echo Bias to select frequent lotto numbers."""
    top_numbers = get_top_numbers(draw_frequencies, top_count)
    random.shuffle(top_numbers)
    return top_numbers[:return_count]


def inverse_fortuna_boost(draw_frequencies, bottom_count=5):
    """Apply Inverse Fortuna Boost to select least frequent lotto numbers."""
    return get_top_numbers(draw_frequencies, bottom_count, reverse=False)


def chaos_jitter(range_=49, count=5):
    """Generate random chaotic numbers within a specified range."""
    return [random.randint(1, range_) for _ in range(count)]


def enforce_universal_balance(numbers, lucky_numbers):
    """Enforce universal balance among selected numbers."""
    if not isinstance(numbers, list) or not isinstance(lucky_numbers, list):
        return []

    numbers = list(set(numbers))
    lucky_numbers = list(set(lucky_numbers))

    all_available_numbers = numbers + lucky_numbers
    random.shuffle(all_available_numbers)
    random.shuffle(lucky_numbers)

    result = lucky_numbers[:min(2, len(lucky_numbers))]

    multiples_of_7 = [num for num in numbers if num %
                      7 == 0 and num not in result]
    if multiples_of_7:
        result.extend(multiples_of_7[:1])

    remaining_numbers = list(set(all_available_numbers) - set(result))
    random.shuffle(remaining_numbers)
    result.extend(remaining_numbers[:6 - len(result)])

    return result[:6]


def generate_pen_lotto_numbers():
    """Generate the final lotto numbers based on various biases and randomness."""
    logger.info("Generating lotto numbers...")
    try:
        draw_frequencies = fetch_draw_frequencies()
        if not draw_frequencies:
            raise ValueError(
                "Unable to fetch draw frequencies. Please try again later.")

        lucky_numbers = lucky_echo_bias(draw_frequencies)
        underdog_numbers = inverse_fortuna_boost(draw_frequencies)
        chaotic_numbers = chaos_jitter()
        final_numbers = enforce_universal_balance(
            chaotic_numbers + underdog_numbers, lucky_numbers)

        reasons = [
            f"Selected most frequently drawn numbers: {', '.join(map(str, lucky_numbers))}",
            f"Boosted least frequently drawn numbers: {', '.join(map(str, underdog_numbers))}",
            f"Generated random chaotic numbers: {', '.join(map(str, chaotic_numbers))}",
            f"Enforced universal balance: {', '.join(map(str, final_numbers))}",
        ]

        logger.info("Lotto numbers generated successfully.")
        return {
            "jackpot": get_lotto_jackpot(url=LOTTO_URL),
            "numbers": final_numbers,
            "reasons": reasons,
            "fun_fact": get_random_fun_fact(),
        }

    except requests.RequestException as e:
        logger.error(f"Error fetching lotto frequencies: {e}")
        return {"error": "Unable to fetch lotto frequencies. Please check your network connection and try again."}
    except ValueError as e:
        logger.error(f"Error in data processing: {e}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": "An error occurred during lotto number generation. Please try again later."}


def refresh_frequency_cache():
    """Refresh the frequency cache periodically (every 24 hours)."""
    while True:
        logger.info("Refreshing frequency cache...")
        fetch_draw_frequencies.cache_clear()
        fetch_draw_frequencies()
        time.sleep(86400)  # Sleep for 24 hours


def start_cache_refresh_task():
    """Start cache refresh task in a separate thread."""
    thread = threading.Thread(target=refresh_frequency_cache)
    thread.daemon = True
    thread.start()


def refresh_frequency_cache_task():
    logger.info("Refreshing frequency cache...")
    fetch_draw_frequencies.cache_clear()
    fetch_draw_frequencies()
