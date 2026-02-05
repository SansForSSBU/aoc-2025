# Setup

From the root of the repository:

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

pip install -e .

# Downloading inputs

From the root of the repository:

mkdir inputs

cd src

python3 downloader.py <advent_of_code_session_cookie>

# Running solutions

From the root of the repository:

python3 src/main.py <day_num>
