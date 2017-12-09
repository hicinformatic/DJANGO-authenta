from .method import Method
import ldap, socket

class method_ldap(Method):
    cnx = None
    start = 'ldap'
    starts = 'ldaps'

    def __init__(self, method):
        self.port     = method.port
        self.tls      = method.tls
        self.host     = method.ldap_host
        self.cert     = method.certificate
        self.certpath = method.certificate_path
        self.define   = method.ldap_define
        self.scope    = method.ldap_scope
        self.version  = method.ldap_version
        self.bind     = method.ldap_bind
        self.password = method.ldap_password
        self.user     = method.ldap_user
        self.search   = method.ldap_search
        self.tls_cacertfile = method.ldap_tls_cacertfile
        self.self_signed = method.self_signed
        self.uri = self.start
        self.ldap = ldap

        if self.tls:
            self.uri = self.starts
            self.ldap.set_option(self.ldap.OPT_X_TLS_DEMAND, True)
            if self.cert:
                if self.self_signed: self.ldap.set_option(self.ldap.OPT_X_TLS_REQUIRE_CERT, self.ldap.OPT_X_TLS_ALLOW) 
                else: self.ldap.set_option(self.ldap.OPT_X_TLS_REQUIRE_CERT, True)
            if self.tls_cacertfile:
                    self.ldap.set_option(self.ldap.OPT_X_TLS_CACERTFILE, self.certpath)

    def check(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.close()
        cnx = ldap.initialize("{}://{}:{}".format(self.uri, self.host, self.port))
        cnx.protocol_version = getattr(ldap, self.version)
        #if self.tls: cnx.start_tls_s()
        if self.bind: cnx.simple_bind_s(self.bind, self.password)
        else: cnx.simple_bind_s()
        cnx.unbind_s()

    def get(self, username, password):
        searchdn = self.search.replace("{{username}}", username)
        self.cnx = self.ldap.initialize("{}://{}:{}".format(self.uri, self.host, self.port))
        self.cnx.protocol_version = getattr(self.ldap, self.version)
        #if self.tls: cnx.start_tls_s()
        if self.bind:
            self.cnx.simple_bind_s(self.bind, self.password)
            data = self.cnx.search_s(self.define, getattr(self.ldap, self.scope), searchdn)
            if data:
                userdn = data[0][0]
            else:
                raise self.UserNotFound
        else:
            userdn = str(self.user).replace("{{username}}", username)
        self.cnx.simple_bind_s(userdn, password)
        self.data = data if data else self.cnx.search_s(self.define, getattr(self.ldap, self.scope), searchdn)
        self.cnx.unbind_s()
        return data

    def correspondence(self, field):
         return self.data[0][1][field][0].decode()
