from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-notify",
    version="0.1.0",
    author="jamez01",
    author_email="james@ruby-code.com",
    description="Cross-platform notification system for Claude Code hooks with intelligent project detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jamez01/claude-notify",
    project_urls={
        "Bug Reports": "https://github.com/jamez01/claude-notify/issues",
        "Source": "https://github.com/jamez01/claude-notify",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: System :: Monitoring",
        "Topic :: Communications",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    keywords="claude ai notifications hooks cross-platform desktop",
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
