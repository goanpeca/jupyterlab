import json
import os


def get_locale_setting(user_settings_dir):
    """
    FIXME: there is probably a better way of doing this! 
    """
    path = os.path.join(user_settings_dir, "jupyterlab-i18n", "plugin.jupyterlab-settings")
    locale = "en"
    if os.path.isfile(path):
        lines = []
        with open(path) as fh:
            data = fh.read()

        # Remove comment lines
        for line in data.split("\n"):
            if "//" not in line:
                lines.append(line)

        data = json.loads("\n".join(lines))
        locale = data.get("locale", "en")

    return locale
