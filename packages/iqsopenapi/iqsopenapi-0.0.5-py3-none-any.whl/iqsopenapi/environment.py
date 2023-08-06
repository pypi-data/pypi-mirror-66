from urllib.parse import urljoin

class Environment(object):

    _env = None

    def __init__(self, config):
        Environment._env = self
        self.config = config
        self.__debug = True

        self.market_api = None

        self.basicdata_api = None

    def get_instance():
        """
        返回已经创建的 Environment 对象
        """
        if Environment._env is None:
            raise RuntimeError(u"Environment has not been created.")
        return Environment._env

    def get_apiurl(self,relativeUrl):
        if self.__debug:
            return urljoin("https://dev_apigateway.inquantstudio.com/", relativeUrl)
        return urljoin("https://apigateway.inquantstudio.com/", relativeUrl)

    def get_quoteaddr(self):
        if self.__debug:
            return "wss://dev_quotegateway.inquantstudio.com"
        return "wss://quotegateway.inquantstudio.com"