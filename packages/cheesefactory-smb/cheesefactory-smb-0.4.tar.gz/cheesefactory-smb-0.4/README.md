# cheesefactory-smb

-----------------

##### A simple wrapper for PySMB.
[![PyPI Latest Release](https://img.shields.io/pypi/v/cheesefactory-smb.svg)](https://pypi.org/project/cheesefactory-smb/)
[![PyPI status](https://img.shields.io/pypi/status/cheesefactory-smb.svg)](https://pypi.python.org/pypi/cheesefactory-smb/)
[![PyPI download month](https://img.shields.io/pypi/dm/cheesefactory-smb.svg)](https://pypi.python.org/pypi/cheesefactory-smb/)
[![PyPI download week](https://img.shields.io/pypi/dw/cheesefactory-smb.svg)](https://pypi.python.org/pypi/cheesefactory-smb/)
[![PyPI download day](https://img.shields.io/pypi/dd/cheesefactory-smb.svg)](https://pypi.python.org/pypi/cheesefactory-smb/)

### Main Features

* Built around PySMB.
* Push and pull files with ease.

**Note:** _This package is still in beta status. As such, future versions may not be backwards compatible and features may change._

## Installation
The source is hosted at https://bitbucket.org/hellsgrannies/cheesefactory-smb

```sh
pip install cheesefactory-smb
```

## Dependencies

* [pysmb](https://pysmb.readthedocs.io/en/latest/)

### Connect to a remote SMB/CIFS server

```python
smb = CfSmb(
    user='jdoe',
    password='superSecret',
    client_name='yoyo',
    server_name='windows_server1',
    server_ip='192.168.1.22',
    server_port='445',
    domain='mydomain',
    use_ntlm_v2=True,
    is_direct_tcp=True
)
```

* _user_ (str): SMB server username.
* _password_ (str): SMB server password.
* _client_name_ (str): Client machine name.
* _server_name_ (str): SMB server name.
* _server_ip_ (str): SMB server IP address or hostname.
* _server_port_ (str): SMB server port.  Default = `'445'`
* _domain_ (str): Domain used for authentication.
* _use_ntlm_v2_ (bool): Use NTLMv1 (False) or NTLMv2 (True) for authentication. Default = `True`
* _is_direct_tcp_ (bool): Use NetBIOS over TCP/IP (False) or direct TCP/IP (True) for communication. Default = `True`

### Query the SMB server for a list of shares

```python
shares = smb.get_shares()

for share in shares:
    print(share)
```

### Query the SMB server for a list of files in a directory on a share

```python
files = smb.get_files(
    share='my_share', 
    directory='/dir1/dir2/directory_of_stuff'
)
```

* _share_ (str): Remote SMB share.
* _directory_ (str): The remote directory to inspect.

### Download a file from the remote SMB server

```python
smb.download(
    share='my_share',
    source_path='/remote_dir1/remote_dir2/cool_beans.pdf',
    destination_path='c:/local_dir1/cool_beans.pdf')
```

* _share_ (str): Remote SMB share.
* _source_path_ (str): Full path of remote filename to download.
* _destination_path_ (str): Full path of destination filename on local machine.

### Upload a local file to the SMB server

```python
smb.upload(
    share='my_share',
    source_path='c:/local_dir1/cool_beans.pdf',
    destination_path='/remote_dir1/remote_dir2/cool_beans.pdf'
)
```

* _share_ (str): Remote SMB share.
* _source_path_ (str): Full path of local filename to upload.
* _destination_path_ (str): Full path of destination filename on Remote SMB server.

### Close the connection to a remote SMB server

```python
smb.close()
```
