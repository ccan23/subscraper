# subscraper

SubScraper is a simple Python script that allows you to download subtitles from OpenSubtitles.org. The script is designed to work with movies identified by their IMDb ID.

While OpenSubtitles has an API, it has many limitations, and using the API often results in a "too many requests" error. Instead, I used a Selenium-based approach to retrieve the subtitles. This approach has helped me to overcome the limitations of the OpenSubtitles API and avoid some limitations.

## Getting Started
1. Clone the repo:
```sh
    git clone https://github.com/ccan23/subscraper.git
```
2. Navigate to the project directory:
```sh
    cd subscraper
```
3. Install the required libraries:
```sh
    pip install -r requirements.txt
```

## Usage
Here are the available arguments for the script:
```
--imdb_id               Specify one or more IMDb IDs for the movies (prefix with "tt" or fully numeric)
--subtitle_type         Filter by subtitle type (e.g., srt, sub)
--language              Filter by language (e.g., eng, spa)
--incognito             Launch the browser in incognito mode (private mode)
--headless              Launch the browser in headless mode (no graphical interface)
--output_path           Specify the path to the folder where to download the subtitles
--safe_downloading      Wait until the download completes before getting the next subtitle (only works for bulk download)
--change_file_names     Change the subtitle file names to their IMDb IDs after download complete
--save_process          Save which movie were downloaded in a JSON file
--save_process_path     Specify the path where to save the JSON file
--reset_process         Reset process
```

### Examples
Install The Matrix subtitle (default language: english, default format: .srt)
```sh
python3 subscraper.py --imdb_id tt0133093
```

Install Spanish subtitle in .sub format.
```sh
python3 subscraper.py --imdb_id tt0133093 --language spa --subtitle_type sub
```

Install 4 subtitles, save the process to the process.json file, wait until the download completes before getting the next subtitle, and change file names.
```sh
python3 subscraper.py --save_process --safe_downloading --change_file_names --imdb_id tt0111161 tt0068646 tt15097216 tt0468569
```

## License
MIT