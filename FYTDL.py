#!/usr/bin/env python

# FYTDL v1.0
# Developed by: Elison O. Cepeda
# Technical Editor: Tim Xiang

import os
import logging
import logging.handlers
import csv
import hashlib
import youtube_dl

from datetime import datetime 


from config import LOG_FORMAT, DESTINATION_DIR, CSV_FILE, DEBUG_MODE, LOG_FILE, YDL_VIDEO_LIST_FILE, YDL_OUTPUT_PARAM, YDL_FORMAT_PARAM

logger = logging.getLogger("youtube-downloader")
    

class CustomError(Exception):
    pass

def output_to_csv(hashes):
    logger.info(f"Writing csv file to {os.path.abspath(CSV_FILE)}")
    with open(CSV_FILE, mode='w') as ytd_csv:
        hash_csv_writer = csv.writer(ytd_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        hash_csv_writer.writerow(['filename', 'hash', "hash_timestamp"])
        for hash in hashes:
            hash_csv_writer.writerow(list(hash))

def get_now_timestamp():
    dateTimeObj = datetime.now()
    return dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

def hash_videos():
    logger.info(f"Hashing videos in {os.path.abspath(DESTINATION_DIR)}")
    hashes = []
    for filename in os.listdir(DESTINATION_DIR):
        if filename.endswith(".mp4"): 
            filepath = os.path.join(DESTINATION_DIR, filename)
            with open(filepath, "rb") as vid_file:
                md5_hash = hashlib.md5()
                content = vid_file.read()
                md5_hash.update(content)
                digest = md5_hash.hexdigest()
                logger.info(f"{filename} MD5: {digest}")
                hashes.append((filename, digest, get_now_timestamp()))
    return hashes

def download():
    logger.info(f"Downloading videos to {os.path.abspath(DESTINATION_DIR)}")
    with open(YDL_VIDEO_LIST_FILE) as f:
        urls = f.readlines()
    ydl_opts = {
        'outtmpl': YDL_OUTPUT_PARAM,
        'format': YDL_FORMAT_PARAM,
        'logger': logger
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

def setup():
    if DEBUG_MODE:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logFormatter = logging.Formatter(LOG_FORMAT)
    fileHandler = logging.FileHandler(LOG_FILE)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    if not os.path.exists(DESTINATION_DIR):
        logger.info(f"Creating videos directory at {os.path.abspath(DESTINATION_DIR)}")
        os.makedirs(DESTINATION_DIR)

    
    if not (os.path.exists(YDL_VIDEO_LIST_FILE)):
        error_msg = f"VIDEO_LIST_FILE.txt file does not exist at {os.path.abspath(YDL_VIDEO_LIST_FILE)}"
        logger.error(error_msg)
        raise CustomError(error_msg) 

def main():
    logger.info("ACQUISITION PROCESS INITIATED!")
    download()
    hashes = hash_videos()
    output_to_csv(hashes)
    logger.info("ACQUISITION COMPLETE!")

if __name__ == '__main__':
    setup()
    main()
