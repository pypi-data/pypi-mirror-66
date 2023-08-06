import multiprocessing
import os

from datetime import datetime

import six

from fabric import api as fab
from fabric.contrib import files

import fabricio

from fabricio import docker, utils
from fabricio.docker.base import Attribute
from fabricio.utils import Options


class PostgresqlBackupMixin(docker.BaseService):
    """
    Your Docker image must have pg_dump and pg_restore installed in order
    to run backup and restore respectively
    (usually this requires `postgresql-client-common` package for Ubuntu/Debian)
    """

    db_name = Attribute()

    db_user = Attribute(default='postgres')

    db_host = Attribute()

    db_port = Attribute()

    db_backup_dir = Attribute()

    db_backup_format = Attribute(default='c')

    db_backup_compress_level = Attribute()  # 0-9 (0 - no compression, 9 - max)

    db_backup_workers = Attribute(default=1)

    db_restore_workers = Attribute(default=4)

    db_backup_filename = Attribute(default='{datetime:%Y-%m-%dT%H:%M:%S.%f}.dump')

    @property
    def db_connection_options(self):
        return Options([
            ('username', self.db_user),
            ('host', self.db_host),
            ('port', self.db_port),
        ])

    @property
    def db_backup_options(self):
        return Options([
            ('if-exists', True),
            ('create', True),
            ('clean', True),
        ])

    def make_backup_command(self):
        options = Options(self.db_connection_options)
        options.update(self.db_backup_options)
        options.update([
            ('format', self.db_backup_format),
            ('dbname', self.db_name),
            ('compress', self.db_backup_compress_level),
            ('jobs', self.db_backup_workers),
            ('file', os.path.join(
                self.db_backup_dir,
                self.db_backup_filename.format(datetime=datetime.utcnow())
            )),
        ])
        return 'pg_dump {options}'.format(options=options)

    @fabricio.once_per_task
    def backup(self):
        if self.db_backup_dir is None:
            fab.abort('db_backup_dir not set, can\'t continue with backup')
        command = self.make_backup_command()
        self.image.run(
            command=command,
            quiet=False,
            options=self.safe_options,
        )

    @property
    def db_restore_options(self):
        return self.db_backup_options

    def make_restore_command(self, backup_filename):
        options = Options(self.db_connection_options)
        options.update(self.db_restore_options)
        options.update([
            ('dbname', 'template1'),  # use any existing DB
            ('jobs', self.db_restore_workers),
            ('file', os.path.join(self.db_backup_dir, backup_filename)),
        ])
        return 'pg_restore {options}'.format(options=options)

    @fabricio.once_per_task
    def restore(self, backup_name=None):
        """
        Before run this method you have somehow to disable incoming connections,
        e.g. by stopping all database client containers:

            client_container.stop()
            pg_container.restore()
            client_container.start()
        """
        if self.db_backup_dir is None:
            fab.abort('db_backup_dir not set, can\'t continue with restore')

        if backup_name is None:
            raise ValueError('backup_filename not provided')

        command = self.make_restore_command(backup_name)
        self.image.run(
            command=command,
            quiet=False,
            options=self.safe_options,
        )


class PostgresqlContainer(docker.Container):

    pg_conf = Attribute(default='postgresql.conf')

    pg_hba = Attribute(default='pg_hba.conf')

    pg_data = Attribute(default=NotImplemented)

    sudo = Attribute(default=False)

    stop_signal = 'INT'

    stop_timeout = 30

    def update_config(self, content, path):
        old_file = six.BytesIO()
        if files.exists(path, use_sudo=self.sudo):
            fab.get(remote_path=path, local_path=old_file, use_sudo=self.sudo)
        old_content = old_file.getvalue()
        need_update = content != old_content
        if need_update:
            fabricio.move_file(
                path_from=path,
                path_to=path + '.backup',
                sudo=self.sudo,
                ignore_errors=True,
            )
            fab.put(six.BytesIO(content), path, use_sudo=self.sudo, mode='0644')
            fabricio.log('{path} updated'.format(path=path))
        else:
            fabricio.log('{path} not changed'.format(path=path))
        return need_update

    def db_exists(self):
        return files.exists(
            os.path.join(self.pg_data, 'PG_VERSION'),
            use_sudo=self.sudo,
        )

    def create_db(self, tag=None, registry=None, account=None):
        """
        Official PostgreSQL Docker image executes 'postgres initdb' before
        any command starting with 'postgres' (see /docker-entrypoint.sh),
        therefore if you use custom image, you probably have to implement
        your own `create_db()`
        """
        fabricio.log('PostgreSQL database not found, creating new...')
        self.image[registry:tag:account].run(
            'postgres --version',  # create new DB (see method description)
            options=self.safe_options,
            quiet=False,
        )

    def update(self, tag=None, registry=None, account=None, force=False):
        if not any(map(self.options.__contains__, ['volume', 'mount'])):
            # TODO better check if volume or mount properly defined
            fab.abort(
                'Make sure you properly define volume or mount for DB data, '
                'Fabricio cannot work properly without it'
            )
        if not self.db_exists():
            self.create_db(tag=tag, registry=registry, account=account)

        main_conf = os.path.join(self.pg_data, 'postgresql.conf')
        hba_conf = os.path.join(self.pg_data, 'pg_hba.conf')

        main_config_updated = self.update_config(
            content=open(self.pg_conf, 'rb').read(),
            path=main_conf,
        )
        hba_config_updated = self.update_config(
            content=open(self.pg_hba, 'rb').read(),
            path=hba_conf,
        )
        container_updated = super(PostgresqlContainer, self).update(
            force=force,
            tag=tag,
            registry=registry,
            account=account,
        )
        if not container_updated:
            if main_config_updated:
                self.reload()
            elif hba_config_updated:
                self.signal('HUP')
            else:
                return False  # nothing updated
            try:
                # remove container backup to prevent reverting to old version
                self.get_backup_version().delete(delete_image=True)
            except docker.ContainerNotFoundError:
                pass
        if not main_config_updated:
            # remove main config backup to prevent reverting to old version
            main_conf_backup = main_conf + '.backup'
            fabricio.remove_file(
                main_conf_backup,
                ignore_errors=True,
                sudo=self.sudo,
            )
        if not hba_config_updated:
            # remove pg_hba config backup to prevent reverting to old version
            hba_conf_backup = hba_conf + '.backup'
            fabricio.remove_file(
                hba_conf_backup,
                ignore_errors=True,
                sudo=self.sudo,
            )
        return True

    def revert(self):
        main_conf = os.path.join(self.pg_data, 'postgresql.conf')
        main_conf_backup = main_conf + '.backup'
        hba_conf = os.path.join(self.pg_data, 'pg_hba.conf')
        hba_conf_backup = hba_conf + '.backup'
        main_config_reverted = fabricio.move_file(
            path_from=main_conf_backup,
            path_to=main_conf,
            ignore_errors=True,
            sudo=self.sudo,
        ).succeeded
        hba_config_reverted = fabricio.move_file(
            path_from=hba_conf_backup,
            path_to=hba_conf,
            ignore_errors=True,
            sudo=self.sudo,
        ).succeeded
        try:
            super(PostgresqlContainer, self).revert()
        except docker.ContainerError:
            if main_config_reverted:
                self.reload()
            elif hba_config_reverted:
                self.signal('HUP')
            else:
                raise

    def destroy(self, delete_data=False):
        super(PostgresqlContainer, self).destroy()
        if utils.strtobool(delete_data):
            fabricio.remove_file(
                self.pg_data,
                sudo=self.sudo,
                force=True,
                recursive=True,
            )


class StreamingReplicatedPostgresqlContainer(PostgresqlContainer):

    pg_recovery = Attribute(default='recovery.conf')

    pg_recovery_primary_conninfo = Attribute(
        default="primary_conninfo = 'host={host} port={port} user={user}'"
    )  # type: str

    pg_recovery_port = Attribute(default=5432)

    pg_recovery_user = Attribute(default='postgres')

    pg_recovery_revert_enabled = Attribute(default=False)

    pg_recovery_master_promotion_enabled = Attribute(default=False)

    pg_recovery_wait_for_master_seconds = Attribute(default=30)

    def __init__(self, *args, **kwargs):
        super(StreamingReplicatedPostgresqlContainer, self).__init__(
            *args, **kwargs)
        self.master_obtained = multiprocessing.Event()
        self.master_lock = multiprocessing.Lock()
        self.multiprocessing_data = data = multiprocessing.Manager().Namespace()
        data.db_exists = False
        data.exception = None
        self.instances = multiprocessing.JoinableQueue()

    def copy_data_from_master(self, tag=None, registry=None, account=None):
        pg_basebackup_command = (
            'pg_basebackup'
            ' --progress'
            ' --write-recovery-conf'
            ' -X stream'
            ' --pgdata=$PGDATA'
            ' --host={host}'
            ' --username={user}'
            ' --port={port}'
            ''.format(
                host=self.multiprocessing_data.master,
                user=self.pg_recovery_user,
                port=self.pg_recovery_port,
            )
        )
        command = "/bin/bash -c '{pg_basebackup_command}'".format(
            pg_basebackup_command=pg_basebackup_command,
        )
        self.image[registry:tag:account].run(
            command=command,
            options=self.options,
            quiet=False,
        )

    def get_recovery_config(self):
        recovery_config = open(self.pg_recovery).read()
        primary_conninfo = self.pg_recovery_primary_conninfo.format(
            host=self.multiprocessing_data.master,
            port=self.pg_recovery_port,
            user=self.pg_recovery_user,
        )
        recovery_config_items = [
            row for row in recovery_config.splitlines()
            if not row.startswith('primary_conninfo')
        ]
        recovery_config_items.append(primary_conninfo)
        return ('\n'.join(recovery_config_items) + '\n').encode()

    def set_master_info(self):
        if self.multiprocessing_data.exception is not None:
            fab.abort('Task aborted due an exception: {exception}'.format(
                exception=self.multiprocessing_data.exception,
            ))
        fabricio.log('Found master: {host}'.format(host=fab.env.host))
        self.multiprocessing_data.master = fab.env.host

    def update_recovery_config(self, tag=None, registry=None, account=None):
        db_exists = self.db_exists()
        recovery_conf_file = os.path.join(self.pg_data, 'recovery.conf')
        if db_exists:
            self.multiprocessing_data.db_exists = True
            if not files.exists(recovery_conf_file, use_sudo=self.sudo):
                # master founded
                self.set_master_info()
                return False
        fabricio.log('Waiting for master info ({seconds} seconds)...'.format(
            seconds=self.pg_recovery_wait_for_master_seconds,
        ))
        self.master_obtained.wait(self.pg_recovery_wait_for_master_seconds)
        if not self.master_obtained.is_set():
            if db_exists and not self.pg_recovery_master_promotion_enabled:
                fab.abort(
                    'Database exists but master not found. This probably '
                    'means master failure. New master promotion disabled '
                    'by default, but can be enabled by setting attribute '
                    '\'pg_recovery_master_promotion_enabled\' to True.'
                )
            self.master_lock.acquire()
            if not self.master_obtained.is_set():
                if db_exists:
                    fabricio.move_file(
                        path_from=recovery_conf_file,
                        path_to=recovery_conf_file + '.backup',
                        sudo=self.sudo,
                    )
                    self.set_master_info()
                    return True
                elif not self.multiprocessing_data.db_exists:
                    self.set_master_info()
                    return False
            self.master_lock.release()
            self.master_obtained.wait()
        if not db_exists:
            self.copy_data_from_master(
                tag=tag,
                registry=registry,
                account=account,
            )
        return self.update_config(
            content=self.get_recovery_config(),
            path=os.path.join(self.pg_data, 'recovery.conf'),
        )

    def update(self, tag=None, registry=None, account=None, force=False):
        if not fab.env.parallel:
            fab.abort(
                'Master-slave configuration update requires parallel mode. '
                'Use Fabric\'s `--parallel` option to enable this mode '
                'for a current session.'
            )

        self.instances.put(None)

        try:
            recovery_config_updated = self.update_recovery_config(
                tag=tag,
                registry=registry,
                account=account,
            )

            container_updated = super(
                StreamingReplicatedPostgresqlContainer,
                self,
            ).update(force=force, tag=tag, registry=registry, account=account)

            if not container_updated and recovery_config_updated:
                self.reload()
            self.master_obtained.set()  # one who first comes here is master
            return container_updated or recovery_config_updated
        except Exception as exception:
            self.multiprocessing_data.exception = exception
            raise
        finally:
            try:
                self.master_lock.release()
            except ValueError:  # ignore "released too many times" error
                pass
            self.instances.get()
            self.instances.task_done()
            self.instances.join()  # wait until all instances will be updated

            # reset state at the end to prevent fail of the next Fabric command
            self.master_obtained.clear()

    def revert(self):
        if not self.pg_recovery_revert_enabled:
            fab.abort(
                "StreamingReplicatedPostgresqlContainer can not be reverted by "
                "default. You can change this behaviour by setting attribute "
                "'pg_recovery_revert_enabled'. BUT whether this attribute is "
                "set or not, recovery configs (master-slave configuration) "
                "will not be reverted anyway."
            )
        super(StreamingReplicatedPostgresqlContainer, self).revert()
