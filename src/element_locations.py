#!/usr/bin/env python3

#* xpath
# single
SINGLE_FILE_NAME = '//a[contains(@href, "/download/nfo")]'
SINGLE_DOWNLOAD_LINK =  '//a[contains(@href, "https://dl.opensubtitles.org/en/download/sub/")]'
SINGLE_UPLOADER_NICKNAME = '//a[contains(@href, "/profile/iduser-")]'
SINGLE_UPLOADER_RANK = '//img[contains(@src, "/gfx/icons/ranks/")]'

# multiple
MULTIPLE_PAGE_DOWNLOAD_LINK = '/html/body/div[1]/form/table/tbody/tr[2]/td[5]/a'
MULTIPLE_UPLOADER_RANK = '//img[contains(@src, "//static.opensubtitles.org/gfx/icons/ranks/")]'
MULTIPLE_UPLOADER_LINK = '//a[contains(@href, "/en/profile/iduser-")]'

#* css selector
# single
SINGLE_MOVIE_NAME = 'img[itemprop="image"]'
SINGLE_SUBTITLE_FEATURES = '#subtitles_body > div.content > div:nth-child(11) > div:nth-child(4) > div:nth-child(3)'
SINGLE_DATETIME = 'time[itemprop="datePublished"]'
SINGLE_FPS = '#subtitles_body > div.content > div:nth-child(11) > div:nth-child(4) > div:nth-child(7) > fieldset > div:nth-child(9)'

# multiple
MULTIPLE_FILE_NAME = 'td[class="sb_star_even"]'
