import json
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class LocaleManager:
    def __init__(self, default_locale='en', locale_dir='lang'):
        self.locale_dir = resource_path(locale_dir)
        self.current_locale = default_locale
        self.translations = {}
        self._load_locales()

    def _load_locales(self):
        self.translations = {}
        if not os.path.exists(self.locale_dir):
            print(f"Warning: Locale directory '{self.locale_dir}' not found.")
            return

        for filename in os.listdir(self.locale_dir):
            if filename.endswith('.json'):
                locale_code = filename.split('.')[0]
                filepath = os.path.join(self.locale_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.translations[locale_code] = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error loading translation file {filename}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred loading {filename}: {e}")

    def set_locale(self, locale_code):
        if locale_code in self.translations:
            self.current_locale = locale_code
            print(f"Locale set to: {locale_code}")
        else:
            print(f"Warning: Locale '{locale_code}' not found. Keeping '{self.current_locale}'.")

    def get_text(self, key, *args):
        try:
            # Fallback to default locale if key not in current locale
            text = self.translations.get(self.current_locale, {}).get(key)
            if text is None:
                text = self.translations.get('en', {}).get(key, f"MISSING_TRANSLATION:{key}")
            return text.format(*args) if args else text
        except KeyError:
            return f"MISSING_KEY:{key}"
        except Exception as e:
            print(f"Error getting text for key '{key}': {e}")
            return f"ERROR:{key}"

    def get_available_locales(self):
        return sorted(list(self.translations.keys()))
    
_LOCALE_MANAGER_GLOBAL = LocaleManager()