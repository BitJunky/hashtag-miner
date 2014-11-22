Pre-requisites:

1. Navigate in iterm to where you want to save the files and enter:
```
git clone https://github.com/allentran/hashtag-miner.git
```
2. set up virtual environment (http://virtualenvwrapper.readthedocs.org/en/latest/)
``` 
           	pip install virtualenvwrapper ...
           	export WORKON_HOME=~/Envs
           	mkdir -p $WORKON_HOME
           	source /usr/local/bin/virtualenvwrapper.sh
           	mkvirtualenv env1
```
--Replace env1 with some name you want for the hashtag miner --
 
How to access:

1. `workon env1`
2. `Pip install –r requirements.txt (only required once)
3. navigate to the hashtag-miner folder
4. `python manage.py runserver localhost:8000`
5.     open web browser to localhost:8000
