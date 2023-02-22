#!/usr/bin/env python3

import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Driver:
    """A class for initializing a Selenium webdriver based on the Chrome browser and managing download paths for subtitles.

    Args:
        args: A Namespace object containing command line arguments parsed by argparse in subscraper.py.
    """

    def __init__(self, args):
        """Initializes a new instance of the Driver class.

        Args:
            args: A Namespace object containing command line arguments parsed by argparse in subscraper.py.
        """
        self.args = args

    @property
    def download_path(self) -> str:
        """Generates the download path for subtitles based on the output_path and language specified in the command line arguments.

        Returns:
            str: The absolute path to the output directory for downloaded subtitles, including a subfolder for the specified language.
        """
        if os.path.isabs(self.args.output_path):
            # If the output path is absolute, return the path with the language subfolder appended
            return f"{self.args.output_path}/{self.args.language}"
        else:
            # If the output path is relative, get the absolute path of the current working directory and append the output path and language subfolder
            return f"{os.path.abspath(os.path.join(os.path.abspath('.'), self.args.output_path))}/{self.args.language}"

    def create_download_folder(self) -> None:
        """
        Create the download folder if it does not exist.

        The method checks if the download path exists. If the folder does not exist, it is created.

        Returns:
            None
        """
        os.makedirs(self.download_path, exist_ok=True)

    def webdriver(self):
        """
        Create a WebDriver instance with Chrome options.

        The method sets the download preferences and Chrome options based on the arguments passed in the subscraper.py file.

        Returns:
            The Chrome WebDriver instance.
        """

        # Set download preferences
        prefs = {
            'download.default_directory': self.download_path,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        }

        # Set Chrome options
        options = webdriver.ChromeOptions()
        if self.args.incognito:
            options.add_argument('--incognito')
        if self.args.headless:
            options.add_argument('--headless')

        options.add_experimental_option('prefs', prefs)

        # Create and return a Chrome WebDriver instance
        # Create and return a Chrome WebDriver instance
        return webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
