from .apps import AuthentaConfig, logmethis
import os

if not os.path.exists(AuthentaConfig.dir_logs): 
    os.makedirs(AuthentaConfig.dir_logs)
logmethis(7, 'logs_directory: %s' % str(AuthentaConfig.dir_logs))
logmethis(7, 'log_level: %s' % str(AuthentaConfig.loglvl))

logmethis(7, 'tasks_directory: %s' % str(AuthentaConfig.dir_task))
logmethis(7, 'binary_python: %s' % str(AuthentaConfig.python))
logmethis(7, 'binary_os: %s' % str(AuthentaConfig.binary))
logmethis(7, 'binary_backstart: %s' % str(AuthentaConfig.backstart))
logmethis(7, 'backstart_extension: %s' % str(AuthentaConfig.backext))
logmethis(7, 'backstart_end_option: %s' % str(AuthentaConfig.backend))
logmethis(7, 'script_autokill_timer: %sseconds' % str(AuthentaConfig.killscript))
logmethis(7, 'host_authorized_tasking: %s' % str(AuthentaConfig.host))
logmethis(7, 'ip_authorized_tasking: %s' % str(AuthentaConfig.ip))

logmethis(7, 'view_signup: %s' % str(AuthentaConfig.vsignup))
logmethis(7, 'view_signin: %s' % str(AuthentaConfig.vsignin))
logmethis(7, 'view_signout: %s' % str(AuthentaConfig.vsignout))
logmethis(7, 'view_profile: %s' % str(AuthentaConfig.vprofile))
logmethis(7, 'mail_activation: %s' % str(AuthentaConfig.mail_activation))

logmethis(7, 'unique_identity: %s' % str(AuthentaConfig.uniqidentity))
logmethis(7, 'required_fields: %s' % '; '.join(AuthentaConfig.requiredfields))
logmethis(7, 'username_is_unique: %s' % str(AuthentaConfig.usernameuniq))
logmethis(7, 'username_is_null: %s' % str(AuthentaConfig.usernamenull))
logmethis(7, 'email_is_unique: %s' % str(AuthentaConfig.emailuniq))
logmethis(7, 'email_is_null: %s' % str(AuthentaConfig.emailnull))
logmethis(7, 'firstname_is_null: %s' % str(AuthentaConfig.firstnamenull))
logmethis(7, 'lastname_is_null: %s' % str(AuthentaConfig.lastnamenull))
logmethis(7, 'is_active_default: %s' % str(AuthentaConfig.isactivedefault))
logmethis(7, 'is_staff_default: %s' % str(AuthentaConfig.isstaffdefault))

logmethis(7, 'choices_method: %s' % '; '.join(str(i[1]) for i in AuthentaConfig.choices_method))
logmethis(7, 'additional_methods: %s' % '; '.join(str(i[1]) for i in AuthentaConfig.additional_methods))

if not os.path.exists(AuthentaConfig.dir_json):
    os.makedirs(AuthentaConfig.dir_json)
logmethis(7, 'jsons_directory: %s' % str(AuthentaConfig.dir_json))

if AuthentaConfig.ldap_activated: 
    if not os.path.exists(AuthentaConfig.dir_ldapcerts):
        os.makedirs(AuthentaConfig.dir_ldapcerts)
    logmethis(7, 'ldap_certificates_directory: %s' % str(AuthentaConfig.dir_ldapcerts))


