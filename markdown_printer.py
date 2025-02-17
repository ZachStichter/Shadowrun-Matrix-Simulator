import builtins
class MarkdownPrinter:
    def __init__(self, force_terminal=True):
        from rich.console import Console
        from rich.markdown import Markdown
        from rich.padding import Padding
        self.console = Console(force_terminal=force_terminal)
        self.Markdown = Markdown
        self.sprint = builtins.print
        self.Padding = Padding

    def __enter__(self):
        builtins.print = self.print
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        builtins.print = self.sprint

    def print(self, text):
        """Prints a given string with Markdown-aware formatting."""
        self.console.print(self.Padding(self.Markdown(text),(0,0,0,4)))

if __name__ == '__main__':
    with MarkdownPrinter():
        print("# Hello\n**Bold Text**\n*Italic Text*\n- List item 1\n- List item 2")
