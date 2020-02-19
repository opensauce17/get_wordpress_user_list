#!/usr/bin/env python3

import os
import paramiko
import shutil
import glob
import pandas as pd

from bin import banner, logger, colors

from bin.logger import *

acl = config_reader.config_json_read()

class Commands:
    def __init__(self, retry_time=10):
        self.retry_time = retry_time
        pass

    def move_empty_files(self):
        os.chdir('csv_list')
        for x in os.listdir('.'):
            if os.stat(x).st_size <= 1:
                logger.warning(x.split('_', 1)[1].replace('.csv', '') + ' on ' + x.split('_', 1)[0] +
                               ' yielded no user data. Investigation required.')
                shutil.move(x, "../empty_files")
        os.chdir('../')


    def delete_empty_files(self):
        try:
            shutil.rmtree('empty_files')
            os.removedirs('empty_files')
        except:
            pass

    def delete_csv_list(self):
        try:
            shutil.rmtree('csv_list')
            os.removedirs('csv_list')
        except:
            pass

    def delete_new_csv_list(self):
        try:
            shutil.rmtree('new_csv_list')
            os.removedirs('new_csv_list')
        except:
            pass

    def make_dirs(self):
        mode = 0o777
        os.mkdir('csv_list', int(mode))
        os.mkdir('empty_files', int(mode))
        os.mkdir('new_csv_list', int(mode))

    def get_projects(self, server_name, host_ip, key_file, cmd_list):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host_ip, username='ubuntu', key_filename=key_file)
        except TimeoutError:
            logger.error('A timeout to ' + server_name + ' has occurred')
            exit()
        ssh.invoke_shell()
        stdin, stdout, stderr = ssh.exec_command(cmd_list)
        dir_lst = list(map(str.strip, stdout))
        prj_list = [project for project in dir_lst if project.startswith("as")]

        return prj_list

    def get_users(self, project_number, server_name, host_ip, key_file, cmd_list):

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(host_ip, username='ubuntu', key_filename=key_file)
            except TimeoutError:
                logger.error('A timeout to ' + server_name + ' has occurred')
                exit()
            ssh.invoke_shell()
            stdin, stdout, stderr = ssh.exec_command(cmd_list)

            logger.info('Getting user details for project ' + project_number)

            #Open new CSV File with hostname and as number as filename
            f = open('csv_list' + '/' + server_name.split('.', 1)[0] + '_' + project_number + ".csv", "w+")

            #Write the User data and replace any commas with spaces and any tabs with commas
            f.write(str(''.join(stdout.readlines()).replace(',', ' ').replace('\t', ',')))

        except paramiko.ssh_exception.AuthenticationException:
            logger.error('Authentication failed when connecting to %s' % server_name)
            sys.exit(1)
        ssh.close()


def main():

    banner.banner()

    logger.info('Clean up folders and files before script starts')

    try:
        os.remove('combined_user_list.csv')
    except:
        pass

    rmdir = Commands()
    rmdir.delete_csv_list()
    rmdir.delete_empty_files()
    rmdir.delete_new_csv_list()

    mkdir = Commands()
    mkdir.make_dirs()

    servers = acl["WP_SRV_LIST"]
    server_names = []

    for k, v in servers.items():
        server_names.append(v)

    for i in server_names:
        logger.info(colors.Colors.HEADER + 'Connected to ' + i + colors.Colors.ENDC)
        wp_srv = i
        ssh_keyfile = acl['SSH_KEYS'][i[:3]]

        get_projects = Commands()

        projects = get_projects.get_projects(i, host_ip=wp_srv, key_file=ssh_keyfile, cmd_list='ls /var/www')

        get_users = Commands()

        for p in projects:
            get_users.get_users(p, i, host_ip=wp_srv, key_file=ssh_keyfile,
                                cmd_list='sudo wp --allow-root user list --path=/var/www/{}'.format(p))

    #Get all the empty files caused by wp command not running
    logger.info('Move files that have empty contents')

    mv = Commands()
    mv.move_empty_files()

    #Create and populate Columns for project, environment and location
    logger.info('Preparing the combined user list into file combined_user_list.csv')

    os.chdir('csv_list')
    for i in os.listdir('.'):
        project = i.split('_', 1)[1].replace('.csv', '')
        location = i.split('-', 1)[0]
        environment = i.split('-', 2)[1]
        if environment == 'd':
            environment = 'development'
        if environment == 's':
            environment = 'staging'
        if environment == 'p':
            environment = 'production'

        csv_input = pd.read_csv(i)
        csv_input['project'] = project
        csv_input['environment'] = environment
        csv_input['location'] = location
        csv_input.to_csv('../new_csv_list' + '/' + i, index=False)

    #Combine all server AS projects into a single CSV file
    os.chdir('../new_csv_list')
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv("../combined_user_list.csv", index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    main()