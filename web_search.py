"""
Web Search Integration for Voice Assistant
Enables real-time web search and content retrieval
"""

import requests
from googlesearch import search
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class WebSearchEngine:
    """Web search engine with content extraction"""
    
    def __init__(self):
        self.timeout = 10
        self.max_results = 5
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Perform web search and return results"""
        try:
            results = []
            count = 0
            
            for url in search(query, num_results=num_results, advanced=True, sleep_interval=1):
                if count >= num_results:
                    break
                
                try:
                    content = self.get_page_content(url)
                    if content:
                        results.append({
                            "url": url,
                            "title": self._extract_title(url),
                            "snippet": content[:200],
                            "full_content": content
                        })
                        count += 1
                except:
                    continue
            
            logger.info(f"Web search completed for '{query}': {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return []
    
    def get_page_content(self, url: str) -> str:
        """Extract main content from webpage"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator=" ", strip=True)
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = " ".join(chunk for chunk in chunks if chunk)
            
            return text[:2000]  # Return first 2000 chars
        
        except Exception as e:
            logger.warning(f"Page content extraction error for {url}: {e}")
            return ""
    
    def _extract_title(self, url: str) -> str:
        """Extract title from URL"""
        try:
            # Simple title extraction from URL
            title = url.replace("https://", "").replace("http://", "").split("/")[0]
            return title
        except:
            return url
    
    def search_news(self, topic: str) -> List[Dict]:
        """Search for news about topic"""
        try:
            query = f"{topic} news today"
            return self.search(query, num_results=5)
        except Exception as e:
            logger.error(f"News search error: {e}")
            return []
    
    def search_weather(self, location: str) -> Dict:
        """Search weather information"""
        try:
            query = f"{location} weather today"
            results = self.search(query, num_results=1)
            
            if results:
                return {
                    "location": location,
                    "info": results[0]["snippet"],
                    "source": results[0]["url"]
                }
            return {}
        except Exception as e:
            logger.error(f"Weather search error: {e}")
            return {}
    
    def search_tutorial(self, topic: str) -> List[Dict]:
        """Search for tutorials"""
        try:
            query = f"how to {topic} tutorial"
            return self.search(query, num_results=5)
        except Exception as e:
            logger.error(f"Tutorial search error: {e}")
            return []
    
    def search_definition(self, word: str) -> Dict:
        """Search definition of word"""
        try:
            query = f"define {word}"
            results = self.search(query, num_results=1)
            
            if results:
                return {
                    "word": word,
                    "definition": results[0]["snippet"],
                    "source": results[0]["url"]
                }
            return {}
        except Exception as e:
            logger.error(f"Definition search error: {e}")
            return {}
