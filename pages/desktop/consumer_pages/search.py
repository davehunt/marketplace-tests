# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.desktop.consumer_pages.base import Base
from pages.desktop.regions.filter import Filter


class Search(Base, Filter):
    """
    Consumer search page
    https://marketplace-dev.allizom.org/
    """

    _expand_button_locator = (By.CSS_SELECTOR, '.search-results-header-desktop .app-list-filters-expand-toggle')
    _results_locator = (By.CSS_SELECTOR, '#search-results .item.result.app-list-app')
    _applied_filters_locator = (By.CSS_SELECTOR, '.applied-filters > ol > li > a')
    _search_results_section_title_locator = (By.CSS_SELECTOR, '.search-results-header-desktop')

    def __init__(self, base_url, selenium, app_name=None):
        Base.__init__(self, base_url, selenium)
        self.app_name = app_name

    @property
    def _page_title(self):
        return '%s | Firefox Marketplace' % (self.app_name or 'Search Results')

    @property
    def applied_filters(self):
        return self.find_element(*self._applied_filters_locator).text

    @property
    def search_results_section_title(self):
        return self.find_element(*self._search_results_section_title_locator).text

    def click_expand_button(self):
        self.find_element(*self._expand_button_locator).click()

    @property
    def results(self):
        return [self.SearchResult(self.base_url, self.selenium, web_element)
                for web_element in self.find_elements(*self._results_locator)]

    class SearchResult(PageRegion):
        """provides the methods to access a search result
        self._root_element - webelement that points to a single result"""

        _screenshots_locator = (By.CSS_SELECTOR, '.previews-thumbnail')
        _install_button_locator = (By.CSS_SELECTOR, '.button.install')
        _rating_locator = (By.CSS_SELECTOR, '.stars')
        _icon_locator = (By.CSS_SELECTOR, '.icon')
        _name_locator = (By.CSS_SELECTOR, '.app-list .mkt-product-name')

        @property
        def are_screenshots_visible(self):
            return self.find_element(*self._screenshots_locator).is_displayed()

        @property
        def is_install_button_visible(self):
            return self.is_element_visible(*self._install_button_locator)

        @property
        def is_rating_visible(self):
            return self.is_element_visible(*self._rating_locator)

        @property
        def name(self):
            return self.find_element(*self._name_locator).text

        @property
        def is_icon_visible(self):
            return self.is_element_visible(*self._icon_locator)

        def click_name(self):
            name = self.name
            self.find_element(*self._name_locator).click()
            from pages.desktop.consumer_pages.details import Details
            return Details(self.base_url, self.selenium, name)
