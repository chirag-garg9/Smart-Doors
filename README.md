<h1 align="center" id="title">Smart Door Opening System</h1>

<h3>This are the commands that you need to run on your computer to start the docker image.</h3>

In rasberry pi
```bash
docker build -t smart-door .
```
This command builds a Docker image with name "Smart-Door".

```bash
docker run -p 5000:5000 smart-door
```

This command starts the docker image on your system.

When working locally, you should

open your command prompt and write
```bash
python -m venv path-where-you-want-virtualenv/name example - python -m venv D:/virtual/smart-door
```

Activate the enviroment using 
```bash
path-where-you-want-virtualenv/name/Scripts/activate Example: D:/virtual/smart-door/Scripts/activate
```
```bash
pip install -r requirements.txt
```
```bash
python main.py
```
the first step is to be done only when you firstly create a virtual environment.

the second step is to executed to activate the virtual environment whenever you want to work on the project because it the environment you will run your project on your computer.

third step only when there is something new in requirements.txt

fourth when you wanna test your application
