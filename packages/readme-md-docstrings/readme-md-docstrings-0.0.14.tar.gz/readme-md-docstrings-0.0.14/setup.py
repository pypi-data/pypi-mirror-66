from setuptools import setup

setup(
    name='readme-md-docstrings',
    version="0.0.14",
    description=(
        'Update README.md from Docstrings'
    ),
    author='David Belais',
    author_email='david@belais.me',
    python_requires='~=3.6',
    py_modules=['readme_md_docstrings'],
    install_requires=[],
    extras_require={
        "dev": [
            "wheel>=0.34.2",
            "setuptools>=40.8.0",
            "setuptools-setup-versions>=0.0.30",
            "pytest>=5.3.5",
            "tox>=3.14.3"
        ],
        "test": [
            "pytest>=5.3.5",
            "tox>=3.14.3"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
