from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-notify",
    version="0.1.0",
    author="Your Name",
    description="A cross-platform notification system for Claude",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/claude-notify",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "plyer>=2.1",
        "click>=8.1.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "claude-notify=claude_notify.cli:main",
        ],
    },
)