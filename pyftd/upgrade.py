import logging
from .base import FTDAPIWrapper
from typing import Optional

log = logging.getLogger(__name__)


class FTDUpgrade:
    """
    Set platform and control plane settings hostname, syslog, ntp, aaa, systeminfo
    """

    ################################
    # NTP Settings
    #
    pass