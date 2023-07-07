# 蒐集文章排程

## 目前來源

1. arXiv

## Start

```
$ nohup poetry run python monitor/main.py&
```

## Stop

```
$ ps aux | grep monitor/main.py
ubuntu   2824314  3.1  0.1  66900 51292 pts/0    S    13:58   0:08 /home/ubuntu/.cache/pypoetry/virtualenvs/community-monitor-TVDhsFyR-py3.10/bin/python monitor/main.py
$ kill -9 2824314
```
