import random
import requests
from bs4 import BeautifulSoup

from app.fun_facts import get_random_fun_fact

# URL for scraping lotto frequencies
LOTTO_URL = 'https://za.national-lottery.com/lotto/hot-numbers'


def fetch_draw_frequencies():
    """Scrape lotto number frequencies from the website."""
    response = requests.get(LOTTO_URL)
    response.raise_for_status()  # Raise an error for failed requests

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract frequencies
    table_cells = soup.find_all("div", class_="tableCell centred fluid")
    frequencies = {}
    for cell in table_cells:
        ball = cell.find("div", class_="ball lotto ball").text.strip()
        drawn_text = cell.find("strong").text.strip()
        frequencies[int(ball)] = int(drawn_text)

    return frequencies


def lucky_echo_bias(draw_frequencies, top_count=13, return_count=5):
    sorted_frequencies = sorted(
        draw_frequencies.items(), key=lambda item: item[1], reverse=True)
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
    if any(number % 7 == 0 for number in numbers):
        return numbers[:6]
    numbers.append(random.randint(1, 7) * 7)
    return numbers[:6]


def generate_pen_lotto_numbers():
    """Generate lotto numbers using dynamic frequencies."""
    draw_frequencies = fetch_draw_frequencies()
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

    return {"numbers": final_numbers, "reasons": reasons, "fun_fact": get_random_fun_fact(), }
