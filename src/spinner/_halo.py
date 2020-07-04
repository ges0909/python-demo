import time

from colorama import Fore
from halo import Halo

DELAY_IN_SECS = 2

if __name__ == "__main__":
    with Halo(text="Hallo!", placement="right"):
        time.sleep(DELAY_IN_SECS)
    with Halo(text="Next step!", placement="right") as spinner:
        time.sleep(DELAY_IN_SECS)
        spinner.warn()
    with Halo(placement="right") as spinner:
        time.sleep(DELAY_IN_SECS)
        spinner.succeed()
    with Halo(text=Fore.RED + "Loading", spinner="dots") as spinner:
        time.sleep(DELAY_IN_SECS)
        spinner.fail()
    # !! ignores leading spaces
    with Halo("  Loading", spinner="dots", color="grey") as spinner:
        time.sleep(DELAY_IN_SECS)
        spinner.info()
    with Halo(text=Fore.YELLOW + "Loading", spinner="dots", placement="right") as spinner:
        time.sleep(DELAY_IN_SECS)
        spinner.warn()
