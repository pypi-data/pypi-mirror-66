# __init__.py

import logging
from typing import Union, List
from smb.SMBConnection import SMBConnection


logger = logging.getLogger(__name__)


class CfSmb(SMBConnection):

    def __init__(self, user: str, password: str, client_name: str, server_name: str, domain: str, server_ip: str,
                 server_port: Union[str, int] = '445', use_ntlm_v2: bool = True, is_direct_tcp: bool = True):
        """Connect to a remote SMB/CIFS server and perform file operations.

        Args:
            user: SMB server username.
            password: SMB server password.
            client_name: Client machine name.
            server_name: SMB server name.
            domain: Domain used for authentication.
            server_ip: SMB server IP address or hostname.
            server_port: SMB server port.
            use_ntlm_v2: Use NTLMv1 (False) or NTLMv2 (True) for authentication.
            is_direct_tcp: Use NetBIOS over TCP/IP (False) or direct TCP/IP (True) for communication.
        """

        super().__init__(
            username=user,
            password=password,
            my_name=client_name,
            remote_name=server_name,
            domain=domain,
            use_ntlm_v2=use_ntlm_v2,
            is_direct_tcp=is_direct_tcp
        )
        self.connect(
            ip=server_ip,
            port=int(server_port)
        )

    def upload(self, share: str, source_path: str, destination_path: str):
        """Upload a local file to the SMB server.

        Args:
            share: Remote SMB share.
            source_path: Full path of local filename to upload.
            destination_path: Full path of destination filename on Remote SMB server.
        """
        source_data = open(source_path, 'rb')
        self.storeFile(
            service_name=share,
            path=destination_path,
            file_obj=source_data
        )
        logger.debug(f'File has been uploaded: {source_path} -> {destination_path}')

    def download(self, share: str, source_path: str, destination_path: str):
        """Download a file from the remote SMB server

        Args:
            share: Remote SMB share.
            source_path: Full path of remote filename to download.
            destination_path: Full path of destination filename on local machine.
        """
        destination_data = open(destination_path, 'wb')  # Will overwrite if exist
        self.retrieveFile(
            service_name=share,
            path=source_path,
            file_obj=destination_data
        )
        logger.debug(f'File has been downloaded: {source_path} -> {destination_path}')

    def delete(self, share: str, file_path_glob: str):
        """Delete file(s) from the remote SMB share.

        Args:
            share: Remote SMB share.
            file_path_glob: A Python glob that contains the filepath of all files to delete.
        """
        # self.deleteFiles(share, file_path_glob)
        pass

    def get_files(self, share: str, directory: str) -> List[str]:
        """Query the SMB server for a list of files in a directory on a share.

        Args:
            share: Remote SMB share.
            directory: The remote directory to inspect.
        Returns:
            A list of files.
        """
        file_names = []
        files = self.listPath(share, directory)
        for file in files:
            file_names.append(file.filename)

        return file_names

    def get_shares(self) -> List[str]:
        """Query the SMB server for a list of shares.

        Returns:
            A list of shares.
        """
        share_names = []
        shares = self.listShares()

        for share in shares:
            share_names.append(share.name)

        return share_names
