from .method import Method
import ldap, socket

class method_ldap(Method):
    def __init__(self, method):
        self.method   = method
        self.conf     = method.ldap_conf
        self.port     = method.port
        self.tls      = method.tls
        self.host     = method.ldap_host
        self.cert     = method.certificate
        self.define   = method.ldap_define
        self.scope    = method.ldap_scope
        self.version  = method.ldap_version
        self.bind     = method.ldap_bind
        self.password = method.ldap_password
        self.user     = method.ldap_user
        self.search   = method.ldap_search

    def check(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            sock.close()
            if self.tls:
                ldap.set_option(ldap.OPT_X_TLS_DEMAND, True)
                if self.cert:
                    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, True)
                    ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, self.method.certificate_path)
            cnx = ldap.initialize("ldap://%s:%s" %(self.host, self.port))
            cnx.protocol_version = getattr(ldap, self.version)
            if self.tls: cnx.start_tls_s()
            if self.bind: cnx.simple_bind_s(self.bind, self.password)
            else: cnx.simple_bind_s()
            cnx.unbind_s()
            self.method.error = None
            self.method.save()
        except Exception as e:
            self.method.error = e
            self.method.save()
            return False
        return True

    def get(self, username, password):
        self.POST_username = username
        self.POST_password = password
        searchdn = self.search.replace("{{username}}", self.POST_username)
        try:
            if self.tls:
                ldap.set_option(ldap.OPT_X_TLS_DEMAND, True)
                if self.cacert:
                    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, True)
                    ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, self.cacert.path)
            cnx = ldap.initialize("ldap://%s:%s" %(self.host, self.port))
            cnx.protocol_version = getattr(ldap, self.version)
            if self.tls: cnx.start_tls_s()
            if self.bind:
                cnx.simple_bind_s(self.bind, self.password)
                try: userdn = cnx.search_s(self.define, getattr(ldap, self.scope), searchdn)[0][0]
                except Exception: return 'UserDoesNotExist'
            else:
                userdn = str(self.user).replace("{{username}}", self.POST_username)
            cnx.simple_bind_s(userdn, self.POST_password)
            if searchdn: data = cnx.search_s(self.define, getattr(ldap, self.scope), searchdn)
            else: data = cnx.search_s(self.define, getattr(ldap, self.scope))
            cnx.unbind_s()
            return data
        except Exception as e:
            return e
        return False
