from _pylzmat import lib, ffi


def encode(data, encoding='latin-1'):
    size = len(data)
    outlen = (size) + ((size + 7) >> 3) + 0x21

    if isinstance( data, str ):
        data = bytes( data, encoding )
    elif isinstance( data, bytearray ):
        data = bytes(data)

    data_in = ffi.new("char[%d]" % size, data )
    data_out = ffi.new("char[%d]" % outlen)
    data_out_buff = ffi.buffer(data_out)
    data_out_len = ffi.new("MP_U32 *")
    data_out_len[0] = outlen

    ret = lib.lzmat_encode(data_out, data_out_len, data_in, len(data))
    if ret == 0:
        return data_out_buff[:data_out_len[0]]
    else:
        raise Exception('Return error: %d' % ret)


def decode(data, size=None, encoding='latin-1'):
    if size:
        outlen = size

    else:
        outlen = len(data) * 100

    if isinstance( data, str ):
        data = bytes( data, encoding )
    elif isinstance( data, bytearray ):
        data = bytes(data)

    data_in = ffi.new("char[%d]" % len(data), data)
    data_out = ffi.new("char[%d]" % outlen)
    data_out_buff = ffi.buffer(data_out)
    data_out_len = ffi.new("MP_U32 *")
    data_out_len[0] = outlen

    ret = lib.lzmat_decode(data_out, data_out_len, data_in, len(data))
    if ret == 0:
        return data_out_buff[:data_out_len[0]]
    else:
        raise Exception('Return error: %d' % ret)
