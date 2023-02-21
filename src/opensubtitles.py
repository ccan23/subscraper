#!/usr/bin/env python3

# import libraries
from selenium.webdriver.common.by import By

import src.element_locations as el
from .main_operations import MainOperations
from .parsing import ParseResult

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

    def execute(self, counter=0):
            """
            Downloads subtitles for the given imdb_id(s) by parsing the corresponding web pages on OpenSubtitles.
            
            Args:
                counter (int): The index of the first imdb_id to process. Default is 0.
                
            Returns:
                None
                
            Raises:
                Exception: If the webdriver cannot be started or if there is an error while downloading or parsing the subtitle.
            """
            
            # Check if imdb_id has single element or multiple elements
            if len(self.args.imdb_id) > 1:
                # If length is more than 1 it should be continued from last downloaded subtitle
                # so get the index of last downloaded subtitle and continue from it.
                downloaded_list = MainOperations.last_movie(self.process_path)
                if downloaded_list:
                    counter = downloaded_list['index'] + 1
                else:
                    counter = 0        

            # Process each imdb_id starting from the given counter
            for imdb_id in self.args.imdb_id[counter:]:
                # Launch the web page for the given imdb_id
                self.driver.get(self.url(imdb_id))

                # Detect the type of page (e.g. movie, TV show, etc.)
                page_type = self.detect_page_type()

                # Check if the page has a subtitle to download
                if page_type > 0:
                    # Parse the page to extract the subtitle information
                    parsing = ParseResult(
                        source=self.driver.find_element(By.TAG_NAME, 'html'),
                        page_type=page_type
                    )

                    # Add the imdb_id to the parse results
                    results = parsing.results
                    results['imdb_id'] = imdb_id

                    # Print the downloading file
                    print(f"{counter}: {results['imdb_id']} ({results['movie_name']}) (page type: {page_type}) downloading..")

                    # Download the subtitle file
                    self.download()

                    # Check if CAPTCHA has been detected
                    if self.detect_captcha():
                        print('Warning: Caught by CAPTCHA. Restarting..')
                        del self.args.imdb_id
                        self.driver.quit()
                        self.execute(counter=counter)

                    # If CAPTCHA is not detected, continue processing the subtitle
                    else:
                        # Wait until the download is complete (if safe_downloading flag is True)
                        if self.args.safe_downloading:
                            self.wait_while_downloading(results['subtitle_id'])

                        # Change the subtitle file name (if change_file_names flag is True)
                        if self.args.change_file_names:
                            self.change_file_name(results['subtitle_id'], results['imdb_id'])

                        # Save the process to process.json (if save_process flag is True)
                        if self.args.save_process:
                            data = {
                                'index': counter,
                                'download_status': True,
                                'parsing_results': results
                            }
                            self.save_process(data=data)

                # If no subtitle found for the imdb_id, log it as an error
                else:
                    print(f'There is no subtitle for {imdb_id}: passed')
                    data = {
                        'index': counter,
                        'download_status': False,
                        'parsing_results': imdb_id
                    }
                    self.save_process(data=data)

                counter += 1