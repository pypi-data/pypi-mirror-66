from .strkey import StrKey, encode_check, decode_check
from .xdr import Xdr


class MuxedAccount:
    def __init__(self, account_id, account_id_id):
        self.account_id = account_id
        self.account_id_id = account_id_id

    @property
    def account_id_muxed(self):
        packer = Xdr.StellarXDRPacker()
        packer.pack_int64(self.account_id_id)
        packer.pack_uint256(StrKey.decode_ed25519_public_key(self.account_id))
        data = packer.get_buffer()
        return encode_check("muxed_account", data)

    @classmethod
    def from_account_id_muxed(cls, account_id_muxed):
        xdr = decode_check("muxed_account", account_id_muxed)
        unpacker = Xdr.StellarXDRUnpacker(xdr)
        account_id_id = unpacker.unpack_int64()
        ed25519 = unpacker.unpack_uint256()
        account_id = StrKey.encode_ed25519_public_key(ed25519)
        return cls(account_id=account_id, account_id_id=account_id_id)

    def to_xdr_object(self):
        return StrKey.decode_muxed_account(self.account_id_muxed)

    def from_xdr_object(self, muxed_account_xdr_object):
        return StrKey.encode_muxed_account(muxed_account_xdr_object)
