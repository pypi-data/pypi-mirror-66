import curses
import random
import time
from dataclasses import dataclass
from typing import List

from space_console_game.animate_spaceship import animate_spaceship
from space_console_game.app_helpers import get_rocket_frame_content, sleep
from space_console_game.fire_animation import fire

TIC_TIMEOUT = 0.1
SYMBOLS_FOR_STARS = '+*.:'
COUNT_OF_STARS = 300
OFFSET_DELAY = int(5 / TIC_TIMEOUT)


@dataclass
class Star:
    """Star attribute."""

    brightness: int
    sleep_time: float


async def blink(
    canvas,
    row: int,
    column: int,
    offset_ticks: int,
    symbol: str = '*',
) -> None:
    """Display animation of blink star."""
    stars = [
        Star(brightness=curses.A_DIM, sleep_time=2),
        Star(brightness=curses.A_NORMAL, sleep_time=0.3),  # noqa: WPS432
        Star(brightness=curses.A_BOLD, sleep_time=0.5),
        Star(brightness=curses.A_NORMAL, sleep_time=0.3),  # noqa: WPS432
    ]
    while True:
        await sleep(offset_ticks)
        for star in stars:
            canvas.addstr(row, column, symbol, star.brightness)
            await sleep(int(star.sleep_time / TIC_TIMEOUT))


def get_coroutines(
    canvas,
    canvas_height: int,
    canvas_width: int,
    rocket_frames: List[str],
    screen_border: int = 2,
):
    """Getting coroutines."""
    coroutines = [
        blink(
            canvas,
            row=random.SystemRandom().randint(screen_border, canvas_height - screen_border),
            column=random.SystemRandom().randint(screen_border, canvas_width - screen_border),
            offset_ticks=random.SystemRandom().randint(0, OFFSET_DELAY),
            symbol=random.SystemRandom().choice(SYMBOLS_FOR_STARS),
        )
        for _ in range(COUNT_OF_STARS)
    ]

    coroutines.append(
        fire(
            canvas,
            start_row=canvas_height - screen_border,
            start_column=canvas_width / 2,
        ),
    )

    coroutines.append(
        animate_spaceship(
            canvas,
            rocket_frames=rocket_frames,
            canvas_height=canvas_height,
            canvas_width=canvas_width,
        ),
    )
    return coroutines


def draw(canvas) -> None:
    """Play the game."""
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)

    canvas_height, canvas_width = canvas.getmaxyx()

    rocket_frames = [
        get_rocket_frame_content('space_console_game/frames/rocket_frame_1.txt '),
        get_rocket_frame_content('space_console_game/frames/rocket_frame_2.txt '),
    ]

    coroutines = get_coroutines(canvas, canvas_height, canvas_width, rocket_frames)
    while coroutines:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
