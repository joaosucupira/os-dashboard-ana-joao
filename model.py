# A regra de negócio que modela os dados e define como se comportam 
# os elementos sem se preocupar com visualização e acesso

import ctypes
from ctypes import c_ulong, c_char, Structure


class Process(Structure):
    _fields_ = [
        ("pid", c_ulong),
        ("name", c_char * 256),
        ("status", c_char * 64),
        ("user", c_char * 128),
    ]

# class System