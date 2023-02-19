#!/usr/bin/env python3

# import libraries
import os
import json
from time import sleep
from selenium.webdriver.common.by import By

from .webdriver import Driver

class MainOperations(Driver):
    """A collection of useful methods for web automation using Selenium WebDriver.

    This class extends the `Driver` class, which is responsible for setting up the Selenium WebDriver.

    Attributes:
        args (argparse.Namespace): The command line arguments parsed by argparse.
        driver (selenium.webdriver.remote.webdriver.WebDriver): The Selenium WebDriver instance.

    Methods:
        process_path() -> str:
            Check if the given path to save process data is absolute or relative. If it is absolute, return the path as is. 
            If it is relative, join the main folder path to the given path and return the new path.

        create_process_file() -> None:
            Create a folder for saving the process data, whose name can be specified by the user. If the folder 
            doesn't already exist, it will be created. If the process.json file doesn't exist, it will be created.

        save_process(data: dict) -> None:
            Save information about the last saved movie, including its imdb_id and the results of its parsing.

        last_movie(process_path: str) -> dict or None:
            Get information about the last downloaded movie, including its imdb_id and the results of its parsing, 
            or None if the process file is not found.

        xpath_exists(xpath: str) -> bool:
            Find element by XPath and check if it exists or not on the page. This method can be used to check the 
            existence of an element before performing any action on it.

        element(xpath: str) -> selenium.webdriver.remote.webelement.WebElement or None:
            Check if an element exists on the page using the XPath expression provided, and return it if the element 
            is found. If the element does not exist, returns None.

        detect_page_type() -> int:
            Detect the type of the current page. Returns an integer representing the page type. 0 for empty page, 
            1 for a single result page, 2 for a page with multiple results, 3 for a CAPTCHA page, and -1 for a backup 
            page.

        detect_captcha() -> bool:
            Check if the current page is a CAPTCHA page. Returns True if the page is a CAPTCHA page, False otherwise.

        wait_while_downloading(subtitle_id: str) -> None:
            Wait for a file to finish downloading before continuing.

        change_file_name(self, subtitle_id: str, imdb_id: str) -> None:
            Rename a downloaded subtitle file using the provided IMDb ID.

    """

    def __init__(self, args):
        """Initialize an instance of MainOperations Class.
        
        Args:
            args (argparse object): the command line arguments parsed by argparse
        """
        super().__init__(args),
        self.driver = self.webdriver()

    @property
    def process_path(self) -> str:
        """Check if the given path to save process data is absolute or relative. 
        If it is absolute, return the path as is. 
        If it is relative, join the main folder path to the given path and return the new path.

        Returns:
            str: The folder path where process data will be saved.
        """
        if os.path.isabs(self.args.save_process_path):
            return f'{self.args.save_process_path}'

        else:
            return f"{os.path.abspath(os.path.join(os.path.abspath('.'), self.args.save_process_path))}"

    def create_process_file(self):
        """Create a folder for saving the process data, whose name can be specified by the user. 
        If the folder doesn't already exist, it will be created. If the process.json file doesn't 
        exist, it will be created.
        """
        dir_path = self.process_path
        process_file = f'{dir_path}/process.json'
        
        # Create the folder if it doesn't already exist
        os.makedirs(dir_path, exist_ok=True)

        # Check if process.json file exists; if not, create it
        if os.path.exists(process_file) is False:
            with open(process_file, 'w') as file:
                file.write('')

    def save_process(self, data: dict):
        """Save information about the last saved movie, including its imdb_id and the results of its parsing.

        Args:
            data (dict): A dictionary containing the imdb_id, download status, and parsing results for the movie.
        """
        file_path = f'{self.process_path}/process.json'
        if self.args.save_process:
            with open(file_path, 'r') as file:
                try:
                    existing_data = json.load(file)

                except json.decoder.JSONDecodeError:
                    existing_data = list()

            existing_data.append(data)

            with open(file_path, 'w', encoding='utf8') as file:
                json.dump(existing_data, file, indent=4)

    @staticmethod
    def last_movie(process_path):
        """Get information about the last downloaded movie.

        Args:
            process_path (str): The path to the folder where the process data is stored.

        Returns:
            dict or None: A dictionary containing information about the last downloaded movie, 
            including its imdb_id and the results of its parsing, or None if the process file is not found.
        """
        file_path = f'{process_path}/process.json'
        try:
            with open(file_path, 'r') as file:
                try:
                    result = json.load(file)
                    return result[-1] if result else result
                    
                except json.decoder.JSONDecodeError:
                    return None
            
        except FileNotFoundError:
            return None

    def xpath_exists(self, xpath: str) -> bool:
        """Find element by XPath and check if it exists or not on the page.
        This method can be used to check the existence of an element before performing any action on it.

        Args:
            xpath (str): XPath expression to locate the element

        Returns:
            bool: True if the element exists, False otherwise
        """
        return True if len(self.driver.find_elements(By.XPATH, xpath)) else False

    def element(self, xpath: str):
        """Check if an element exists on the page using the XPath expression provided,
        and return it if the element is found. If the element does not exist, returns None.

        Args:
            xpath (str): XPath expression to locate the element

        Returns:
            selenium.webdriver.remote.webelement.WebElement or None: The element found, or None if not found
        """
        if self.xpath_exists(xpath):
            return self.driver.find_element(By.XPATH, xpath)

        else:
            return None

    def detect_page_type(self) -> int:
        """Detect the type of the current page.
        
        Returns:
            int: An integer representing the page type. 0 for empty page, 1 for a single result page, 2 for a page with 
            multiple results, 3 for a CAPTCHA page, and -1 for a backup page.
        """

        # The length of the URL can be used to differentiate between single and multiple result pages.
        url_len = len(self.driver.current_url.split('/'))

        # Detect a single result page.
        if url_len == 7:
            return 1

        # Detect a page with multiple results.
        elif url_len == 12:

            # Check if the page is empty, since the URL is the same for empty and multiple result pages.
            if len(self.driver.find_elements(By.ID, 'search_results')) == 0:
                return 0 

            return 2

        # Detect a backup page.
        elif self.element('/html/body/pre/text()') == 'Site will be online soon. We are doing some necessary backups and upgrades. Thanks for understanding.':
            return -1

    def detect_captcha(self) -> bool:
        """
        Check if the current page is a CAPTCHA page.
        
        Returns:
            bool: True if the page is a CAPTCHA page, False otherwise.
        """
        return True if 'captcha/redirect' in self.driver.current_url else False

    def wait_while_downloading(self, subtitle_id: str):
        """
        Wait for a file to finish downloading before continuing.
        
        Args:
            subtitle_id (str): The ID of the subtitle file to wait for.
        """
        # Define a lambda function to check if the file with the given subtitle ID exists in the download directory
        find_id = lambda _id: any(_id in elem for elem in os.listdir(self.download_path))
        
        while True:
            # Wait for a short amount of time before checking if the file has finished downloading
            sleep(.2)
            if find_id(subtitle_id):
                return False

    def change_file_name(self, subtitle_id: str, imdb_id: str):
        """
        Rename a downloaded subtitle file using the provided IMDb ID.
        
        Args:
            subtitle_id (str): The ID of the subtitle file to rename.
            imdb_id (str): The IMDb ID to use as the new name for the file.
        """
        dir_path = self.download_path
        
        # Find the filename of the downloaded subtitle file with the given ID
        file_name = [elem for elem in os.listdir(dir_path) if subtitle_id in elem][0]
        file_path = os.path.join(dir_path, file_name)
        
        # Create the new filename using the provided IMDb ID and rename the file
        new_file = f'{dir_path}/{imdb_id}.zip'
        os.rename(file_path, new_file)
