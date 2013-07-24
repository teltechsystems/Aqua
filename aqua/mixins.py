import os
import MySQLdb

class DbMixin(object):
    def __init__(self, db_params, *args, **kwargs):
        self.connection = MySQLdb.connect(**db_params)

        super(DbMixin, self).__init__(*args, **kwargs)

    def query_select(self, select):
        with self.connection as cursor:
            cursor.execute(str(select))

            fields = [x[0] for x in cursor.description]

            return [dict(zip(fields, x)) for x in cursor.fetchall()]

class SSHMixin(object):
    def __init__(self, ssh_params, *args, **kwargs):
        self.ssh_params = ssh_params

        super(SSHMixin, self).__init__(*args, **kwargs)

    def execute_command(self, command):
        command_parts = ['ssh', '%s@%s' % (self.ssh_params['user'], self.ssh_params['hostname'], )]

        if 'port' in self.ssh_params:
            command_parts.append('-p %s' % self.ssh_params['port'])

        # command_parts.append('"sh -c \\\"%s\\\"' % (command, ))
        command_parts.append('"%s"' % (command.replace('"', '\\\"'), ))

        print ' '.join(command_parts)

        return os.popen(' '.join(command_parts)).read()