from clld.web.maps import Map, ParameterMap, LanguageMap


class LanguagesMap(Map):
    def get_options(self):
        return {'max_zoom': 15}


class WordMap(ParameterMap):
    def get_options(self):
        return {
            'max_zoom': 15,
            'show_labels': True,
        }


class DialectMap(LanguageMap):
    def get_options(self):
        return {
            'zoom': 10,
            'max_zoom': 15,
        }


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('language', DialectMap)
    config.register_map('parameter', WordMap)
