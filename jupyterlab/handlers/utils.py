"""
Localization utilities to find available language packs and packages
with localization information.
"""

import json
import os

import babel
import pkg_resources

# Entry points
JUPYTERLAB_LANGUAGEPACK_ENTRY = "jupyterlab.languagepack"
JUPYTERLAB_LOCALE_ENTRY = "jupyterlab.locale"


def is_valid_locale(locale):
    """
    Check if a `locale` value is valid.

    Parameters
    ----------
    locale: str
        Language locale code.

    Notes
    -----
    A valid locale is in the form language (See ISO-639 standard) and an
    optional territory (See ISO-3166 standard).
    
    Examples of valid locales:
    - English: "en"
    - Australian English: "en_AU"
    - Portuguese: "pt"
    - Brazilian Portuguese: "pt_BR"
    
    Examples of invalid locales:
    - Australian Spanish: "es_AU"
    - Brazilian German: "de_BR"
    """
    valid = False
    try:
        babel.Locale.parse(locale)
        valid = True
    except babel.core.UnknownLocaleError:
        pass

    return valid

def merge_data():
    """
    Merge language pack data with locale data bundled in packages.
    """


def get_installed_packages_locale(locale: str) -> dict:
    """
    Get all jupyterlab extensions installed that contain locale data.

    Returns
    -------
    dict
        Ordered list of available language packs.
        >>>{"package-name": locale_data, ...}

    Examples
    --------
    - `entry_points={"jupyterlab.locale": "package-name = package_module"}`
    - `entry_points={"jupyterlab.locale": "jupyterlab-git = jupyterlab_git"}`
    """
    packages_locale_data = {}
    for entry_point in pkg_resources.iter_entry_points(JUPYTERLAB_LOCALE_ENTRY):
        name = entry_point.name.replace("-", "_").lower()
        locales = []
        try:
            package_root_path = os.path.dirname(entry_point.load().__file__)
            locale_path = os.path.join(package_root_path, "locale")
            locales = [loc for loc in os.listdir(locales) if os.path.isdir(loc)]
        except Exception as e:
            print(e)
            continue

        data = {}
        if locale in locales:
            locale_json_path = os.path.join(
                locale_path, locale, "LC_MESSAGES", f"{name}.json"
            )
            if os.path.isfile(locale_json_path):
                with open(locale_json_path, "r") as fh:
                    data[locale] = json.loads(fh)

        if data:
            packages_locale_data[name] = data

    return packages_locale_data


def get_display_name(locale, display_locale : str = "en") -> str:
    """
    FIXME:

    Parameters
    ----------
    locale: str
        FIXME:

    Returns
    -------
    str
        FIXME:
    """
    locale = locale if is_valid_locale(locale) else "en"
    display_locale = display_locale if is_valid_locale(display_locale) else "en"
    loc = babel.Locale.parse(locale)
    return loc.get_display_name(display_locale)


def get_installed_language_packs(display_locale : str = "en") -> tuple:
    """
    Get available language packs.

    Parameters
    ----------
    display_locale: str
        FIXME:

    Returns
    -------
    tuple
        A tuple in the form `(locales, message)`, the locales found and a
        message with any information on exceptions or invalid locales.
    """
    invalid_locales = []
    valid_locales = []
    message = ""
    for entry_point in pkg_resources.iter_entry_points(JUPYTERLAB_LANGUAGEPACK_ENTRY):
        locale = entry_point.name
        if is_valid_locale(locale):
            valid_locales.append(locale)
        else:
            invalid_locales.append(locale)

    display_locale = display_locale if display_locale in valid_locales else "en"
    locales = {
        "en": {
            "displayName": get_display_name("en", display_locale),
            "nativeName": get_display_name("en", "en"),
        }
    }
    for locale in valid_locales:
        locales[locale] = {
            "displayName": get_display_name(locale, display_locale),
            "nativeName": get_display_name(locale, locale),
        }

    if invalid_locales:
        message += f"The following locales are invalid: {invalid_locales}!"

    return locales, message


def get_language_pack(locale: str) -> tuple:
    """
    Get a language pack for a given `locale` and update with any installed
    package locales.

    Returns
    -------
    tuple
        A tuple in the form `(locale_data_dict, message)`.
    """
    message = "SPAM!"
    locale_data = {}
    # locale_data = {
    #     "domain" : "messages",
    #     "locale_data" : {
    #     "messages" : {    
    #         "" : {
    #             "domain" : "messages",            
    #             "lang" : locale,
    #             "plural_forms" : "nplurals=2; plural=(n != 1);"
    #             },
    #         }
    #     }
    # }
    if is_valid_locale(locale):
        for entry_point in pkg_resources.iter_entry_points(
            JUPYTERLAB_LANGUAGEPACK_ENTRY
        ):
            if locale == entry_point.name:
                mod = entry_point.load()
                path = os.path.dirname(mod.__file__)
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        if name.endswith(".json"):
                            pkg_name = name.replace(".json", "")
                            json_path = os.path.join(root, name)
                            with open(json_path, "r") as fh:
                                locale_data[pkg_name] = json.load(fh)

                return locale_data, message
        else:
            return locale_data, message
    else:
        return locale_data, message


# if __name__ == "__main__":
#     print(get_installed_language_packs("de"))
