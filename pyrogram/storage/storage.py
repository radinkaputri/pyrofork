#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

import base64
import struct
from abc import abstractmethod
from typing import List, Tuple


class Storage:
    OLD_SESSION_STRING_FORMAT = ">B?256sI?"
    OLD_SESSION_STRING_FORMAT_64 = ">B?256sQ?"
    SESSION_STRING_SIZE = 351
    SESSION_STRING_SIZE_64 = 356

    SESSION_STRING_FORMAT = ">BI?256sQ?15s39sB15s39sB"

    def __init__(self, name: str):
        self.name = name

    async def open(self):
        raise NotImplementedError

    async def save(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def delete(self):
        raise NotImplementedError

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        raise NotImplementedError

    async def update_usernames(self, usernames: List[Tuple[int, str]]):
        raise NotImplementedError

    @abstractmethod
    async def update_state(self, update_state: Tuple[int, int, int, int, int] = object):
        """Get or set the update state of the current session.

        Parameters:
            update_state (``Tuple[int, int, int, int, int]``): A tuple containing the update state to set.
                Tuple must contain the following information:
                - ``int``: The id of the entity.
                - ``int``: The pts.
                - ``int``: The qts.
                - ``int``: The date.
                - ``int``: The seq.
        """
        raise NotImplementedError

    async def get_peer_by_id(self, peer_id: int):
        raise NotImplementedError

    async def get_peer_by_username(self, username: str):
        raise NotImplementedError

    async def get_peer_by_phone_number(self, phone_number: str):
        raise NotImplementedError

    async def dc_id(self, value: int = object):
        raise NotImplementedError

    async def api_id(self, value: int = object):
        raise NotImplementedError

    async def test_mode(self, value: bool = object):
        raise NotImplementedError

    async def auth_key(self, value: bytes = object):
        raise NotImplementedError

    async def date(self, value: int = object):
        raise NotImplementedError

    async def user_id(self, value: int = object):
        raise NotImplementedError

    async def is_bot(self, value: bool = object):
        raise NotImplementedError

    async def server_address(self, value: str = object):
        raise NotImplementedError

    async def server_address_v6(self, value: str = object):
        raise NotImplementedError

    async def server_port(self, value: int = object):
        raise NotImplementedError

    async def media_address(self, value: str = object):
        raise NotImplementedError

    async def media_address_v6(self, value: str = object):
        raise NotImplementedError

    async def media_port(self, value: int = object):
        raise NotImplementedError

    async def export_session_string(self):
        server_ip = await self.server_address()
        server_ip_v6 = await self.server_address_v6()
        port_server = await self.server_port()
        media_ip = await self.media_address()
        media_ip_v6 = await self.media_address_v6()
        port_media = await self.media_port()
        # Add leading zero to make fixed size
        server_address = '.'.join(i.zfill(3) for i in server_ip.split('.'))
        server_address_v6 = ':'.join(i.zfill(4) for i in server_ip_v6.split(':'))
        server_port = f"{port_server}".zfill(5)
        media_address = '.'.join(i.zfill(3) for i in media_ip.split('.'))
        media_address_v6 = ':'.join(i.zfill(4) for i in media_ip_v6.split(':'))
        media_port = f"{port_media}".zfill(5)
        packed = struct.pack(
            self.SESSION_STRING_FORMAT,
            await self.dc_id(),
            await self.api_id(),
            await self.test_mode(),
            await self.auth_key(),
            await self.user_id(),
            await self.is_bot(),
            bytes(server_address.encode()),
            bytes(server_address_v6.encode()),
            bytes(server_port.encode()),
            bytes(media_address.encode()),
            bytes(media_address_v6.encode()),
            bytes(media_port.encode())
        )

        return base64.urlsafe_b64encode(packed).decode().rstrip("=")
