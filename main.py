"""
FelipdedelosH - 2024
CronTaskByLokoV1.0


This script run Task with time indication

1 - put the scripts to execute in folder Task
2 - Execute this file to work in cron time
"""
import schedule
from croniter import croniter
import datetime
import time
from os import scandir


def saveInfoInLOGFile(status, info):
    _previous_log_info = ""
    try:
        with open("log.log", "r") as f:
            _previous_log_info = f.read()
    except:
        pass
    with open("log.log", "w") as f: # Save
            data = ""

            if _previous_log_info != "":
                data = _previous_log_info + f"{status} - {datetime.date.today()} - {info}\n"
            else:
                data = f"{status} - {datetime.date.today()} - {info}\n"
                
            f.write(data)
#..,,..............................:+,.............................::.........................................
#.,#?..............................+@:............................,?*...........:#;...........................
#.,@%.......;????;..,*????+,..,*???%@:.......;????+..:*???*,,?+;?*.*+..**+?%%+.:%@%*?:.....:?+*?%?:.;?:...:?;.
#.,@%......%#;,,;#%..;::;+@?.:#%;::?@:......;@?,,:;.;@?:,:+::@S+;:.#S.,##;::+@*,+@*::,.....;@%;::%@;,#S,.,S#,.
#.,@%.....:@?....?@,,*%??*@%.?@,...+@:......,?S%%*:.S#......:@*....#S.,#%....S#.:@+........;@+...,@?.:@?.?@:..
#.,@%.....,#S,..,S#,?@:..,@%.+@+..,*@:......,,,,:%@:*@;...,,:@*....#S.,#%...:@?.:@*....;;..;@+..,*@;..;@?@;...
#.,SS%%%%%,:%%??%%:.;SS???#?..*S%??%#:......;%???%*,,*S%??%::#+....S%.,##??%S*,.,?S??:,#S,.;@S??%%;....?@+....
#..,,,,,,,...,::,.....,:,.,,...,::,.,........,,:,,.....,:,,..,.....,,.,@%,,,......,,,..,,..;@+,,,.....:#?.....
#......................................................................*+..................:?:........+?,.....
_SCRIPTS_ = {} # dict[key] = code
# Read all scripts in folder
def _isCronExpresionInCode(script_code, filename):
    _1stLine = str(script_code).split("\n")[0]

    if "#expresion_cron=" not in _1stLine:
        saveInfoInLOGFile("LOAD-SCRIPT:ERROR-NOT-FOUND-CRONEXPRESION", filename)
        return False
    
    return True

def loadAlPythonFilesInTaskFolder():
    for i in scandir("Task"):
        if i.is_file():
            if ".py" in i.name:
                _path = f"Task/{i.name}"
                with open(_path) as f:
                    script_code = f.read()
                    if _isCronExpresionInCode(script_code, i.name):
                        _SCRIPTS_[_path] = script_code # Save Script
loadAlPythonFilesInTaskFolder()


def executeCODE(script):
    _isLoad = script in _SCRIPTS_.keys()

    if not _isLoad:
        saveInfoInLOGFile("ERROR:REGISTRATION", script)
        return

    # Execute script
    try:
        exec(_SCRIPTS_[script])
        saveInfoInLOGFile("OK:EXECUTE-SCRIPT", script)
    except Exception as e:
        _err = str(e).replace("\n", "   ")
        saveInfoInLOGFile("FAILED:EXECUTE-SCRIPT", _err)


#  Convert CRON to Scheluded
def schedule_from_cron(cron_expression, job_function):
    """
    This method convert a cront espresion in seconds and programing the seconds in scheluded

    This is the first versión of code. NOT MAKE A TEST...
    PLZ make a test in the future
    """
    base_time = datetime.datetime.now()
    cron = croniter(cron_expression, base_time)
    next_execution = cron.get_next(datetime.datetime)
    interval = (next_execution - base_time).total_seconds()
    schedule.every(interval).seconds.do(lambda : executeCODE(str(job_function)))


# Auto registred all Task here
for i in _SCRIPTS_:
    _varCron = _SCRIPTS_[i] # Get ALL code
    _varCron = str(_varCron).split("\n")[0] # In first line of code FIND cron expresion

    _expresion_cron = _varCron.split("=")[-1]

    cron = croniter(_expresion_cron, datetime.datetime.now())
    next_execution = cron.get_next(datetime.datetime)
    # Register
    schedule_from_cron(_expresion_cron, i)


# RUN
while True:
    schedule.run_pending()
    time.sleep(1)
