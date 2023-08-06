# pvlink

ParaView-Web RemoteRenderer in Jupyter

## Installation

You can install pvlink using `pip`.

```
$ pip install pvlink
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```
$ jupyter nbextension enable --py [--sys-prefix|--user|--system] pvlink
```

To enable pvlink with Jupyter lab, make sure the Jupyter widgets extension is installed, and install the pvlink extension:
```
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager # install the Jupyter widgets extension
$ jupyter labextension install pvlink
```


## Usage
For examples see the [example notebook](examples/Examples.ipynb).  
The RemoteRenderer additionally requires the `paraview.simple` and `paraview.web modules`.


## Jupyter Proxy Setup (using nginx)

To enable streaming these settings need to be set, in the nginx config file for Jupyter (for example: in /etc/nginx/conf.d/):

```
# top-level http config for websocket headers
# If Upgrade is defined, Connection = upgrade
# If Upgrade is empty, Connection = close
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

... location ... {
   ...
           # websocket headers
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
  ...
}
```

An unused stream is automatically disconnected by nginx, after `proxy_read_timeout`'s seconds are exceeded. The default value of 60s is reached quite fast, therefore it is recommended to increase this value. 
For example:
```
# HTTPS server to handle JupyterHub
server {
    listen 443 ssl;
    ...
    proxy_read_timeout 3600s;
    ...
```

## Changelog
See [Changelog](CHANGELOG.md)
