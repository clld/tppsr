from clld.web.maps import Map, ParameterMap


class LanguagesMap(Map):
    def get_options(self):
        return {'max_zoom': 15}


class WordMap(ParameterMap):
    def get_options(self):
        return {
            'max_zoom': 15,
            'show_labels': True,
        }


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('parameter', WordMap)
