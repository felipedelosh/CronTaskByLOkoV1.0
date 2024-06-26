"""
FelipdedelosH - 2024
CronTaskByLokoV1.0


This script run Task with time indication

1 - put the scripts to execute in folder Task
2 - register the time and name of script
"""
import schedule
from datetime import date
import time
from os import scandir

_SCRIPTS_ = {} # dict[key] = code
# Read all scripts in folder
def loadAlPythonFilesInTaskFolder():
    for i in scandir("Task"):
        if i.is_file():
            if ".py" in i.name:
                _path = f"Task/{i.name}"
                with open(_path) as f:
                    script_code = f.read()
                    _SCRIPTS_[_path] = script_code
loadAlPythonFilesInTaskFolder()


def saveInfoInLOGFile(status,info):
    _previous_log_info = ""

    try:
        with open("log.log", "r") as f:
            _previous_log_info = f.read()
    except:
        pass

    with open("log.log", "w") as f: # Save
            data = ""

            if _previous_log_info != "":
                data = _previous_log_info + f"{status} - {date.today()} - {info}\n"
            else:
                data = f"{status} - {date.today()} - {info}\n"
                
            f.write(data)


def executeCODE(script):
    _isLoad = script in _SCRIPTS_.keys()

    if not _isLoad:
        saveInfoInLOGFile("ERROR:FILE", script)
        return

    # Execute script
    try:
        exec(_SCRIPTS_[script])
        saveInfoInLOGFile("RUN:CODE", script)
    except Exception as e:
        _err = str(e).replace("\n", "   ")
        saveInfoInLOGFile("ERROR:EXECUTE-SCRIPT", _err)


# Register all Task Here
schedule.every(1).seconds.do(lambda : executeCODE("test_dict_error")) # Testing if program run if taskcode fail.
schedule.every(1).seconds.do(lambda : executeCODE("Task/exampleEverySecondTask.py")) # Run every second
schedule.every(1).seconds.do(lambda : executeCODE("Task/emptyTaskCode.py")) # The program run if send empty code.

# END to register

# RUN
while True:
    schedule.run_pending()
    time.sleep(1)