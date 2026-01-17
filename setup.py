"""
Setup script for yt-x
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="yt-x",
    version="1.0.0",
    author="pinakdhabu",
    author_email="pinakdhabu@users.noreply.github.com",
    description="YouTube Terminal Browser - Windows Native",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pinakdhabu/yt-x",
    project_urls={
        "Bug Reports": "https://github.com/pinakdhabu/yt-x/issues",
        "Source": "https://github.com/pinakdhabu/yt-x",
        "Discord": "https://discord.gg/HBEmAwvbHV",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=[
        "textual>=7.3.0",
        "rich>=14.2.0",
        "requests>=2.32.0",
        "platformdirs>=4.5.0",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "yt-x=yt_x.cli:main",
        ],
    },
    include_package_data=True,
    keywords="youtube terminal tui video downloader mpv vlc yt-dlp",
    license="MIT",
)
