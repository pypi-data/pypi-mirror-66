# Jupyter Marathon Spawner

Add Support to spin up jupyter notebooks in marathon


## Features
- Spawn Jupyter Notebook Single User Notebooks in Marathon
- Store them in a cool location
- Set Marathon Memory/CPU Constraints
- Set Mesos Host Constraints
- Create Volumes on containers
- Set Ports for users
- Allow custom start commands on single-user
- Support named server
- Use Bridge or Host Mode

# Configuration example

```python
c.JupyterHub.spawner_class = 'marathonspawner.MarathonSpawner'
c.MarathonSpawner.app_prefix = 'jupyter'
c.MarathonSpawner.marathon_host = 'http://leader-001.xxxxx:8080'
c.MarathonSpawner.marathon_user_name = 'admin'
c.MarathonSpawner.marathon_user_password = 'xxxxx'
c.MarathonSpawner.fetch = [{'uri': '/srv/config/docker-gitlab.tar.gz'}]
c.MarathonSpawner.mem_limit = '2G'
c.MarathonSpawner.cpu_limit = 1
c.MarathonSpawner.app_image = 'registry.gitlab.com/xxxx/extra/jupyter/master:5ad67069'
c.MarathonSpawner.app_cmd = '/home/jupyter/.local/bin/jupyter labhub --port $PORT0'
c.MarathonSpawner.volumes = [{'containerPath': '/home/jupyter/notebooks', 'hostPath': '/srv/config/notebooks', 'mode': 'RW' }]
c.MarathonSpawner.network_mode = 'HOST'
```


Below configs are optional

```python
c.JupyterHub.start_timeout: 120

c.JupyterHub.cleanup_servers = False # This should in general be a good idea
```