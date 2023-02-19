#!/usr/bin/env python3

# import libraries
from selenium.webdriver.common.by import By

import src.element_locations as el
from .main_operations import MainOperations

class OpenSubtitles(MainOperations):
    
    def __init__(self, args):
        """Initializes an instance of the OpenSubtitles class.

        Args:
            args: A Namespace object that contains command line arguments.
        """
        super().__init__(args)
    
    def url(self, imdb_id: str) -> str:
        """Returns a URL for OpenSubtitles that includes filters for a given IMDb ID.

        Args:
            imdb_id (str): An IMDb ID.

        Returns:
            str: A URL for OpenSubtitles that includes filters for the given IMDb ID.
        """
        base_url = 'https://www.opensubtitles.org/en/search/'

        # URL parameters
        params = {
            'sublanguageid': self.args.language,
            'searchonlymovies': 'on',
            'subsumcd': '1',
            'subformat': self.args.subtitle_type,
            'imdbid': imdb_id,
            'sort': '7',
            'asc': '0'
        }

        # Merge parameters with the base URL and split them with '/'
        query_string = [f'{key}-{value}' for key, value in params.items()]
        query_string = '/'.join(query_string)

        return base_url + query_string

    def launch_page(self, imdb_id: str):
        """Launches the OpenSubtitles search page for a given IMDb ID.

        Args:
            imdb_id (str): An IMDb ID.
        """
        self.driver.get(self.url(imdb_id))

    def download(self):
        """Clicks the download button for the current OpenSubtitles page."""
        page_type = self.detect_page_type()

        if page_type == 0:
            # Subtitle not found for this movie
            print('Subtitle not found for this movie')

        elif page_type == 1:
            # Single subtitle page
            if self.xpath_exists(el.SINGLE_DOWNLOAD_LINK):
                self.driver.find_element(By.XPATH, el.SINGLE_DOWNLOAD_LINK).click()
            else:
                print('Download button not found')

        elif page_type == 2:
            # Multiple subtitle page
            if self.xpath_exists(el.MULTIPLE_PAGE_DOWNLOAD_LINK):
                self.driver.find_element(By.XPATH, el.MULTIPLE_PAGE_DOWNLOAD_LINK).click()
            else:
                print('Download button not found')

        else:
            # Unexpected page
            print('Unexpected page type')
