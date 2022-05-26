import logging
import requests
from requests.auth import HTTPBasicAuth

from redash.destinations import *
from redash.utils import json_dumps
from redash.serializers import serialize_alert


class Webhook(BaseDestination):
    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["url"],
            "secret": ["password", "url"],
        }

    @classmethod
    def icon(cls):
        return "fa-bolt"

    def notify(self, alert, query, user, new_state, app, host, options):
        try:
            logging.error("!!!!!change post webhook will call jandi11")
            data = {
                "event": "alert_state_change",
                "alert": serialize_alert(alert, full=False),
                "url_base": host,
                "body": alert.custom_subject
            }

            data["alert"]["description"] = alert.custom_body
            data["alert"]["title"] = alert.custom_subject
            logging.error("!!!!!webhook will call jandi22")
            logging.error(options.get("url"))

            headers = {"Content-Type": "application/json", "Accept":"application/vnd.tosslab.jandi-v2+json"}
            # auth = (
            #     HTTPBasicAuth(options.get("username"), options.get("password"))
            #     if options.get("username")
            #     else None
            # )
            auth = None
            resp = requests.request("POST", options.get("url"), headers=headers, data=json_dumps(data))
            # resp = requests.post(
            #     options.get("url"),
            #     data=json_dumps(data),
            #     auth=auth,
            #     headers=headers,
            #     timeout=50,
            # )
            logging.error(json_dumps(data))
            logging.error("!!!!!webhook will call jandi will print body")
            logging.error(resp.text)
            
            logging.error(resp.body)
            
            if resp.status_code != 200:
                logging.error(
                    "webhook send ERROR. status_code => {status}".format(
                        status=resp.status_code
                    )
                )
        except Exception:
            logging.exception("webhook send ERROR.")


register(Webhook)
