# Percona XtraBackup: Restore via Python (Google Cloud Bucket)

1. Move authorization key from your Google Cloud Platform account (in JSON format) to the folder with the code.

2. Change the data in *config.ini* for the project:

- **ACCOUNT_JSON** - The name of the JSON file for authorization (with an extension). *Example:* ***service-iam-gserviceaccount-com.json***
- **BUCKET_NAME** - Bucket name in Google Cloud Platform
- **PASSWORD** - Password for extracting files from the archive
- **MYSQL_PATH** - The path to the MySQL database directory

3. Install all dependencies:

```sh
pip3 install -r requirements.txt  
```

4. Start the program:

```sh
python3 main.py
```

5. Check logs for errors and successful completion:
```sh
cat restore-backup.log
```
