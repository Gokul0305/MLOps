# PLCConnect


## How to Install

### Using PIP

To install the package using pip,

```bash
# Install Specific Version

pip install pip install "git+https://github.com/mechmet-vision/PLCConnect.git@{VERSION}" # Replace {VERSION} with a release version 

# Install Latest Stable Release

pip install pip install "git+https://github.com/mechmet-vision/PLCConnect.git"
```

### Using Setuptools

Installing a Specific Version

```python
from setuptools import setup, find_packages

setup(
    name="foo",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "LoggerLib @ git+https://github.com/mechmet-vision/PLCConnect.git@{VERSION}" # Replace {VERSION} with a release version
    ] 
)

```

Installing a Latest Stable Version

```python
from setuptools import setup, find_packages

setup(
    name="foo",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "PLCConnect @ git+https://github.com/mechmet-vision/PLCConnect.git"
    ] 
)
```

### Using `pyproject.toml`

```toml
# Install Specific Version

[project]
dependencies = [
    "PLCConnect @ git+https://github.com/mechmet-vision/PLCConnect.git@{VERSION}" # Replace {VERSION} with a release version
]

# Install Latest Stable Version

[project]
dependencies = [
    "PLCConnect @ git+https://github.com/mechmet-vision/PLCConnect.git"
]
```
