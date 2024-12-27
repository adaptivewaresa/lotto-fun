import os
import random
import requests
from bs4 import BeautifulSoup
import logging
import time
from functools import lru_cache

from app.fun_facts import get_random_fun_fact

from logging.handlers import RotatingFileHandler

home_directory = os.path.expanduser("~")

# Logger Configuration
LOG_FILE_PATH = f"{home_directory}/lottoscope.adaptiveware.dev/logs/debug.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),  # Log to file
        logging.StreamHandler()             # Also log to console
    ]
)
logger = logging.getLogger(__name__)


# URL for scraping lotto frequencies
LOTTO_URL = 'https://za.national-lottery.com/lotto/hot-numbers'


@lru_cache(maxsize=1)
def fetch_draw_frequencies():
    """Scrape lotto number frequencies with caching and error handling."""
    try:
        logger.info("Fetching lotto draw frequencies from the website...")
        response = requests.get(LOTTO_URL, timeout=10)
        response.raise_for_status()  # Raise error for failed requests

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

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
    except requests.RequestException as e:
        logger.error(f"Error fetching lotto draw frequencies: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {}


def lucky_echo_bias(draw_frequencies, top_count=13, return_count=5):
    sorted_frequencies = sorted(
        draw_frequencies.items(), key=lambda item: item[1], reverse=True
    )
    top_numbers = [number for number, _ in sorted_frequencies[:top_count]]
    random.shuffle(top_numbers)
    return top_numbers[:return_count]


def inverse_fortuna_boost(draw_frequencies, bottom_count=3):
    sorted_numbers = sorted(draw_frequencies.items(), key=lambda x: x[1])
    random.shuffle(sorted_numbers)
    return [num for num, _ in sorted_numbers[:bottom_count]]


def chaos_jitter(range_=49, count=5):
    return [random.randint(1, range_) for _ in range(count)]


def enforce_universal_balance(numbers):
    random.shuffle(numbers)
    if any(number % 7 == 0 for number in numbers):
        return numbers[:6]
    numbers.append(random.randint(1, 7) * 7)
    return numbers[:6]


def generate_pen_lotto_numbers():
    """Generate lotto numbers with caching, error handling, and logging."""
    logger.info("Generating lotto numbers...")
    try:
        draw_frequencies = fetch_draw_frequencies()
        if not draw_frequencies:
            raise ValueError(
                "Unable to fetch draw frequencies. Please try again later.")

        reasons = []

        # Lucky Echo Bias
        lucky_numbers = lucky_echo_bias(draw_frequencies)
        reasons.append(
            f"Selected most frequently drawn numbers: {', '.join(map(str, lucky_numbers))}")

        # Inverse Fortuna Boost
        underdog_numbers = inverse_fortuna_boost(draw_frequencies)
        reasons.append(
            f"Boosted least frequently drawn numbers: {', '.join(map(str, underdog_numbers))}")

        # Chaos Jitter
        chaotic_numbers = chaos_jitter()
        reasons.append(
            f"Generated random chaotic numbers: {', '.join(map(str, chaotic_numbers))}")

        # Enforce Universal Balance
        final_numbers = enforce_universal_balance(
            lucky_numbers + chaotic_numbers[:3] + underdog_numbers)
        reasons.append(
            f"Enforced universal balance: {', '.join(map(str, final_numbers))}")

        logger.info("Lotto numbers generated successfully.")
        return {
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


# Background Task for Updating Cache
def refresh_frequency_cache():
    while True:
        logger.info("Refreshing frequency cache...")
        fetch_draw_frequencies.cache_clear()
        fetch_draw_frequencies()  # Populate cache
        time.sleep(86400)  # Refresh every 24 hours


# Background Task for Updating Cache
def refresh_frequency_cache_task():
    logger.info("Refreshing frequency cache...")
    fetch_draw_frequencies.cache_clear()
    fetch_draw_frequencies()  # Repopulate the cache
