import ras.Constants as constants
import os


class RasConnect:

    def __init__(self, r):
        self.r = r
        self.host = os.getenv(constants.RETHINK_HOST)
        self.port = os.getenv(constants.RETHINK_PORT)
        self.db = os.getenv(constants.RETHINK_DB)
        self.username = os.getenv(constants.RETHINK_USERNAME)
        self.password = os.getenv(constants.RETHINK_PASSWORD)
        self.cacertpath = os.getenv(constants.RETHINK_CERT_PATH)
        if ((self.cacertpath == None) or (self.cacertpath == "")):
            self.cacertpath = constants.CACERT
        else:
            self.cacertpath = self.cacertpath + "/" + constants.CACERT

    def open(self):
        conn = self.r.connect(
            host=self.host,
            port=self.port,
            db=self.db,
            user=self.username,
            password=self.password,
            ssl={'ca_certs': self.cacertpath}
        ).repl()
        return conn




