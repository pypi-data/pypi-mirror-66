import logging
import sys
from abc import abstractmethod
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Type, Union
if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    Protocol = object
else:
    from typing_extensions import Protocol

import colorama
from colorama import Back, Fore, Style
from colorama.ansi import AnsiFore, AnsiBack, AnsiStyle

from .progress import StatusWriter
from .version import VERSION_STRING

log = logging.getLogger(__name__)


class Writer(Protocol):
    @abstractmethod
    def write(self, s: str) -> int:
        pass

    @abstractmethod
    def isatty(self) -> bool:
        pass

    @abstractmethod
    def flush(self) -> Any:
        pass


class RawWriter(Writer, Protocol):
    @abstractmethod
    def raw_write(self, s: str) -> int:
        pass


STRIKETHROUGH = '\u0336'
UNDER_PLUS = '\u031F'


class CombiningMarkWriter(RawWriter):
    def __init__(self, parent: RawWriter):
        self.parent: RawWriter = parent
        self._marks: Set[str] = set()
        self.enabled: bool = True

    def add(self, combining_mark: str):
        self._marks.add(combining_mark)

    def remove(self, combining_mark: str):
        self._marks.remove(combining_mark)

    def context(self, *combining_marks: str) -> 'CombiningMarkContext':
        return CombiningMarkContext(self, *combining_marks)

    @property
    def marks(self) -> Set[str]:
        return self._marks

    @property
    def marks_str(self) -> str:
        return ''.join(self._marks)

    def write(self, s: str) -> int:
        if self.enabled:
            marks = self.marks_str
            return self.parent.raw_write("".join(f"{c}{marks}" for c in s))
        else:
            return self.raw_write(s)

    def raw_write(self, s: str) -> int:
        return self.parent.raw_write(s)

    def isatty(self) -> bool:
        return self.parent.isatty()

    def flush(self):
        return self.parent.flush()


class CombiningMarkContext:
    def __init__(self, writer: CombiningMarkWriter, *combining_marks: str):
        self.writer: CombiningMarkWriter = writer
        self.marks: Set[str] = set(combining_marks)
        self._state_before: Optional[Set[str]] = None

    def __enter__(self) -> CombiningMarkWriter:
        self._state_before = set(self.writer.marks)
        for mark in self.marks:
            self.writer.add(mark)
        return self.writer

    def __exit__(self, exc_type, exc_val, exc_tb):
        for mark in self.marks - self._state_before:
            self.writer.remove(mark)


class ANSIContext:
    def __init__(
            self,
            stream: Union[RawWriter, 'ANSIContext'],
            fore: Optional[AnsiFore] = None,
            back: Optional[AnsiBack] = None,
            style: Optional[AnsiStyle] = None,
    ):
        if isinstance(stream, ANSIContext):
            self.stream: RawWriter = stream.stream
            self._parent: Optional['ANSIContext'] = stream
        else:
            self.stream: RawWriter = stream
            self._parent: Optional['ANSIContext'] = None
        self._fore: Optional[AnsiFore] = fore
        self._back: Optional[AnsiBack] = back
        self._style: Optional[AnsiStyle] = style
        self._start_code: Optional[str] = None
        self._end_code: Optional[str] = None
        self.is_applied: bool = False

    @property
    def start_code(self) -> str:
        if self._start_code is None:
            self._set_codes()
        return self._start_code

    @property
    def end_code(self) -> str:
        if self._end_code is None:
            self._set_codes()
        return self._end_code

    def _set_codes(self):
        if not self.is_applied:
            raise ValueError("start_code and end_code should only be called after an ANSIContext has been __enter__'d")

        self._start_code: str = ''
        self._end_code: str = ''

        contexts = ANSI_CONTEXT_STACK[self.stream]
        if contexts:
            if self._parent is None:
                self._parent: Optional['ANSIContext'] = contexts[-1]
            else:
                if not self.root.is_applied:
                    self.root._parent = contexts[-1]

        parent_end_code: str = ''
        if self.parent is not None and not self.parent.is_applied:
            self.parent.is_applied = True
            self._start_code += self.parent.start_code
            parent_end_code = self.parent.end_code

        if self._fore is not None and (self._parent is None or self._fore != self.parent.fore):
            self._start_code += self._fore
            if self._parent is None or self.parent.fore is None:
                self._end_code = Fore.RESET
            else:
                self._end_code = self.parent.fore
        if self._back is not None and (self._parent is None or self._back != self.parent.back):
            self._start_code += self._back
            if self._parent is None or self.parent.back is None:
                self._end_code = Back.RESET
            else:
                self._end_code = self.parent.back
        if self._style is not None and (self._parent is None or self._style != self.parent.style):
            self._start_code += self._style
            if self._parent is None or self.parent.style is None:
                self._end_code = Style.RESET_ALL
            else:
                self._end_code = self.parent.style

        self._end_code += parent_end_code

    @property
    def fore(self) -> Optional[AnsiFore]:
        if self._fore is None and self._parent is not None:
            return self._parent.fore
        else:
            return self._fore

    @property
    def back(self) -> Optional[AnsiBack]:
        if self._back is None and self._parent is not None:
            return self._parent.back
        else:
            return self._back

    @property
    def style(self) -> Optional[AnsiStyle]:
        if self._style is None and self._parent is not None:
            return self._parent.style
        else:
            return self._style

    @property
    def parent(self) -> Optional['ANSIContext']:
        return self._parent

    def color(self, foreground_color: AnsiFore) -> 'ANSIContext':
        return self.__class__(
            stream=self,
            fore=foreground_color
        )

    def background(self, bg_color: AnsiBack) -> 'ANSIContext':
        return self.__class__(
            stream=self,
            back=bg_color
        )

    def bright(self) -> 'ANSIContext':
        return self.__class__(
            stream=self,
            style=Style.BRIGHT
        )

    def dim(self) -> 'ANSIContext':
        return self.__class__(
            stream=self,
            style=Style.DIM
        )

    @property
    def root(self):
        root = self
        while root._parent is not None:
            root = root._parent
        return root

    def __enter__(self) -> RawWriter:
        assert not self.is_applied
        self.is_applied = True
        self.stream.raw_write(self.start_code)
        ANSI_CONTEXT_STACK[self.stream].append(self)
        return self.stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.is_applied
        self.stream.raw_write(self.end_code)
        self.is_applied = False
        self._start_code = None
        self._end_code = None
        assert ANSI_CONTEXT_STACK[self.stream] and ANSI_CONTEXT_STACK[self.stream][-1] == self
        ANSI_CONTEXT_STACK[self.stream].pop()


class HTMLANSIContext(ANSIContext):
    @staticmethod
    def get_fore(color: AnsiFore) -> str:
        for name in ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'):
            if color == Fore.BLACK:
                return "gray"
            elif color == getattr(Fore, name.upper()):
                return name
        raise ValueError(f"Unknown ANSI color: \"{color}\"")

    @staticmethod
    def get_back(color: AnsiBack) -> str:
        for name in ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'):
            if color == getattr(Back, name.upper()):
                return name
        raise ValueError(f"Unknown ANSI color: \"{color}\"")

    def _set_codes(self):
        if not self.is_applied:
            raise ValueError("start_code and end_code should only be called after an ANSIContext has been __enter__'d")

        self._start_code: str = ''
        self._end_code: str = ''
        style = ''

        contexts = ANSI_CONTEXT_STACK[self.stream]
        if contexts:
            if self._parent is None:
                self._parent: Optional['ANSIContext'] = contexts[-1]
            else:
                if not self.root.is_applied:
                    self.root._parent = contexts[-1]

        parent_end_code: str = ''
        if self.parent is not None and not self.parent.is_applied:
            self.parent.is_applied = True
            self._start_code += self.parent.start_code
            parent_end_code = self.parent.end_code

        if self._fore is not None and self._fore and (self._parent is None or self._fore != self.parent.fore):
            style += f"color: {self.get_fore(self._fore)};"
        if self._back is not None and (self._parent is None or self._back != self.parent.back):
            style += f"background-color: {self.get_back(self._back)};"
        if self._style is not None and (self._parent is None or self._style != self.parent.style):
            if self._style == Style.BRIGHT:
                style += f"font-weight: bold; opacity: 1.0;"
            elif self._style == Style.DIM:
                style += f"opacity: 0.6; font-weight: normal;"
            else:
                style += f"font-weight: normal; opacity: 1.0;"

        if style:
            self._start_code = f'{self._start_code}<span style="{style}">'
            self._end_code = '</span>'
        else:
            self._start_code = ''
            self._end_code = ''
        self._end_code = f"{self._end_code}{parent_end_code}"


class NullANSIContext:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __getattr__(self, item):
        def fake_fun(*args, **kwargs):
            return self

        return fake_fun


ANSI_CONTEXT_STACK: Dict[Writer, List[ANSIContext]] = defaultdict(list)


class Printer(StatusWriter, RawWriter):
    def __init__(
            self,
            out_stream: Optional[Writer] = None,
            ansi_color: Optional[bool] = None,
            quiet: bool = False,
            options: Optional[Dict[str, Any]] = None
    ):
        if out_stream is None:
            out_stream = sys.stdout
        super().__init__(
            out_stream=out_stream,
            quiet=quiet
        )
        self._context_type: Type[ANSIContext] = ANSIContext
        self.out_stream: CombiningMarkWriter = CombiningMarkWriter(self)
        self.indents = 0
        self._ansi_color = None
        self.ansi_color = ansi_color
        if self.ansi_color:
            colorama.init()
        self._strikethrough = False
        self._plusthrough = False
        if options is not None:
            for option, value in options.items():
                if hasattr(self, option):
                    raise ValueError(f"Illegal option name: {option}")
                setattr(self, option, value)

    @property
    def ansi_color(self) -> bool:
        return self._ansi_color

    @ansi_color.setter
    def ansi_color(self, is_color: Optional[bool]):
        if is_color is None:
            self._ansi_color = self.out_stream.isatty()
        else:
            self._ansi_color = is_color

    def context(self) -> ANSIContext:
        if ANSI_CONTEXT_STACK[self]:
            return ANSI_CONTEXT_STACK[self][-1]
        else:
            return ANSIContext(self)

    def raw_write(self, s: str) -> int:
        return super().write(s)

    def write(self, s: str) -> int:
        return self.out_stream.write(s)

    def newline(self):
        self.raw_write('\n')
        self.raw_write(' ' * (4 * self.indents))

    def color(self, foreground_color: AnsiFore) -> ANSIContext:
        if self.ansi_color:
            return self._context_type(self, fore=foreground_color)
        else:
            return NullANSIContext()    # type: ignore

    def background(self, bg_color: AnsiBack) -> ANSIContext:
        if self.ansi_color:
            return self._context_type(self, back=bg_color)
        else:
            return NullANSIContext()    # type: ignore

    def bright(self) -> ANSIContext:
        if self.ansi_color:
            return self._context_type(self, style=Style.BRIGHT)
        else:
            return NullANSIContext()    # type: ignore

    def dim(self) -> ANSIContext:
        if self.ansi_color:
            return self._context_type(self, style=Style.DIM)
        else:
            return NullANSIContext()    # type: ignore

    def strike(self) -> CombiningMarkContext:
        if self.ansi_color:
            return self.out_stream.context(STRIKETHROUGH)
        else:
            return NullANSIContext()    # type: ignore

    def under_plus(self):
        if self.ansi_color:
            return self.out_stream.context(UNDER_PLUS)
        else:
            return NullANSIContext()    # type: ignore

    def indent(self) -> 'Printer':
        class Indent:
            def __init__(self, printer):
                self.printer = printer

            def __enter__(self):
                self.printer.indents += 1
                return self.printer

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.printer.indents -= 1

        return Indent(self)


class HTMLPrinter(Printer):
    def __init__(self, *args, title: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._context_type = HTMLANSIContext
        self.raw_write("<html>")
        self.indents += 1
        super().newline()
        with self.html_element('head'):
            with self.html_element('meta', charset='UTF-8', inline=True):
                pass
            super().newline()
            with self.html_element('meta', name='application-name', content='graphtage', inline=True):
                pass
            super().newline()
            with self.html_element('meta', name='application-version', content=VERSION_STRING, inline=True):
                pass
            super().newline()
            with self.html_element('title', inline=True) as p:
                if title is None:
                    p.write("Graphtage Diff")
                else:
                    p.write(title)
        self.raw_write("<body>")
        super().newline()
        self.indents += 1
        self.raw_write("<div style=\"margin: auto; background-color: black; color: gray;\">")
        super().newline()
        self.indents += 1

    def close(self):
        if self.indents != 3:
            log.warning(f"Mismatched indent; expected 3 but got {self.indents}")
        self.indents -= 1
        super().newline()
        self.raw_write("</body>")
        self.indents -= 1
        super().newline()
        self.raw_write("</html>")
        super().newline()

    def html_element(self, element_name, inline=False, **kwargs) -> 'HTMLPrinter':
        class Element:
            def __init__(self, printer):
                self.printer = printer

            def __enter__(self):
                tags = ''.join(f" {k}=\"{v}\"" for k, v in kwargs.items())
                self.printer.raw_write(f"<{element_name}{tags}>")
                if not inline:
                    self.printer.indents += 1
                    Printer.newline(self.printer)
                return self.printer

            def __exit__(self, exc_type, exc_val, exc_tb):
                if not inline:
                    self.printer.indents -= 1
                    Printer.newline(self.printer)
                self.printer.raw_write(f"</{element_name}>")
                if not inline:
                    Printer.newline(self.printer)

        return Element(self)

    def strike(self):
        return self.html_element('span', inline=True, style='text-decoration: line-through;')

    def newline(self):
        super().raw_write('<br />')
        super().newline()

    def indent(self) -> 'Printer':
        return self.html_element('div', style='margin-left: 24pt; font-family: monospace; padding: 0;')

    def write(self, s: str) -> int:
        # super().write(html.escape(s))
        super().write(s)


DEFAULT_PRINTER: Printer = Printer()
