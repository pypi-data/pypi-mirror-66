# SG Markets API Authentication


> This package had a major update on 22apr20.  
    Run `pip install -U sgmarkets_api_auth` to update.

## 1- Introduction

This repo is a helper package for clients (and employees) to autheticate with SG Markets APIs.  


## 2 - Install

From terminal:
```bash
# download and install package from pypi.org
pip install sgmarkets_api_auth
```


## 3 - User guide

### 3.1 - Define you credentials

Create a file `my-secret.txt` (or pick the name) in your home directory.  
+ On Windows: `C:\Users\youraccountsname`.
+ On Linux/macOS: `~/youraccountsname`.

This file must contain your secrets in the following format:
```bash
SG_TOKEN=myowntoken

# compulsory even as blank
PROXY_LOGIN=myownproxylogin
PROXY_PASSWORD=myownproxypwd

# compulsory even as blank
PROXY_HOST=myownproxyhost
PROXY_PORT=myownproxyport
```

Pass this file name as argument to the Api object.

```python
from sgmarkets_api_auth import Api
# default name is 'my-secret.txt'
a = Api()

# default name is 'my-secret.txt'
a = Api(path_secret='my_custom_secret.txt')

# to see the logs - default is False
a = Api(verbose=True)

# to remove secrets and token from disk
a.clear_secret_token()
```

See the [demo notebook](http://nbviewer.jupyter.org/urls/gitlab.com/sgmarkets/sgmarkets-api-auth/raw/master/demo_sgmarkets_api_auth.ipynb).

### 3.2 - Make an API call

Read the demo notebooks for various APIs in the same gitlab [sgmarkets organization](https://gitlab.com/sgmarkets).  
There you can see how to use the `Api` object to make a request to an SG Markets API and analyse the response.  

