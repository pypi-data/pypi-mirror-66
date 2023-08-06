#!/usr/bin/env python3

import hmac
import hashlib

from .utils.utils import \
    decodeint, encodepoint, scalarmultbase,\
    sc_reduce32, sc_muladd, _verify


def prune_root_scalar(s_str):
    s_bytes = bytes.fromhex(s_str)
    s = bytearray(s_bytes)
    s[0] = s[0] & 248
    s[31] = s[31] & 31  # clear top 3 bits
    s[31] = s[31] | 64  # set second highest bit
    return s


def get_root_xprivate(seed_hexstr):
    hc_hexstr = hmac.HMAC(b'Root', bytes.fromhex(seed_hexstr), digestmod=hashlib.sha512).hexdigest()
    root_xprivate_hexstr = prune_root_scalar(hc_hexstr[:64]).hex() + hc_hexstr[64:]
    return root_xprivate_hexstr


def get_xpublic(xprivate):
    xprivate_bytes = bytes.fromhex(xprivate)
    scalar = decodeint(xprivate_bytes[:len(xprivate_bytes)//2])
    buf = encodepoint(scalarmultbase(scalar))
    xpublic = buf + xprivate_bytes[len(xprivate_bytes)//2:]
    xpublic = xpublic.hex()
    return xpublic


def get_expanded_private_key(xprivate):
    hc_hexstr = hmac.HMAC(b"Expand", bytes.fromhex(xprivate), digestmod=hashlib.sha512).hexdigest()
    expanded_private_key_hexstr = xprivate[:64] + hc_hexstr[64:]
    return expanded_private_key_hexstr


def get_public_key(xpublic):
    public_key_hexstr = xpublic[:64]
    return public_key_hexstr


def prune_intermediate_scalar(f):
    f = bytearray(f)
    f[0] = f[0] & 248       # clear bottom 3 bits
    f[29] = f[29] & 1       # clear 7 high bits
    f[30] = 0               # clear 8 bits
    f[31] = 0               # clear 8 bits
    return f


def sign(private, message):
    private = get_expanded_private_key(private)
    private_bytes = bytes.fromhex(private)
    message_bytes = bytes.fromhex(message)
    data_bytes = private_bytes[32:64] + message_bytes

    message_digest = hashlib.sha512(data_bytes).digest()
    message_digest = sc_reduce32(message_digest.hex().encode())
    message_digest = bytes.fromhex(message_digest.decode())
    message_digest_reduced = message_digest[0:32]

    scalar = decodeint(message_digest_reduced)
    encoded_r = encodepoint(scalarmultbase(scalar))
    public = get_xpublic(private)
    public_bytes = bytes.fromhex(public)
    hram_digest_data = encoded_r + public_bytes[:32] + message_bytes

    hram_digest = hashlib.sha512(hram_digest_data).digest()
    hram_digest = sc_reduce32(hram_digest.hex().encode())
    hram_digest = bytes.fromhex(hram_digest.decode())
    hram_digest_reduced = hram_digest[0:32]

    sk = private_bytes[:32]
    s = sc_muladd(hram_digest_reduced.hex().encode(), sk.hex().encode(), message_digest_reduced.hex().encode())
    s = bytes.fromhex(s.decode())

    signature_bytes = encoded_r + s
    signature = signature_bytes.hex()
    return signature


def verify(public, message, signature):
    return _verify(get_public_key(public), signature, message)
