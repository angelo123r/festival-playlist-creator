# your_app/management/commands/scrape_data.py

from django.core.management.base import BaseCommand
from festivalPlaylistApp.get_artist2 import scrape_page

class Command(BaseCommand):
    help = 'Scrapes data from website and imports it into the database'

    def handle(self, *args, **kwargs):
        for page_num in range(1, 11):
            page_url = f"https://www.musicfestivalwizard.com/all-festivals/page/{page_num}/"
            scrape_page(page_url)
        self.stdout.write(self.style.SUCCESS('Data successfully scraped and imported.'))
