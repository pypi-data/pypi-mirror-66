# hbdl the Humble Bundle downloader
A simple [Humble Bundle](https://www.humblebundle.com) downloader, takes a `Humble Bundle` product URI (e.g `https://www.humblebundle.com/downloads?key=xxxxxx`) and it takes care of the download from there.
## Installation
* ```pip install hbdl```
## Usage
```
Usage: hbdl [OPTIONS] URI
Options:
  --dest-dir PATH
  --downloader [wget|curl|python]
  --help                          Show this message and exit.
  ```
## Todo
 * Check the hash of the downloaded to avoid repetitive download
 * Better logging and error reporting
 * Standalone app / GUI
 * Automate the pypi publish
