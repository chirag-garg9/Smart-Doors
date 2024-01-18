#This are the commands that you need to run on your computer to start the docker image.

In rasberry pi
1.) docker build -t smart-door .
This command builds a Docker image with name "Smart-Door".

2.) docker run -p 5000:5000 smart-door
This command starts the docker image on your system.

When working locally, you should

1.) open your command prompt
2.) write python -m venv path-where-you-want-virtualenv/name example - python -m venv D:/virtual/smart-door
3.) Activate the enviroment using path-where-you-want-virtualenv/name/Scripts/activate
    Example: D:/virtual/smart-door/Scripts/activate
4.) pip install -r requirements.txt
5.) python main.py

the first step is to be done only when you firstly create a virtual environment
the second step is to executed to activate the virtual environment whenever you want to work on the project because it the environment you will run your project on your computer
third step only when there is something new in requirements.txt
fourth when you wanna test your application
