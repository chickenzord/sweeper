# sweeper

list old docker containers

```sh
pip install requirements.txt

# list container ids exited more than 3 days ago
./container.py --unit=day --exited=3

# list container ids created more than 60 minutes ago
# most probably won't be used
./container.py --unit=minute --created=60
```
