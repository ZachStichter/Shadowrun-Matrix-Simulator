import shutil, textwrap,builtins

class wrap:
    def __init__(self):
        self.terminal_width = shutil.get_terminal_size().columns
        self.orig_print = print
        self.new_print = self._wrapped_print

    def __enter__(self):
        builtins.print = self.new_print
        return self

    def __exit__(self,exc_type, exc_value,traceback):
        builtins.print = self.orig_print

    def _wrapped_print(self, *args, **kwargs):
         text = ' '.join(map(str,args))
         parts = text.split('\n')
         wrapped_parts = []
         for part in parts:
             wrapped_text = textwrap.fill(part,width=shutil.get_terminal_size().columns)
             wrapped_parts.append(wrapped_text)

         printable = '\n'.join(wrapped_parts)
         self.orig_print(printable,**kwargs)