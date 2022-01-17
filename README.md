# IP Query

A CLI tool for gathering IP and domain name information.

## Requirements

- Python >= 3.7.
- `whois` shell command.
- `nslookup` shell command.
- `ping` shell command.

## Installation

Latest stable version:

```bash
pip install ipq
```

Latest stable version with speedups:
- Adds `aiodns` and `cchardet` dependencies.

```bash
pip install "ipq[speedups]"
```

Development version:

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

# Ping the host
$ ipq -p google.com
$ ipq --ping 8.8.8.8

# Get ip and whois info on a domain
$ ipq -w google.com
$ ipq --whois google.com

# Fails: ips do not have whois info
$ ipq -w 8.8.8.8
```

## License

ipq is licensed under the [MIT License](https://github.com/Jonxslays/ipq/blob/master/LICENSE).
