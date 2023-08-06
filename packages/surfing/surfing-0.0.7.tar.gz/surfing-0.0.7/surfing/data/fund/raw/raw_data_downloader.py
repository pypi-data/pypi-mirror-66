from .rq_raw_data_downloader import RqRawDataDownloader
from .em_raw_data_downloader import EmRawDataDownloader
from .web_raw_data_downloader import WebRawDataDownloader

class RawDataDownloader(object):
    def __init__(self, rq_license):
        self.rq_downloader = RqRawDataDownloader(rq_license)
        self.web_downloader = WebRawDataDownloader()
        self.em_downloader = EmRawDataDownloader()

    def download(self, start_date, end_date):
        self.rq_downloader.download_all(start_date, end_date)
        self.web_downloader.download_all(start_date, end_date)
        self.em_downloader.download_all(start_date, end_date)
