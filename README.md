# Forensic YouTube-DL (FYTDL)

REQUIREMENTS: youtube-dl==2021.5.16

DESCRIPTION: This script uses youtube-dl to download videos from a predefined list and automates the process of hashing the videos, pushing the results to a .csv file, logging the process/errors, and pushing the information logged to a .log file.

INSTRUCTIONS: 
1. Download the files within this repository into the same directory.
2. Identify the videos to be downloaded.
3. Copy the link(s) to each video and place them into the VIDEO_FILE_LIST.txt. Each link MUST be on its own line within the file.
4. Execute FYTDL.py in your favorite python interpreter or within a CMD prompt, PowerShell, or terminal window.
5. Review the FYTDL_log.log file, RESULTS.csv, and the "FYTDL ACQUIRED VIDEOS" directory containing the downloaded videos.
