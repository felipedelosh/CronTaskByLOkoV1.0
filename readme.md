<h1 align="center"> FelipedelosH </h1>
<br>
<h4>CronTask By LOko v1.0</h4>

![Banner](docs/banner.png)
:construction: IN CONTRUCTION :construction:
<br><br>
This program is cretate to execute Task in time lapses. If you need execute a python script for example every minute you only need follow two steps: 1 - save you python script in folder task. 2 - register the python script in main.py. the run the "main.py" file a waiting.

## :hammer:Funtions:

- `Function 1`: Automatic load all scripts.py files in folder Task<br>
- `Function 2`: You register a frecuency to execute every script in Task folder<br>
- `Function 3`: LOG system for every event in execute task folder<br>


## :play_or_pause_button:How to execute a project

Install all requirements with the command: pip install -r requirements.txt<br>
insert your script.py in folder: Task/<br>
Register your script in main.py<br>
RUN main.py<br>


## About the time to execute scripts

It´s based in library "Schelude" of python https://schedule.readthedocs.io/
<br>
you only need to undertands the time logic for example:
<br>
if you need execute a script every 15 minutes use schedule.every(1).minutes.do(lambda : method_to_call())

## To register python file

OPEN the file "main.py" and search registration. and put the frecuency of execute a task.

## :hammer_and_wrench:Tech.

- python
- Schelude


## Architecture

```
PROJECT
    Task
        files.py
    main.py
    requirements.txt
```

## :warning:Warning.

- every python file in the folder task be single archive, NOT support another subclass files.

## Autor

| [<img src="https://avatars.githubusercontent.com/u/38327255?v=4" width=115><br><sub>Andrés Felipe Hernánez</sub>](https://github.com/felipedelosh)|
| :---: |