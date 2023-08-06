# Gimme-iPhotos

Download media files from iCloud.

This tool uses [pyicloud] to synchronize photos and videos from iCloud to your
local machine.

## Features

- Downloads media files from iCloud in parallel (might be beneficial on small files and wide bandwidth)
- Keeps local collection in sync with iCloud by:
  - skipping files which exist locally
  - removing local files which were removed from the cloud
- Reads configuration from ini-file
- Stores password in keychain (provided by [pyicloud])
- Supports two-factor authentication
- Shows nice progress bars (thanks to [tqdm])

## Usage

```
$ gimme-iphotos --help
usage: gimme-iphotos [-h] [-c CONFIG] [-v] [-u USERNAME] [-p PASSWORD] [-d DESTINATION] [-o] [-r] [-n PARALLEL]

Download media files from iCloud

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration file
  -v, --verbose
  -u USERNAME, --username USERNAME
  -p PASSWORD, --password PASSWORD
  -d DESTINATION, --destination DESTINATION
                        Destination directory
  -o, --overwrite       Overwrite existing files
  -r, --remove          Remove missing files
  -n PARALLEL, --num-parallel-downloads PARALLEL
```

[pyicloud]: (https://github.com/picklepete/pyicloud)
[tqdm]: (https://github.com/tqdm/tqdm)
