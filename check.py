from .apps import (AuthentaConfig as conf, logmethis)
import os

if not os.path.exists(conf.dir_logs): 
    os.makedirs(conf.dir_logs)
logmethis(7, 'logs_directory: %s' % str(conf.dir_logs))
logmethis(7, 'log_level: %s' % str(conf.loglvl))

logmethis(7, 'tasks_directory: %s' % str(conf.dir_task))
logmethis(7, 'binary_python: %s' % str(conf.python))
logmethis(7, 'binary_os: %s' % str(conf.binary))
logmethis(7, 'binary_extension: %s' % str(conf.binary_ext))
logmethis(7, 'python_os: %s' % str(conf.python))
logmethis(7, 'python_extension: %s' % str(conf.python_ext))
logmethis(7, 'python_backstart: %s' % str(conf.python_start))
logmethis(7, 'ptyhon_end_option: %s' % str(conf.python_end))
logmethis(7, 'script_autokill_timer: %sseconds' % str(conf.killscript))
logmethis(7, 'host_authorized_tasking: %s' % str(conf.host))
logmethis(7, 'ip_authorized_tasking: %s' % str(conf.ip))

logmethis(7, 'view_signup: %s' % str(conf.vsignup))
logmethis(7, 'view_signin: %s' % str(conf.vsignin))
logmethis(7, 'view_signout: %s' % str(conf.vsignout))
logmethis(7, 'view_profile: %s' % str(conf.vprofile))
logmethis(7, 'mail_activation: %s' % str(conf.mail_activation))

logmethis(7, 'unique_identity: %s' % str(conf.uniqidentity))
logmethis(7, 'required_fields: %s' % '; '.join(conf.requiredfields))
logmethis(7, 'username_is_unique: %s' % str(conf.usernameuniq))
logmethis(7, 'username_is_null: %s' % str(conf.usernamenull))
logmethis(7, 'email_is_unique: %s' % str(conf.emailuniq))
logmethis(7, 'email_is_null: %s' % str(conf.emailnull))
logmethis(7, 'firstname_is_null: %s' % str(conf.firstnamenull))
logmethis(7, 'lastname_is_null: %s' % str(conf.lastnamenull))
logmethis(7, 'is_active_default: %s' % str(conf.isactivedefault))
logmethis(7, 'is_staff_default: %s' % str(conf.isstaffdefault))

logmethis(7, 'choices_method: %s' % '; '.join(str(i[1]) for i in conf.choices_method))
logmethis(7, 'additional_methods: %s' % '; '.join(str(i[1]) for i in conf.additional_methods))

if not os.path.exists(conf.dir_cache):
    os.makedirs(conf.dir_cache)
logmethis(7, 'jsons_directory: %s' % str(conf.dir_cache))

if conf.ldap_activated: 
    if not os.path.exists(conf.dir_ldapcerts):
        os.makedirs(conf.dir_ldapcerts)
    logmethis(7, 'ldap_certificates_directory: %s' % str(conf.dir_ldapcerts))


