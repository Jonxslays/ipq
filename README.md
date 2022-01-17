# IP Query

A CLI tool for gathering IP and domain name information.

## Disclaimer

**Still in early development!**

## Requirements

- Python >= 3.7.
- `whois` shell command.
- `nslookup` shell command.
- Potentially `ping` shell command for future `-p` flag.

## Installation

```bash
pip install git+https://github.com/Jonxslays/ipq.git
```

## Usage

```bash
# Check ipq version
$ ipq -v
$ ipq --version

# Get help
$ ipq -h
$ ipq --help

# Get info on a domain
$ ipq google.com

# Get info on an ip
$ ipq 8.8.8.8

# Get info on a domain, and include whois info
$ ipq -w google.com
$ ipq --whois google.com

# Fails because ips do not have whois info
$ ipq -w 8.8.8.8
```

## License

ipq is licensed under the [MIT License](https://github.com/Jonxslays/ipq/blob/master/LICENSE).
