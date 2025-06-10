import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os

# URL of the website containing PDF links
URL = "https://rochesterham.org/newsletters.htm"
SAVE_FOLDER = "/Users/ofarawi/Desktop/RagArchAsync"


# Create a folder to save the downloaded PDFs
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Function to fetch all PDF links from the webpage
async def get_pdf_links():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            links = soup.find_all('a', href=True)
            pdf_links = [
                "https://rochesterham.org/" + link['href']
                for link in links if link['href'].endswith('.pdf')
            ]
            return pdf_links

# Function to download a single PDF file
async def download_pdf(session, url):
    filename = url.split("/")[-1]
    save_path = os.path.join(SAVE_FOLDER, filename)

    async with session.get(url) as response:
        if response.status == 200:
            content = await response.read()
            with open(save_path, 'wb') as f:
                f.write(content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {filename}")

# Main function to run everything
async def main():
    pdf_links = await get_pdf_links()
    async with aiohttp.ClientSession() as session:
        tasks = [download_pdf(session, url) for url in pdf_links]
        await asyncio.gather(*tasks)

# Entry point to run the async code
if __name__ == "__main__":
    asyncio.run(main())