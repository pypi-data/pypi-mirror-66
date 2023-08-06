# readme-md-docstrings

This script updates module, class, and function docs in a README.md file,
based on their corresponding docstrings (so that documentation does not need to
be manually written in two places).

## Install

```shell script
pip3 install readme-md-docstrings
```

## Modules

### readme_md_docstrings

This module may be called as a command-line executable. For example:
```shell script
python3 -m readme_md_docstrings ./README.md
```

If no path is provided, the default is "./README.md":
```shell script
python3 -m readme_md_docstrings
```

#### ReadMe

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

#### update

Update an existing markdown-formatted README file based on any headers
matching (fully-qualified) module, class, or function docstrings.

```python
import readme_md_docstrings
readme_md_docstrings.update('./README.md')
```
