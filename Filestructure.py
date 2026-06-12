import os
from pathlib import Path
import logging

logging.basicConfig(level= logging.INFO, format='[%(asctime)s]: %(message)s')

list_of_files =[
    "Documentation/SDD.txt",
    "Documentation/HLD.txt",
    "Documentation/LLD.txt",
    "Documentation/Trace_SDD_HLD.txt",
    "Documentation/Trace_HLD_LLD.txt",
    "Data/Text/Audio_text.txt",
    "Data/Audio/output_audio.wav",
    "Data/Image/",
    "Research/trail.ipynb",
    "Code/__init__.py",
    "Code/main.py",
    "config/setup.py",
    "config/pyproject.py",
    ".env",
    "requirements.txt",
    "app.py",
]

for filepath in list_of_files:
    #Path: converts a string file path into a Path object
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f'Created directory : {filedir} for {filename}')

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w"):
            pass
            logging.info(f'creating empty file: {filepath}')

    else:
        logging.info(f"{filepath} alrady exists")
