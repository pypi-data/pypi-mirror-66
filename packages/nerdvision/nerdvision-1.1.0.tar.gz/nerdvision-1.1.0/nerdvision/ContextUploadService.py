import logging
import requests
from nerdvision import settings

from six.moves.urllib.parse import quote

our_logger = logging.getLogger("nerdvision")


class ContextUploadService(object):
    def __init__(self):
        self.url = settings.get_context_url()
        self.api_key = settings.get_setting("api_key")

    def send_event(self, event_snapshot, bp, watches, session_id, log_msg=None):
        try:
            our_logger.debug("Sending snapshot to %s", self.url)
            snapshot_as_dict = event_snapshot.as_dict()
            snapshot_as_dict['named_watches'] = [watcher.as_dict() for watcher in watches]
            snapshot_as_dict['breakpoint'] = bp

            encoded_log_msg = None
            if log_msg is not None:
                snapshot_as_dict['log_msg'] = log_msg
                encoded_log_msg = quote(log_msg)

            our_logger.debug("Sending event snapshot for breakpoint %s", bp['breakpoint_id'])

            if settings.is_context_debug_enabled():
                our_logger.debug(snapshot_as_dict)

            self.send_context(bp, session_id, "snapshot", snapshot_as_dict, encoded_log_msg)
        except Exception:
            our_logger.exception("Error while sending event snapshot %s", self.url)

    def send_context(self, bp, session_id, type, snapshot_as_dict, log_msg=None):
        url = self.url + "?breakpoint_id=" + bp['breakpoint_id'] + "&workspace_id=" + bp['workspace_id'] + "&type=" + type

        if log_msg is not None:
            url = url + "&log_msg=" + log_msg

        response = requests.post(
            url=url,
            auth=(session_id, self.api_key), json=snapshot_as_dict)
        json = response.json()
        our_logger.debug("Context response: %s", json)
        response.close()

    def send_log_event(self, bp, log_msg, session_id):
        try:
            log_cxt = {
                'log_msg': log_msg,
                'breakpoint': bp
            }
            self.send_context(bp, session_id, "log_point", log_cxt, quote(log_msg))
        except Exception:
            our_logger.exception("Error while sending event snapshot %s", self.url)
