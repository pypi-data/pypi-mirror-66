import unittest
from string import ascii_uppercase

from caesar.caesar import Caesar

class TestCaesar(unittest.TestCase):
    def test_encryption(self):
        keys = (4, 21, 21)
        messages = (
            "AMBIDEXTROUS: Able to pick with equal skill a right-hand pocket or a left.",
            "GUILLOTINE: A machine which makes a Frenchman shrug his shoulders with good reason.",
            "IMPIETY: Your irreverence toward my deity."
        )
        encrypted_messages = (
            "EQFMHIbXVSYW:AEfpiAxsAtmgoA1mxlAiuyepAwomppAeAvmklx-lerhAtsgoixAsvAeApijxD",
            "bpdggjodiZ:RVR8vx349zRD34x3R8v6z.RvRa?z9x38v9R.3?B2R34.R.30B7yz?.RD4A3R200yR?zv.09U",
            "dhkdZot:Rt0B?R4??zCz?z9xzRA0Dv?yR8FRyz4AFU"
        )
        for key, message, encrypted_message in (zip(keys, messages, encrypted_messages)):
            with self.subTest(key=key, message=message, encrypted_message=encrypted_message):
                cipher = Caesar(key, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.')
                self.assertEqual(cipher.encrypt(message), encrypted_message)

    def test_decryption(self):
        keys = (15, 4)
        messages = (
            "ZXAI: P RDHIJBT HDBTIXBTH LDGC QN HRDIRWBTC XC PBTGXRP PCS PBTGXRPCH XC HRDIAPCS.",
            "MQTSWXSV: E VMZEP EWTMVERX XS TYFPMG LSRSVW."
        )
        decrypted_messages = (
            "KILT: A COSTUME SOMETIMES WORN BY SCOTCHMEN IN AMERICA AND AMERICANS IN SCOTLAND.",
            "IMPOSTOR: A RIVAL ASPIRANT TO PUBLIC HONORS."
        )
        for key, message, decrypted_message in (zip(keys, messages, decrypted_messages)):
            with self.subTest(key=key, message=message, decrypted_message=decrypted_message):
                cipher = Caesar(key, ascii_uppercase)
                self.assertEqual(cipher.decrypt(message), decrypted_message)
