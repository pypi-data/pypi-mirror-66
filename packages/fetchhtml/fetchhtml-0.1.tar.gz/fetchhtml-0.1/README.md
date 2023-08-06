fetchhtml is a package that allows for developers to request HTML files of a website and save it in a designated save path. 

## Installation
```python
pip3 install fetchhtml 

```

## Usage
```python 
import fetchhtml 
from fetchhtml import fetcher 

```

## Saving HTML Document in directory
```python
fetcher = Fetcher()
fetcher.set_url("https://www.google.com)
fetcher.download_html("Your/Directory/Here", "Google.html")
```

