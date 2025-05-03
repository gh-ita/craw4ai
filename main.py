import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from bs4 import BeautifulSoup

async def link_crawler():
    '''Web crawler returns the html page content 
    '''
    browser_cfg = BrowserConfig(
        browser_type="chromium",
        headless=True,
        verbose=True
    )
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        page_timeout=90000
    )
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun("https://www.ensam-casa.ma/", config=run_conf)
    if result.success:
        clnd_html = result.cleaned_html
        return clnd_html

def find_formation_list_items(html):
    '''the method that extracts the nodes nested in an unordered list that contain the word 'Formation', it returns their child nodes
    '''
    soup = BeautifulSoup(html, "html.parser")
    formation_items = []
    
    # Find all list items (li) that contain the word "formation"
    for li in soup.find_all('li'):
        if "formation" in li.get_text(strip=True).lower():
            # Only include those that are inside a ul parent
            if li.parent and li.parent.name == 'ul':
                formation_items.append(li)
    
    return formation_items

def get_child_nodes(list_items):
    result = []
    
    for li in list_items:
        # Create a dictionary to store the list item and its children
        item_data = {
            "parent": li.prettify(),
            "children": []
        }
        
        # Get all immediate children of the list item
        for child in li.children:
            if child.name:  # Check if it's an HTML element and not just text
                item_data["children"].append(child.prettify())
        
        result.append(item_data)
    
    return result

if __name__ == "__main__":
    html = asyncio.run(link_crawler())
    formation_items = find_formation_list_items(html)
    
    print(f"Found {len(formation_items)} list items containing 'formation' inside ul tags\n")
    
    # Print parent li elements containing "formation"
    print("PARENT LIST ITEMS:")
    for item in formation_items:
        print(item.prettify())
        print("-" * 80)
    
    # Get and print child nodes
    print("\nCHILD NODES OF EACH LIST ITEM:")
    child_nodes = get_child_nodes(formation_items)
    for idx, item_data in enumerate(child_nodes, 1):
        print(f"\nItem {idx} children:")
        if item_data["children"]:
            for child in item_data["children"]:
                print(child)
                print("-" * 40)
        else:
            print("No HTML element children found (might contain only text)")