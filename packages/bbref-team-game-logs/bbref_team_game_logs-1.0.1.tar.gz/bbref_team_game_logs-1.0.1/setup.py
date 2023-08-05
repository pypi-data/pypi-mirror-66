import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bbref_team_game_logs",
    version="1.0.1",
    author="Siddharth Mehta",
    author_email="siddharthm2350@gmail.com",
    description="Retrieves a team's regular season game log and stats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sherpan/bbref_team_game_logs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4==4.8.2',
        'pandas==0.25.3',
        'requests==2.22.0',
        'lxml==4.4.2'
    ],
)
