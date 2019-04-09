class Search:

    def __init__(self, hc_manager, user_manager):
        self._hc_manager = hc_manager
        self._user_manager = user_manager
        
    # Search 1
    # Input: string - name of healthcentre
    # Output: List of all healthcentres(object)
    def search_HC_name(self, name=""):
        if name:
            name = name.lower()
            return [x for x in self._hc_manager.centres if name in x.name.lower()]
        else:
            return self._hc_manager.centres

    # Search 2
    # Input: string - suburb
    # Output: List of all healthcentres(object)
    def search_HC_suburb(self, suburb=""):
        if suburb:
            suburb = suburb.lower()
            return [x for x in self._hc_manager.centres if suburb in x.suburb.lower()]
        else:
            return self._hc_manager.centres

    # Search 3
    # Input: string - name of service/profession
    # Output: List of all providers(object)
    def search_HP_service(self, service=""):
        if service:
            service = service.lower()
            return [x for x in self._user_manager.providers if service in x.profession.lower()]
        else:
            return self._user_manager.providers

    # Search 4
    # Input: string - name of provider
    # Output: List of all providers(object)
    def search_HP_name(self, name=""):
        if name:
            name = name.lower()
            return [x for x in self._user_manager.providers if name in x.name.lower()]
        else:
            return self._user_manager.providers