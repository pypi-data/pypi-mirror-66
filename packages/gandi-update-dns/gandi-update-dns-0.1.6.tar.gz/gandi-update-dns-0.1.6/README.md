Yet another tool to update DNS zone in Gandi provider!

[![PyPI](https://img.shields.io/pypi/v/gandi-update-dns.svg)](https://pypi.org/project/gandi-update-dns/)
[![PyPI - Status](https://img.shields.io/pypi/status/gandi-update-dns.svg)](https://pypi.org/project/gandi-update-dns/)
[![PyPI - License](https://img.shields.io/pypi/l/gandi-update-dns.svg)](https://opensource.org/licenses/ISC)

## How to use

Just use the following command:

    gandi-update-dns
    
If the command is not on your PATH, it will be usually found on `$HOME/.local/bin`.

## Configuration file

If you have no configuration file, the main command will ask you for a domain and a Gandi api key.

Configuration file can be found here:

- Directory: XDG_CONFIG_HOME (default is `$HOME/.config`)
- File: `gandi-update-dns.conf`
