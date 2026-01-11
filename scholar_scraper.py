"""
Google Scholar爬虫模块
负责自动搜索、提取和解析BibTeX数据
"""

import time
import random
import re
from typing import Optional, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote_plus
import logging

from parser import parse_bibtex_string


class ScholarScraper:
    """Google Scholar爬虫类"""
    
    def __init__(self, headless: bool = False, delay_range: tuple = (2, 4)):
        """
        初始化爬虫
        
        Args:
            headless: 是否使用无头模式
            delay_range: 延迟范围（秒），格式为(min, max)
        """
        self.headless = headless
        self.delay_range = delay_range
        self.driver = None
        self.logger = logging.getLogger(__name__)
        
    def _init_driver(self):
        """初始化Chrome WebDriver"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # 反爬虫设置
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 禁用图片加载以加速
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 隐藏webdriver特征
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
        
        self.logger.info("Chrome WebDriver initialized")
    
    def _random_delay(self):
        """随机延迟"""
        delay = random.uniform(self.delay_range[0], self.delay_range[1])
        time.sleep(delay)
    
    def search_paper(self, title: str) -> Optional[Dict]:
        """
        搜索论文并获取BibTeX信息
        
        Args:
            title: 论文标题
            
        Returns:
            BibTeX字典，如果失败返回None
        """
        if self.driver is None:
            self._init_driver()
        
        try:
            # 构建搜索URL
            encoded_title = quote_plus(title)
            search_url = f"https://scholar.google.com/scholar?q={encoded_title}"
            
            self.logger.info(f"Searching: {title}")
            self.driver.get(search_url)
            
            # 检查是否遇到验证码
            if self._check_captcha():
                self.logger.warning("CAPTCHA detected! Please solve it manually.")
                input("Press Enter after solving CAPTCHA...")
            
            self._random_delay()
            
            # 查找第一个搜索结果的Cite按钮
            cite_button = self._find_cite_button()
            if cite_button is None:
                self.logger.warning(f"No cite button found for: {title}")
                return None
            
            # 点击Cite按钮
            cite_button.click()
            self._random_delay()
            
            # 在弹出的对话框中找到BibTeX链接
            bibtex_link = self._find_bibtex_link()
            if bibtex_link is None:
                self.logger.warning(f"No BibTeX link found for: {title}")
                return None
            
            # 点击BibTeX链接
            bibtex_url = bibtex_link.get_attribute('href')
            self.driver.get(bibtex_url)
            self._random_delay()
            
            # 提取BibTeX内容
            bibtex_text = self._extract_bibtex_text()
            if bibtex_text is None:
                self.logger.warning(f"Failed to extract BibTeX for: {title}")
                return None
            
            # 解析BibTeX
            bibtex_dict = parse_bibtex_string(bibtex_text)
            self.logger.info(f"Successfully retrieved BibTeX for: {title}")
            
            return bibtex_dict
            
        except Exception as e:
            self.logger.error(f"Error searching paper '{title}': {str(e)}")
            return None
    
    def _check_captcha(self) -> bool:
        """检查是否遇到验证码"""
        try:
            captcha_element = self.driver.find_element(By.ID, "gs_captcha_f")
            return captcha_element is not None
        except NoSuchElementException:
            return False
    
    def _find_cite_button(self) -> Optional[webdriver.remote.webelement.WebElement]:
        """查找第一个搜索结果的Cite按钮"""
        try:
            # 等待搜索结果加载
            wait = WebDriverWait(self.driver, 10)
            
            # 尝试多种选择器
            selectors = [
                (By.CSS_SELECTOR, ".gs_or_cit.gs_or_btn.gs_nph"),
                (By.CSS_SELECTOR, ".gs_or_cit"),
                (By.XPATH, "//a[contains(@aria-label, 'Cite')]"),
                (By.XPATH, "//div[@class='gs_ri']//a[contains(text(), 'Cite')]")
            ]
            
            for by, selector in selectors:
                try:
                    cite_button = wait.until(
                        EC.presence_of_element_located((by, selector))
                    )
                    if cite_button:
                        return cite_button
                except TimeoutException:
                    continue
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding cite button: {str(e)}")
            return None
    
    def _find_bibtex_link(self) -> Optional[webdriver.remote.webelement.WebElement]:
        """在引用对话框中查找BibTeX链接"""
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # 尝试多种选择器
            selectors = [
                (By.LINK_TEXT, "BibTeX"),
                (By.PARTIAL_LINK_TEXT, "BibTeX"),
                (By.XPATH, "//a[contains(text(), 'BibTeX')]"),
                (By.CSS_SELECTOR, "a[href*='scholar.bib']")
            ]
            
            for by, selector in selectors:
                try:
                    bibtex_link = wait.until(
                        EC.presence_of_element_located((by, selector))
                    )
                    if bibtex_link:
                        return bibtex_link
                except TimeoutException:
                    continue
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding BibTeX link: {str(e)}")
            return None
    
    def _extract_bibtex_text(self) -> Optional[str]:
        """从BibTeX页面提取文本"""
        try:
            # BibTeX通常在<pre>标签中
            pre_element = self.driver.find_element(By.TAG_NAME, "pre")
            bibtex_text = pre_element.text
            
            if bibtex_text and bibtex_text.strip():
                return bibtex_text.strip()
            
            # 如果<pre>标签为空，尝试从body获取
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            if body_text and body_text.strip().startswith('@'):
                return body_text.strip()
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error extracting BibTeX text: {str(e)}")
            return None
    
    def batch_search(self, titles: list, progress_callback=None) -> Dict[str, Optional[Dict]]:
        """
        批量搜索论文
        
        Args:
            titles: 论文标题列表
            progress_callback: 进度回调函数，接受(current, total)参数
            
        Returns:
            字典，键为标题，值为BibTeX字典或None
        """
        results = {}
        total = len(titles)
        
        for i, title in enumerate(titles, 1):
            result = self.search_paper(title)
            results[title] = result
            
            if progress_callback:
                progress_callback(i, total)
            
            # 每10次搜索后增加额外延迟
            if i % 10 == 0:
                self.logger.info("Taking a longer break to avoid rate limiting...")
                time.sleep(random.uniform(5, 10))
        
        return results
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logger.info("Chrome WebDriver closed")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
