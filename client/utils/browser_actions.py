import random

from client.driver.browser_driver import BrowserDriver


def random_driver_sleep(driver: BrowserDriver, micro_wait: bool = False):
    sleep_range_seconds = [0.5, 1.2] if micro_wait else [1, 2.5]
    sleep_duration = random.uniform(sleep_range_seconds[0], sleep_range_seconds[1])
    driver.wait_for_timeout(int(sleep_duration * 1000))


def random_mouse_movement(driver: BrowserDriver):
    driver.evaluate_script("""
        const width = window.innerWidth;
        const height = window.innerHeight;
        const randomX = Math.floor(Math.random() * width);
        const randomY = Math.floor(Math.random() * height);
        const event = new MouseEvent('mousemove', {
            bubbles: true,
            clientX: randomX,
            clientY: randomY
        });
        document.dispatchEvent(event);
    """)


def random_scroll(driver: BrowserDriver):
    # Get current scroll position to return to later
    current_y = driver.evaluate_script("window.pageYOffset")

    # Number of random scroll actions (1-4)
    scroll_actions = random.randint(1, 4)

    for _ in range(scroll_actions):
        # Random scroll direction and distance
        direction = random.choice(["up", "down"])
        distance = random.randint(200, 800)  # pixels

        if direction == "down":
            driver.evaluate_script(f"window.scrollBy(0, {distance})")
        else:
            driver.evaluate_script(f"window.scrollBy(0, -{distance})")

        # Human-like pause between scrolls
        random_driver_sleep(driver)

    # Return to original position
    driver.evaluate_script(f"window.scrollTo(0, {current_y})")
    # Final pause to mimic human behavior
