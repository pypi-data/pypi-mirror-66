# mds - markdown server
**M**ark**d**own **S**erver is a simple Python application that serves local markdown files in your browser for simple viewing and editing. Markdown server is still in early development. 

### Installation
Via pip:

`pip3 install mds`

Via setup.py:

`pip3 install mistune bottle`

`python3 setup.py install`

### Usage
To use markdown server you simply need to point it to a directory where you keep markdown files. It will recursively search through the directory for files with a `*.md` extension. These can then be viewed and edited in the browser at localhost:3000. 

Serve notes on default port:
```
mds ~/notes
```

Serve notes on specific ports:
```
mds -p 8080 ~/notes
```

### Contributing
Contributing is welcome, just make a PR.

### License
MIT
