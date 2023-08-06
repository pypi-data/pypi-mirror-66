# ipymagic


[Reference](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Distributing%20Jupyter%20Extensions%20as%20Python%20Packages.html)


Server Extension
```txt
- setup.py
- MANIFEST.in
- pymagic/
  - __init__.py
```

nbextension

```txt
- setup.py
- MANIFEST.in
- my_fancy_module/
  - __init__.py
  - static/
    index.js
```