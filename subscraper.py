#!/usr/bin/env python3

# Import libraries
import argparse
from src import OpenSubtitles

# Create argument parser
parser = argparse.ArgumentParser(description='Get subtitles from opensubtitles.org')

# Create argument groups
group_main = parser.add_argument_group('main')
group_filter = parser.add_argument_group('filter')
group_driver = parser.add_argument_group('driver')
group_download = parser.add_argument_group('download')
group_process = parser.add_argument_group('process')

# Add arguments for group main
group_main.add_argument('--imdb_id', nargs='+', help='Specify one or more IMDb IDs for the movies (prefix with "tt" or fully numeric)')

# Add arguments for group filter
group_filter.add_argument('--subtitle_type', type=str, default='srt', help='Filter by subtitle type (e.g., srt, sub)')
group_filter.add_argument('--language', type=str, default='eng', help='Filter by language (e.g., eng, spa)')

# Add arguments for group driver
group_driver.add_argument('--incognito', action='store_true', default=True, help='Launch the browser in incognito mode (private mode)')
group_driver.add_argument('--headless', action='store_true', default=False, help='Launch the browser in headless mode (no graphical interface)')

# Add arguments for group download
group_download.add_argument('--output_path', type=str, default='dump', help='Specify the path to the folder where to download the subtitles')
group_download.add_argument('--safe_downloading', action='store_true', help='Wait until the download completes before getting the next subtitle (only works for bulk download)')
group_download.add_argument('--change_file_names', action='store_true', help='Change the subtitle file names to their IMDb IDs after download complete')

# Add arguments for group process
group_main.add_argument('--save_process', action='store_true', help='Save which movie were downloaded in a JSON file')
group_main.add_argument('--save_process_path', type=str, default='process', help='Specify the path where to save the JSON file')
group_main.add_argument('--reset_process', type=bool, default=False, help='Reset process')

# Parse the arguments
args = parser.parse_args()

opensubs = OpenSubtitles(args=args)
opensubs.execute()