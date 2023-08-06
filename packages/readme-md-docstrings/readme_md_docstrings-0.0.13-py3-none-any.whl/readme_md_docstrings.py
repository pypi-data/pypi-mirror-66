"""
This module may be called as a command-line executable. For example:
```shell script
python3 -m readme_md_docstrings ./README.md
```

If no path is provided, the default is "./README.md":
```shell script
python3 -m readme_md_docstrings
```
"""
import argparse
import collections
import importlib
import pydoc
from typing import Iterable, List, Optional, Sequence, Tuple


def _get_object_from_path(path: str) -> Optional[object]:
    """
    Get a function, class, or module from a fully-qualified path + name.
    """
    object_: Optional[object] = None
    parts: List[str] = path.split('.')
    index: int
    attribute_name: str
    # Iterate over indices in reverse: 0, -1, -2, -3, ...
    for index in range(0, -len(parts), -1):
        # When the index is `0`--we use the whole path, otherwise
        # we split at `index`
        module_path: str = (
            '.'.join(parts[:index])
            if index else
            path
        )
        # Check to see if `module_path` is valid, and if it is not--continue
        # to shift the split index until we find a module path which *is*
        # valid, or come to the beginning of the path
        try:
            object_ = importlib.import_module(
                module_path
            )
            # If the module path is a valid namespace, but the `path`
            # was pointing to an attribute of the module and not the module
            # itself--resolve that attribute path
            if index < 0:
                for attribute_name in parts[index:]:
                    try:
                        object_ = getattr(object_, attribute_name)
                    except AttributeError:
                        object_ = None
            break
        except ModuleNotFoundError:
            pass
    return object_


def _get_header_level(header: str) -> int:
    header_level: int = 0
    character: str
    for character in header:
        if character == '#':
            header_level += 1
        else:
            break
    return header_level


def _get_header_name(header: str) -> str:
    return header.lstrip('#').strip()


def _get_sub_section_ranges(
    lines: Sequence[str],
    header_level: int
) -> List[Tuple[int, int]]:
    assert lines
    in_code_block: bool = False
    sub_section_ranges: List[Tuple[int, int]] = []
    line: str
    start: int = 0
    index: int = 0
    for index, line in enumerate(lines, 0):
        # Identify whether we are inside a code block
        if (
            # We were not *already* within a code block
            (not in_code_block) and
            # This line opens a code block
            line.lstrip().startswith('```') and
            # This line does not also close that code block
            len(line.split('```')) == 2
        ):
            # We started a new code block
            in_code_block = True
        elif in_code_block and len(line.split('```')) == 2:
            # We've ended a code block
            in_code_block = False
        # Only examine lines which are *not* within code blocks,
        # and which are *not* part of the top-level header
        if (not in_code_block) and index:
            line_header_level: int = _get_header_level(line)
            if line_header_level == header_level:
                sub_section_ranges.append((start, index))
                start = index
            else:
                # We shouldn't have any lower-level headers...
                assert (
                    line_header_level == 0 or
                    line_header_level > header_level
                )
    # if start != index:
    sub_section_ranges.append((start, index + 1))
    return sub_section_ranges


class Section:

    def __init__(
        self,
        lines: Iterable[str],
        parent_object_path: str = ''
    ) -> None:
        self.documented_object: Optional[object] = None
        self.name_space_path: str = parent_object_path
        self.name: str = ''
        self.header_level: int = 0
        self.lines: List[str] = []
        self.sub_sections: List[Section] = []
        self._init_lines(lines)

    def _init_header(self, header: str) -> None:
        self.header_level = _get_header_level(header)
        self.name = _get_header_name(header)
        name_space_path: Optional[str]
        for name_space_path in (
            [f'{self.name_space_path}.{self.name}']
            if self.name_space_path else []
        ) + [
            self.name,
            None
        ]:
            if name_space_path is not None:
                self.documented_object = _get_object_from_path(name_space_path)
            self.name_space_path = name_space_path
            if self.documented_object is not None:
                break

    def _init_lines(self, lines: Iterable[str]) -> None:
        # If `lines` is not a sequence, make it one
        if not isinstance(lines, collections.abc.Sequence):
            lines = tuple(lines)
        # Ensure there is at least one line
        assert lines
        self._init_header(lines[0])
        start: int
        end: int
        for start, end in _get_sub_section_ranges(
            lines,
            self.header_level + 1
        ):
            if start:
                # This is a new sub-section
                self.sub_sections.append(
                    Section(
                        lines[start: end],
                        parent_object_path=self.name_space_path
                    )
                )
            else:
                # This is the top-level content
                self.lines.extend(lines[start: end])

    def _get_docstring(self) -> str:
        docstring: str = ''
        if self.documented_object is not None:
            docstring: str = pydoc.getdoc(self.documented_object).rstrip()
        return docstring

    def __str__(self) -> str:
        assert self.lines
        docstring: str = self._get_docstring()
        sub_sections_text: str = ''
        if self.sub_sections:
            sub_sections_text = '\n'.join(
                str(section)
                for section in self.sub_sections
            )
        if docstring:
            return (
                f'{self.lines[0].strip()}\n\n'
                f'{docstring}\n'
            ) + (
                ('\n' + sub_sections_text)
                if sub_sections_text else
                sub_sections_text
            )
        else:
            return '\n'.join(
                self.lines + (
                    [sub_sections_text]
                    if sub_sections_text else
                    []
                )
            )


class ReadMe:
    r"""
    This class parses a markdown-formatted README file and updates sections
    to reflect a corresponding package's class, method, and function
    docstrings.

    Parameters:

    - markdown (str): Markdown-formatted text

    ```python
    from readme_md_docstrings import ReadMe
    # Read the existing markdown
    path: str = './README.md'
    with open(path, 'r') as readme_io:
        read_me: ReadMe = ReadMe(readme_io.read())
    read_me_str: str = str(read_me).rstrip()
    # Update and save
    if read_me_str:
        with open(path, 'w') as readme_io:
            readme_io.write(read_me_str)
    ```
    """

    def __init__(
        self,
        markdown: str
    ) -> None:
        self.markdown = markdown

    def __str__(self) -> str:
        """
        Render the document as markdown, updated to reflect any docstrings
        that were found
        """
        return str(Section(self.markdown.split('\n')))


def update(path: str = './README.md') -> None:
    """
    Update an existing markdown-formatted README file based on any headers
    matching (fully-qualified) module, class, or function docstrings.

    ```python
    import readme_md_docstrings
    readme_md_docstrings.update('./README.md')
    ```
    """
    # Read the existing markdown
    with open(path, 'r') as readme_io:
        read_me: ReadMe = ReadMe(readme_io.read())
    read_me_str: str = str(read_me)
    # Update and save
    if read_me_str:
        with open(path, 'w') as readme_io:
            readme_io.write(read_me_str)


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Parse command-line arguments'
    )
    parser.add_argument(
        'path',
        default='./README.md',
        nargs=argparse.OPTIONAL,
        help='Where is the README file (defaults to "./README.md")?'
    )
    arguments = parser.parse_args()
    update(arguments.path)
