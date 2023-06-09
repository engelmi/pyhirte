**The hirte python module**

This is an effort from the hirte team to provide to community a python module. With the `hirte python module`, it's possible to make dynamic programs also using dbus interface. However, don't expect such library in an official FuSA image.

As example, we have `py-hirtectl` which uses the python module as demo:

```
# python3 ./py-hirtectl node listall
Node: control.medogz.com, State: online
Node: node1.medogz.com, State: offline
Node: qm-node1, State: offline
```

```
# python3 ./py-hirtectl node start libpod@node1 ypserve@node2
Starting libpod on node node1
Starting ypserve on node node2
```

## Requirements
1) gobject and pip packages:
```
dnf install -y \
    python3-gobject \
    python3-pip
```

2) install requirements using pip
```
pip install -r requirements.txt
```

## How to use ?

Until properly package, use these steps:

- create `hirte` dir into your python site-packages
`mkdir /usr/lib/python3.9/site-packages/hirte/`

- copy `__init__.py, config.py, node.py` to /usr/lib/python3.9/site-packages/hirte/

- run `python ./py-hirtectl`