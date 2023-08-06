

class Domain:
    protocol = 'https://'
    def url(self):
        return self.protocol + self.domain_name + self.server

class DomainProd(Domain):
    server =  '.vetmanager.ru'
    def __init__(self, domain_name):
        self.domain_name = domain_name


class DomainTest(Domain):
    server = '.tests.kube-dev.vetmanager.cloud'
    def __init__(self, domain_name):
        self.domain_name = domain_name


class DomainLocal(Domain):
    protocol = 'http://'
    server = '.localhost:8080'
    def __init__(self, domain_name):
        self.domain_name = domain_name
