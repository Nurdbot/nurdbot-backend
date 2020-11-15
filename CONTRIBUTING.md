* install docker, make sure you can run docker as not sudo.

```sh
bash create_db.sh
```

```sh
python -m venv env
source env/bin/activate
pip3 install -r requirments.txt
```

* edit add_creator.py to reflect your username
```py
#change
init_creator('something')
#to
init_creator('your_twitch_username')
```

```sh
python3 init_db.py
python3 add_creator.py
```



