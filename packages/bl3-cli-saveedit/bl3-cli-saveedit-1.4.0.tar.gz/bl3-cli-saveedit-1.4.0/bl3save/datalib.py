#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

import io
import json
import lzma
import struct
import base64
import random
import binascii
import pkg_resources

class ArbitraryBits(object):
    """
    Ridiculous little object to deal with variable-bit-length packed data that
    we find inside item serial numbers.  This is super-inefficient on the
    large scale, but given that we're likely to only be dealing with hundreds of
    items at the absolute most (and more likely only dozens), it probably doesn't
    matter.

    Rather than doing clever things with bitwise operations and shifting data
    around, we're convering all the data into a string where each letter is a
    0 or 1, so we can just use regular Python indexing and slicing to do whatever
    we want with them.  A call to `int(data, 2)` on the string (or a bit of the
    string) will convert it back into a number for us.

    Many bits of data will span byte boundaries, and to properly handle the way
    they're packed, we're actually storing the data in backwards chunks of 8
    bits.  So when we mention the "front" of the data, we'll actually end up
    looking at the *end* of our internally-stored data, and vice-versa.  "Front"
    and "back" are used as if you're looking at the actual binary representation,
    not our own janky internal model.
    """

    def __init__(self, data=b''):
        self.data = ''.join([f'{d:08b}' for d in reversed(data)])

    def eat(self, bits):
        """
        Eats the specified number of `bits` off the front of the
        data and returns the value.  This is destructive; the data
        eaten off the front will no longer be in the data.
        """
        if bits > len(self.data):
            raise Exception('Attempted to read {} bits, but only {} remain'.format(bits, len(self.data)))
        val = int(self.data[-bits:], 2)
        self.data = self.data[:-bits]
        return val

    def append_value(self, value, bits):
        """
        Feeds the given `value` to the end of the data, using the given
        number of `bits` to do so.  We're assuming that `value` is
        an unsigned number.
        """
        value_data = struct.pack('>I', value)
        value_txt = ''.join([f'{d:08b}' for d in value_data])
        self.data = value_txt[-bits:] + self.data

    def append_data(self, new_data):
        """
        Appends the given `new_data` (from another ArbitraryBits object)
        to the end of our data.
        """
        self.data = new_data + self.data

    def get_data(self):
        """
        Returns our current data in binary format.  Will bad the end with
        `0` bits if we're not a multiple of 8.
        """
        # Pad with 0s if need be
        need_bits = (8-len(self.data)) % 8
        temp_data = '0'*need_bits + self.data

        # Now convert back to an actual bytearray
        byte_data = []
        for i in range(int(len(temp_data)/8)-1, -1, -1):
            byte_data.append(int(temp_data[i*8:(i*8)+8], 2))
        return bytearray(byte_data)

class BL3Serial(object):
    """
    Class to handle serializing and deserializing BL3 item/weapon serial
    numbers.
    """

    def __init__(self, serial, datawrapper):

        self.datawrapper = datawrapper
        self.serial_db = datawrapper.serial_db
        self.name_db = datawrapper.name_db
        self.set_serial(serial)

        # Attributes which get filled in when we parse
        self._version = None
        self._balance_bits = None
        self._balance_idx = None
        self._balance = None
        self._balance_short = None
        self._eng_name = None
        self._invdata_bits = None
        self._invdata_idx = None
        self._invdata = None
        self._manufacturer_bits = None
        self._manufacturer_idx = None
        self._manufacturer = None
        self._level = None
        self._remaining_data = None

    def set_serial(self, serial):
        """
        Sets our serial number
        """

        self.serial = serial
        (self.decrypted_serial, self.orig_seed) = BL3Serial._decrypt_serial(serial)
        self.parsed = False
        self.can_parse = True

    @staticmethod
    def _xor_data(data, seed):
        """
        Run some `data` through some XOR-based obfuscation, using the
        specified `seed`
        """

        # If the seed is 0, we basically don't do anything (though
        # make sure we return the same datatype as below)
        if seed == 0:
            return [d for d in data]

        # Because our seed can be negative, we do have to do the
        # & here, even though it might not seem to make sense to
        # do so.
        xor = (seed >> 5) & 0xFFFFFFFF
        temp = []
        for i, d in enumerate(data):
            xor = (xor * 0x10A860C1) % 0xFFFFFFFB
            temp.append((d ^ xor) & 0xFF)
        return temp

    @staticmethod
    def _bogodecrypt(data, seed):
        """
        "Decrypts" the given item `data`, using the given `seed`.
        """

        # First run it through the xor wringer.
        temp = BL3Serial._xor_data(data, seed)

        # Now rotate the data
        steps = (seed & 0x1F) % len(data)
        return bytearray(temp[-steps:] + temp[:-steps])

    @staticmethod
    def _bogoencrypt(data, seed):
        """
        "Encrypts" the given `data`, using the given `seed`
        """

        # Rotate first
        steps = (seed & 0x1F) % len(data)
        rotated = bytearray(data[steps:] + data[:steps])

        # Then run through the xor stuff
        return bytearray(BL3Serial._xor_data(rotated, seed))

    @staticmethod
    def _decrypt_serial(serial):
        """
        Decrypts (really just de-obfuscates) the serial number.
        """

        # Initial byte should always be 3
        assert(serial[0] == 3)

        # Seed does need to be an unsigned int
        orig_seed = struct.unpack('>i', serial[1:5])[0]

        # Do the actual "decryption"
        decrypted = BL3Serial._bogodecrypt(serial[5:], orig_seed)

        # Grab the CRC stored in the serial itself
        orig_checksum = bytearray(decrypted[:2])

        # Compute the checksum ourselves to make sure we've done
        # everything properly
        data_to_checksum = serial[:5] + b"\xFF\xFF" + decrypted[2:]
        computed_crc = binascii.crc32(data_to_checksum)
        computed_checksum = struct.pack('>H',
                ((computed_crc >> 16) ^ computed_crc) & 0xFFFF)
        if orig_checksum != computed_checksum:
            raise Exception('Checksum in serial ({}) does not match computed checksum ({})'.format(
                '0x{}'.format(''.join(f'{d:02X}' for d in orig_checksum)),
                '0x{}'.format(''.join(f'{d:02X}' for d in computed_checksum)),
                ))

        # Return what we decrypted
        return (decrypted[2:], orig_seed)

    @staticmethod
    def _encrypt_serial(data, seed=None):
        """
        Given an unencrypted `data`, return the binary serial number for
        the item, optionally with the given `seed`.  If `seed` is not passed in,
        a random one will be passed in.  Use a `seed` of `0` to not apply any
        encryption/obfuscation to the data
        """

        # Pick a random seed if one wasn't given.  Taken from the BL2 CLI editor
        if seed is None:
            seed = random.randrange(0x100000000) - 0x80000000

        # Construct our header and find the checksum
        header = struct.pack('>Bi', 3, seed)
        crc32 = binascii.crc32(header + b"\xFF\xFF" + data)
        checksum = struct.pack('>H', ((crc32 >> 16) ^ crc32) & 0xFFFF)

        # Return the freshly-encrypted item
        return header + BL3Serial._bogoencrypt(checksum + data, seed)

    def _get_inv_db_header_part(self, category, bits):
        """
        Given the category name `category`, and the ArbitraryBits object `bits`,
        containing serial number data, return a tuple containing:
            1) The category value
            2) The number of bits the category takes up
            3) The numerical index of the value
        This relies on being run during `_parse_serial`, so that `_version` is
        populated in our object.
        """
        num_bits = self.serial_db.get_num_bits(category, self._version)
        part_idx = bits.eat(num_bits)
        part_val = self.serial_db.get_part(category, part_idx)
        if not part_val:
            part_val = 'unknown'
        return (part_val, num_bits, part_idx)

    def _parse_serial(self):
        """
        Parse our serial number, at least up to the level.  We're not going
        to care about actual parts in here.
        """

        if not self.can_parse:
            return

        bits = ArbitraryBits(self.decrypted_serial)

        # First value should always be 128, apparently
        assert(bits.eat(8) == 128)

        # Grab the serial version and check it against the max version we know about
        self._version = bits.eat(7)
        if self._version > self.serial_db.max_version:
            self.can_parse = False
            return

        # Now the rest of the data we care about.
        (self._balance,
                self._balance_bits,
                self._balance_idx) = self._get_inv_db_header_part('InventoryBalanceData', bits)
        (self._invdata,
                self._invdata_bits,
                self._invdata_idx) = self._get_inv_db_header_part('InventoryData', bits)
        (self._manufacturer,
                self._manufacturer_bits,
                self._manufacturer_idx) = self._get_inv_db_header_part('ManufacturerData', bits)
        self._level = bits.eat(7)
        self._remaining_data = bits.data

        # At this point, if we were planning on reading parts, we'd read eat six
        # more bits to find the number of parts, then read in that many, using a
        # mapping to get to the correct category.  Then another four bits tells
        # us how many anointments there are, reading from InventoryGenericPartData
        # after that.  After anointments, I'm not totally sure what's out there.

        # Parse out a "short" balance name, for convenience's sake
        self._balance_short = self._balance.split('.')[-1]

        # If we know of an English name for this balance, use it
        self._eng_name = self.name_db.get(self._balance_short)

        # Mark down that we're parsed, now.
        self.parsed = True

    def _deparse_serial(self):
        """
        De-parses a serial; used after we make changes to the data that gets
        pulled out during `_parse_serial`.  At the moment, that's only going
        to be item level changes.  Will update the serial in the protobuf as
        well, and set the object to trigger a re-parse if anything else needs
        to read more.

        This is all pretty inefficient -- really we should just write over the
        bits values with the new values, in-place.  But whatever, this'll do
        for now.
        """

        if not self.can_parse:
            return

        # Construct the new item data
        bits = ArbitraryBits()
        bits.append_value(128, 8)
        bits.append_value(self._version, 7)
        bits.append_value(self._balance_idx, self._balance_bits)
        bits.append_value(self._invdata_idx, self._invdata_bits)
        bits.append_value(self._manufacturer_idx, self._manufacturer_bits)
        bits.append_value(self._level, 7)
        bits.append_data(self._remaining_data)
        new_data = bits.get_data()

        # Encode the new serial (using seed 0; unencrypted)
        new_serial = BL3Serial._encrypt_serial(new_data, 0)

        # Load in the new serial (this will set `parsed` to `False`)
        self.set_serial(new_serial)

    @property
    def balance(self):
        """
        Returns the balance for this item
        """
        if not self.parsed:
            self._parse_serial()
            if not self.can_parse:
                return None
        return self._balance

    @property
    def balance_short(self):
        """
        Returns the "short" balance for this item
        """
        if not self.parsed:
            self._parse_serial()
            if not self.can_parse:
                return None
        return self._balance_short

    @property
    def eng_name(self):
        """
        Returns an English name for the balance, if possible.  Will default
        to the "short" balance for this item if not.
        """
        if not self.parsed:
            self._parse_serial()
            if not self.can_parse:
                return None
        if self._eng_name:
            return self._eng_name
        else:
            return self._balance_short

    @property
    def level(self):
        """
        Returns the level of this item
        """
        if not self.parsed:
            self._parse_serial()
            if not self.can_parse:
                return None
        return self._level

    @level.setter
    def level(self, value):
        """
        Sets a new level for the item.  This would be a super inefficient way of
        doing it if we supported doing anything other than changing level -- we're
        rebuilding the whole serial right now and triggering a re-parse if anything
        decides to re-read it.  That should be sufficient for our purposes here,
        though.
        """
        if not self.parsed:
            self._parse_serial()
            if not self.can_parse:
                return None

        # Set the level and trigger a re-encode of the serial
        self._level = value
        self._deparse_serial()

    def get_serial_number(self, orig_seed=False):
        """
        Returns the binary item serial number.  If `orig_seed` is `True`, the
        serial number will use the same seed that was used in the savegame.
        Otherwise, it will use a seed of `0`, which will then be unencrypted.
        """
        if orig_seed:
            seed = self.orig_seed
        else:
            seed = 0
        return BL3Serial._encrypt_serial(self.decrypted_serial, seed)

    def get_serial_base64(self, orig_seed=False):
        """
        Returns the base64-encoded item serial number.  If `orig_seed` is
        `True`, the serial number will use the same seed that was used in the
        savegame.  Otherwise, it will use a seed of `0`, which will then be
        unencrypted.
        """
        return 'BL3({})'.format(base64.b64encode(self.get_serial_number(orig_seed)).decode('latin1'))

    @staticmethod
    def decode_serial_base64(new_data):
        """
        Decodes a `BL3()`-encoded item serial into a binary serial
        """
        if not new_data.lower().startswith('bl3(') or not new_data.endswith(')'):
            raise Exception('Unknown item format: {}'.format(new_data))
        encoded = new_data[4:-1]
        return base64.b64decode(encoded)

class InventorySerialDB(object):
    """
    Little wrapper to provide access to our inventory serial number DB
    """

    def __init__(self):
        self.initialized = False
        self.db = None
        self._max_version = -1

    def _initialize(self):
        """
        Actually read in our data.  Not doing this automatically because I
        only want to do it if we're doing an operation which requires it.
        """
        if not self.initialized:
            with lzma.open(io.BytesIO(pkg_resources.resource_string(
                    __name__, 'resources/inventoryserialdb.json.xz'
                    ))) as df:
                self.db = json.load(df)
            self.initialized = True

            # I generally shy away from complex one-liners like this, but eh?
            self._max_version = max(
                    [max([v['version'] for v in category['versions']]) for category in self.db.values()]
                    )

    @property
    def max_version(self):
        """
        Return the max version we can handle
        """
        if not self.initialized:
            self._initialize()
        return self._max_version

    def get_num_bits(self, category, version):
        """
        Returns the number of bits used for the specified `category`, using
        a serial with version `version`
        """
        if not self.initialized:
            self._initialize()
        cur_bits = self.db[category]['versions'][0]['bits']
        for cat_version in self.db[category]['versions']:
            if cat_version['version'] > version:
                return cur_bits
            elif version >= cat_version['version']:
                cur_bits = cat_version['bits']
        return cur_bits

    def get_part(self, category, index):
        """
        Given the specified `category`, return the part for `index`
        """
        if not self.initialized:
            self._initialize()
        if index < 1:
            return None
        else:
            if index > len(self.db[category]['assets']):
                return None
            else:
                return self.db[category]['assets'][index-1]

class BalanceToName(object):
    """
    Little wrapper to provide access to a mapping from Balance names (actually
    just the "short" version of those, without path) to English names that
    we can report on.
    """

    def __init__(self):
        self.initialized = False
        self.mapping = None

    def _initialize(self):
        """
        Actually read in our data.  Not doing this automatically because I
        only want to do it if we're doing an operation which requires it.
        """
        if not self.initialized:
            with lzma.open(io.BytesIO(pkg_resources.resource_string(
                    __name__, 'resources/short_name_balance_mapping.json.xz'
                    ))) as df:
                self.mapping = json.load(df)
            self.initialized = True

    def get(self, balance):
        """
        Returns an english mapping for the given balance, if we can.
        """
        if not self.initialized:
            self._initialize()
        if '/' in balance:
            balance = balance.split('/')[-1]
        if '.' in balance:
            balance = balance.split('.')[-1]
        balance = balance.lower()
        if balance in self.mapping:
            return self.mapping[balance]
        else:
            return None

class DataWrapper(object):
    """
    Weird little metaclass which just has an instance of each of our file-backed
    data objects in here.  This way apps using it can just pass around a single
    object instance and take what they want, rather than having to carry around
    multiple.  (For instance, BL3Item needs both InventorySerialDB and
    BalanceToName, and we instantiate a fair number of those.)
    """

    def __init__(self):
        self.serial_db = InventorySerialDB()
        self.name_db = BalanceToName()

