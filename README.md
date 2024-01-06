# MikroBrute

MikroBrute is a brute-force script for MikroTik router credentials which attempts through the web panel of the router. It is meant to be a toy project, and is not intended for use in any serious actions.

## Requirements

1. Python 3.10+
2. Google chrome

## Installation

- Clone the repo

```sh
git clone https://github.com/junkcodes/mikrobrute.git
```

- Install dependencies:

```sh
pip3 install -r requirements.txt
```

## Updating

If you want to get most recent updates for MikroBrute, just pull the latest changes:

```sh
git pull
```

## Usage

Here are the options for MikroBrute here.

| Option    | Function                         |
| --------  | -------------------------------- |
| `--site`  | MikroTik web login address       |
| `--userl` | Target user list to attack       |
| `--passl` | Password dictionary              |

You can pass those options in the form of arguments.

Here is an example of how to use the tool with proper arguments:
```sh
python3 MikroBrute.py --site "http://172.16.16.1:8081" --user userlist.txt --pass passlist.txt
```
> Here, 172.16.16.1 is the address and 8081 is the port on which the web panel is listening

## Disclaimer

> This project and it's contributors do not support or take responsibility for any form of unethical acts. This software is purely for educational purposes and is not intended to cause any harm.
