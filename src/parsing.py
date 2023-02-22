#!/usr/bin/env python3

# import libraries
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import src.element_locations as el

class ParseResult:
    # get subtitle info
    # if page contains table, get first results info

    def __init__(self, source, page_type: int):
        self.source = source
        self.page_type = page_type

        # there is no exact element for single result page (page type 1)
        # get table element if multiple results (page type 2)
        if self.page_type == 2:
            # get first row element
            table = self.source.find_element(By.ID, 'search_results')
            self.first_row = table.find_elements(By.TAG_NAME, 'tr')[1]
            self.elements = self.first_row.find_elements(By.TAG_NAME, 'td')

    def handle_no_such_element(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except NoSuchElementException:
                return None
        
        return wrapper

    @property
    @handle_no_such_element
    def movie_name(self) -> str:
        """Get the name of the movie

        Returns:
            str: The name of the movie.
        """
        
        # On a single result page, the movie name can be found using the CSS_SELECTOR for the element.
        # The element contains the movie name and 'Download' string, so it must be split to get the name only.
        if self.page_type == 1:
            return self.source.find_element(By.CSS_SELECTOR, el.SINGLE_MOVIE_NAME).get_attribute('title').split(' - Download')[0]

        # On multiple result pages, the movie name can be found by getting the first column of the table,
        # which contains the name of the movie. The name is followed by the release year, so it needs to be trimmed.
        elif self.page_type == 2:
            return self.elements[0].text.split('\n')[0][:-7]

        # If there is no search result, returns None.
        else:
            return None

    @property
    @handle_no_such_element
    def movie_year(self) -> int:
        """Get the year of the movie
        
        Returns:
            int: The year of the movie.
        """
        if self.page_type == 1:
            # For single result pages, the year is the third-to-last word in the h2 tag
            return int(self.source.find_element(By.TAG_NAME, 'h2').text.split()[-3][1:-1])

        elif self.page_type == 2:
            # For multiple result pages, the year is the last 4 characters of the first column of the first row
            return int(self.elements[0].text.split('\n')[0][-5:-1])

        else:
            # If the page type is unknown, return None
            return None

    @property
    @handle_no_such_element
    def file_name(self) -> str:
        """Get movie file name

        Returns:
            str: file name
        """
        if self.page_type == 1:
            # If it's a single result page, get the file name from the corresponding element
            return self.source.find_element(By.XPATH, el.SINGLE_FILE_NAME).text

        elif self.page_type == 2:
            # If it's a multiple results page, get the file name from the first element of the first row
            # If the first element has a span tag, get the title attribute of the span tag
            # Otherwise, get the file name from the second line of the text in the first row
            elem = self.elements[0].find_elements(By.TAG_NAME, 'span')
            if elem:
                return elem[0].get_attribute('title')
            else:
                return self.source.find_element(By.CSS_SELECTOR, el.MULTIPLE_FILE_NAME).text.split('\n')[1]

        else:
            return None

    @property
    @handle_no_such_element
    def subtitle_features(self) -> dict:
        """Get subtitle features.

        Returns:
            dict: A dictionary containing the following keys:
                - trusted_source: a boolean indicating if the subtitle is from a trusted source.
                - hearing_impaired: a boolean indicating if the subtitle is for the hearing impaired.
                - hd: a boolean indicating if the subtitle is for a high-definition movie.
                - machine_translated: a boolean indicating if the subtitle is machine translated.
                - foreign_parts_only: a boolean indicating if the subtitle is for foreign parts only.
        """
        # Initialize an empty list for the images
        images = list()

        if self.page_type == 1:
            # For a single result page, find the subtitle features in the CSS selector and get the images
            elem = self.source.find_element(By.CSS_SELECTOR, el.SINGLE_SUBTITLE_FEATURES)
            images = elem.find_elements(By.TAG_NAME, 'img')

        elif self.page_type == 2:
            # For multiple result pages, find the subtitle features in the first row and get the images
            images = self.first_row.find_elements(By.TAG_NAME, 'img')

        # Create a list of the alt attributes for each image
        subtitle_features = [img.get_attribute('alt') for img in images]

        # Define a function to check if a string is a substring of any element in the subtitle_features list
        find_feature = lambda string: any(string in elem for elem in subtitle_features)

        # Return a dictionary of the subtitle features
        return {
            'trusted_source'    : find_feature('trusted source'),
            'hearing_impaired'  : find_feature('hearing impaired'),
            'hd'                : find_feature('high-definition movie'),
            'machine_translated': find_feature('machine translated'),
            'foreign_parts_only': find_feature('Foreign Parts Only')
        }

    @property
    @handle_no_such_element
    def upload_datetime(self) -> str:
        """Gets the upload datetime in ISO 8601 format.

        Returns:
            str: A string representing the upload datetime in the format "YYYY-MM-DDTHH:MM:SSZ".
        """
        if self.page_type == 1:
            return self.source.find_element(By.CSS_SELECTOR, el.SINGLE_DATETIME).get_attribute('datetime')
        
        elif self.page_type == 2:
            return self.elements[3].find_element(By.TAG_NAME, 'time').get_attribute('datetime')

        else:
            return None

    @property
    @handle_no_such_element
    def upload_date(self) -> str:
        """Get the human-readable upload date of the subtitle.

        Returns:
            str: The upload date in a human-readable format.
        """
        if self.page_type == 1:
            # On a single subtitle page, the upload date is displayed as the title attribute of the datetime element.
            return self.source.find_element(By.CSS_SELECTOR, el.SINGLE_DATETIME).get_attribute('title')

        elif self.page_type == 2:
            # On a search results page, the upload date is displayed as the title attribute of the time element within the fourth td element.
            return self.elements[3].find_element(By.TAG_NAME, 'time').get_attribute('title')

        else:
            return None

    @property
    @handle_no_such_element
    def fps(self) -> str:
        """Get fps of movie

        Returns:
            str: fps
        """
        if self.page_type == 1:
            # For single page, find the element with CSS selector
            # and extract fps if it's found in the text
            elem = self.source.find_elements(By.CSS_SELECTOR, el.SINGLE_FPS)
            if elem:
                elem = elem[0]
                text_list = elem.text.split('\n')
                fps_elem = [string for string in text_list if 'FPS' in string]

                # If 'fps' is found, extract it and return
                return fps_elem[0][-10:-4] if fps_elem else None

        elif self.page_type == 2:
            # For multiple pages, find the element with tag name and return its text
            elem = self.elements[3].find_elements(By.TAG_NAME, 'span')
            if elem:
                return elem[0].text

        else:
            return None

    @property
    @handle_no_such_element
    def download_link(self) -> str:
        """Get download link of subtitle

        Returns:
            str: subtitle download link
        """
        if self.page_type == 1:
            return self.source.find_element(By.XPATH, el.SINGLE_FILE_NAME).get_attribute('href')

        elif self.page_type == 2:
            return self.elements[4].find_element(By.TAG_NAME, 'a').get_attribute('href')

        else:
            return None

    @property
    @handle_no_such_element
    def subtitle_id(self) -> str:
        """Get the unique ID of the subtitle.

        Returns:
            str: The subtitle ID, which is extracted from the download link.
        """
        # If download link is found, extract the ID from it
        if self.download_link:
            return self.download_link.split('/')[-1]

        # If download link is not found, return None
        else:
            return None

    @property
    @handle_no_such_element
    def uploader_nickname(self) -> str:
        """Get the uploader's nickname for the subtitle.

        Returns:
            str: Uploader's nickname.

        Raises:
            NoSuchElementException: If the uploader nickname element is not found.
        """
        if self.page_type == 1:
            # Find the uploader nickname element on a single subtitle page
            return self.source.find_element(By.XPATH, el.SINGLE_UPLOADER_NICKNAME).text

        elif self.page_type == 2:
            # Find the uploader nickname element on a search results page
            return self.elements[8].text

        else:
            # If the page type is not supported, return None
            return None

    @property
    @handle_no_such_element
    def uploader_rank(self) -> str:
        """Get uploader rank from the page

        Returns:
            str: The uploader rank as a string or None if not found.
        """
        if self.page_type == 1:
            # Get the uploader rank element from the page
            elem = self.source.find_elements(By.XPATH, el.SINGLE_UPLOADER_RANK)
            return elem[0].get_attribute('title') if elem else None

        elif self.page_type == 2:
            # Get the uploader rank element from the page
            return self.elements[0].find_element(By.XPATH, el.MULTIPLE_UPLOADER_RANK).get_attribute('title')

        else:
            return None

    @property
    @handle_no_such_element
    def uploader_link(self) -> str:
        """Get uploader link.

        Returns:
            str: The uploader link, or None if not found.
        """
        # If the page type is 1, look for the single uploader nickname link.
        # If found, return the href attribute.
        if self.page_type == 1:
            return self.source.find_element(By.XPATH, el.SINGLE_UPLOADER_NICKNAME).get_attribute('href')

        # If the page type is 2, look for the uploader link in the first element.
        # If found, return the href attribute.
        elif self.page_type == 2:
            return self.elements[0].find_element(By.XPATH, el.MULTIPLE_UPLOADER_LINK).get_attribute('href')

        # If the page type is not recognized, return None.
        else:
            return None

    @property
    @handle_no_such_element
    def uploader_id(self) -> str:
        """Get the unique ID of the uploader's profile.

        Returns:
            str: The uploader ID, if available. Otherwise, None.
        """
        if self.uploader_link:
            # The uploader ID is the last part of the URL, after the last hyphen.
            return self.uploader_link.split('-')[-1]
        else:
            return None

    @property
    def results(self) -> dict:
        """Results of parsing

        Returns:
            dict: get all parsing variables in dictionary
        """
        return {
            'movie_name'       : self.movie_name,
            'movie_year'       : self.movie_year,
            'file_name'        : self.file_name,
            'subtitle_features': self.subtitle_features,
            'upload_datetime'  : self.upload_datetime,
            'upload_date'      : self.upload_date,
            'fps'              : self.fps,
            'download_link'    : self.download_link,
            'subtitle_id'      : self.subtitle_id,
            'uploader_nickname': self.uploader_nickname,
            'uploader_rank'    : self.uploader_rank,
            'uploader_link'    : self.uploader_link,
            'uploader_id'      : self.uploader_id
        }