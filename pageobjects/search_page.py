from decimal import Decimal
from typing import List, Final

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from pageobjects.base_page import BasePage
from dataclasses import dataclass
import os

@dataclass
class ProductInfo:
    name: str
    price: Decimal

class SearchPage(BasePage):

    host: str = os.environ['HOST']

    def get_url(self) -> str:
        return f'{SearchPage.host}/demo/index.php?route=product/search'

    def get_search_criteria_field(self) -> WebElement:
        """Метод получения поля критериев поиска"""
        return self.driver.find_element(By.ID, 'input-search')

    def get_search_field(self) -> WebElement:
        """Метод получения поля поиска"""
        return self.driver.find_element(By.NAME, 'search')

    def get_button_search_criteria(self) -> WebElement:
        """Метод получения кнопки поиска по критериям"""
        return self.driver.find_element(By.ID, 'button-search')

    def get_button_global_search(self) -> WebElement:
        """Метод получения кнопки глобального поиска"""
        return self.driver.find_element(By.CLASS_NAME, 'input-group-btn')

    def get_notification(self) -> str:
        """Получения нотификации при пустом результате поиска"""
        return self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/p[2]').text

    def clean_search_field(self):
        self.get_search_field().clear()

    def clean_search_criteria_field(self):
        self.get_search_criteria_field().clear()

    def input_search_criteria_keywords(self, keywords: str):
        """Ввод доп. критериев"""
        self.get_search_criteria_field().send_keys(keywords)

    def search_by_criteria(self, criteria: str):
        """Поиск по доп. критериям"""
        self.get_search_criteria_field().send_keys(criteria)
        self.get_button_search_criteria().click()

    def search_by_name(self, name: str):
        """Глобальный поиск"""
        self.get_search_field().send_keys(name)
        self.get_button_global_search().click()

    def search_in_description_checkbox(self):
        self.driver.find_element(By.ID, 'description').click()

    def get_decimal_price_from_str(self, price_str: str) -> Decimal:
        """Метод извлечения цены и перевода в decimal"""
        split_by_lines: List[str] = price_str.split('\n')
        first_price: List[str] = split_by_lines[0].split(' ')
        price_wo_symbols: str = first_price[0][1:].replace(',', '')
        return Decimal(price_wo_symbols)

    def get_search_results(self) -> List[ProductInfo]:
        """Возвращает список найденных моделей"""
        products: List[ProductInfo] = []
        results: List[WebElement] = self.driver.find_elements(By.CLASS_NAME, 'product-layout')

        for result in results:
            name: str = result.find_element(By.TAG_NAME, 'h4').text
            try:
                price: str = result.find_element(By.CLASS_NAME, 'price-new').text
            except NoSuchElementException:
                price: str = result.find_element(By.CLASS_NAME, 'price').text

            product = ProductInfo(name=name, price=self.get_decimal_price_from_str(price))
            products.append(product)

        return products
