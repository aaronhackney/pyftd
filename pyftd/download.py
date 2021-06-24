import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDDownload:
    """
    Download various files from the FTD Appliance
    """

    @FTDAPIWrapper()
    def download_disk_file(self, file_name: str) -> dict:
        """
        Given a filename, return the file from the FTD directory /ngfw/var/cisco/deploy/pkg/diskfiles/
        :param file_name: str
        """
        return self.swagger_client.Download.getdownloaddiskfile(objId=file_name).result()
