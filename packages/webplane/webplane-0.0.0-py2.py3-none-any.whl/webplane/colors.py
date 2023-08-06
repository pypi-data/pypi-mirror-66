try:
    import colorama

    colorama_is_installed = True
except ImportError:
    colorama_is_installed = False

if colorama_is_installed:
    colorama.init()
    RED = colorama.Fore.RED
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    BRIGHT = colorama.Style.BRIGHT
    RESET = colorama.Style.RESET_ALL
else:
    RED = GREEN = YELLOW = RESET = BRIGHT = ""
