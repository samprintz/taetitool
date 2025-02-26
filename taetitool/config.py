class Style:
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INVERSE = '\033[7m'
    GREY = '\033[90m'

    def __init__(self, enabled=True):
        self.enabled = enabled

    def bold(self, text):
        if self.enabled:
            return f'{Style.BOLD}{text}{Style.END}'
        return text

    def underline(self, text):
        if self.enabled:
            return f'{Style.UNDERLINE}{text}{Style.END}'
        return text

    def inverse(self, text):
        if self.enabled:
            return f'{Style.INVERSE}{text}{Style.END}'
        return text

    def grey(self, text):
        if self.enabled:
            return f'{Style.GREY}{text}{Style.END}'
        return text
