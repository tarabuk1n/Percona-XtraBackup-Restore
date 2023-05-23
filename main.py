from google.cloud import storage
import subprocess
import logging
import configparser
import py7zr
import sys
import os
import glob
import shutil

config = configparser.ConfigParser()
config.read('config.ini')
account_json = config.get('project', 'account_json')
bucket_name = config.get('project', 'bucket_name')
password = config.get('project', 'password')
mysql_path = config.get('project', 'mysql_path')
logging.basicConfig(filename='restore-backup.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def get_bucket_files(bucket_name):
    client = storage.Client.from_service_account_json(account_json)
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    blobs = sorted(blobs, key=lambda x: x.updated, reverse=True)
    latest_file = blobs[0]
    latest_file.download_to_filename('backup.7z')

def restore_backup():
    current_dir = os.getcwd()
    destination_path = "/tmp/mysql/"
    commands = [
        'sudo systemctl stop mysql.service',
        f'sudo rm -rf {mysql_path}',
        'sudo xtrabackup --prepare --target-dir=/tmp/mysql/',
        f'sudo mkdir {mysql_path}',
        'sudo xtrabackup --move-back --target-dir=/tmp/mysql/',
        f'sudo chown -R mysql:mysql {mysql_path}',
        'sudo systemctl start mysql.service',
        'rm -rf /tmp/mysql/',
    ]
    try:
        with py7zr.SevenZipFile('backup.7z', 'r', password=password) as archive:
            archive.extractall()
    except Exception as e:
        logging.error("Failed to extract data from archive backup.7z")
        print("Error: failed to extract data from archive backup.7z")
        sys.exit(1)

    folder_to_move = glob.glob(os.path.join(current_dir, 'mysql-xtra_*'))[0]
    shutil.move(folder_to_move, destination_path)

    for command in commands:
        try:
            subprocess.check_call(command.split())
        except subprocess.CalledProcessError as error:
            logging.error(f"An error occurred while executing the command: {command}. Error Message: {error.output}")
            break

logging.info('Start of the recovery process')
get_bucket_files(bucket_name)
restore_backup()
logging.info('End of the recovery process')
