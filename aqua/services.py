class Service(object):
    def process_search(self, resource, search_params = None):
        resource = 'search_' + resource

        if hasattr(self, resource):
            return getattr(self, resource)(search_params)