from enum import Enum


class Colours(Enum):
    """
    Colour Enum class.
    """
    RED          = "\033[31m"
    BLUE         = "\033[34m"
    GREEN        = "\033[32m"
    YELLOW       = "\033[33m"
    DARK_YELLOW  = "\033[93m"
    MAGENTA      = "\033[35m"
    BOLD_GREY    = "\033[1;30m"
    WHITE        = "\033[0m"
    DEFAULT      = "\033[0m"
