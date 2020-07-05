import json
import os

from notebook.base.handlers import APIHandler
from notebook.utils import url_path_join
from tornado import gen, web
import tornado

from .config import get_locale_setting
from .utils import get_installed_language_packs, get_language_pack


class TranslationHandler(APIHandler):

    @tornado.web.authenticated
    @gen.coroutine
    def get(self, locale=""):
        """
        Get a language pack by locale. If no locale is provided, it will list installed language packs.
        """
        try:
            data = [] if locale == "" else locale
            page_config = self.settings["page_config_data"]
            user_settings_dir = page_config["userSettingsDir"]
            if locale == "":
                data, message = get_installed_language_packs(get_locale_setting(user_settings_dir))
            else:
                data, message = get_language_pack(locale)
        except Exception as e:
            data, message = {}, str(e)

        self.set_status(200)
        self.finish(json.dumps({"data": data, "message": message}))


translations_handler_path = r"/lab/api/translations/(?P<locale>.*)"
