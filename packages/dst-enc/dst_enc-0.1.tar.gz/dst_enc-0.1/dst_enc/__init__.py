#-*- coding: utf-8 -*-
"""
Copyright (c) 2020 Dst_207 | Mr.D`HACK

Author: Mr.D`HACK
Team: BlackCoderCrush
"""

"""
Buset bro niat amat sampe nyari kesini.
Yg dirikod sc bro bkn modul niat amat smpe kesini:v.
aowkaowok rikoders.
"""

import random
import base64
import sys
import os

def encode(text):
    """
    Random encode code Python.
    Usage:
       >>> import dst_enc
       >>> dst_enc('TextInHere')
    """
    sp=text
    aray=list("".join(sp))
    a=[]
    for i in aray:
        ra_enc = ['x\^@/','$\^D','@\$^@','\$@^@']
        a.append('\a$@^$')
        a.append(i)
        a.append(random.choice(ra_enc))

    return "".join(a)

def decode(text):
    """
    Decode code random encode.
    Usage:
       >>> import dst_enc
       >>> dst_enc.decode('TextEncode')
    """
    sp=text
    rsult=sp.replace('x\^@/','').replace('$\^D','').replace('@\$^@','').replace('\$@^@','').replace('\a$@^$','')
    return rsult


class base_dst:
      def __init__(self):
          pass

      def bs64encode(self,text):
          """
          Modifing Function base64 Encode.
          Usage:
             >>> import dst_enc
             >>> bs=dst_enc.base_dst()
             >>> bs.bs64encode('TextInHere')
          """
          self.text = text.encode('utf-8')
          bs = base64.b64encode(self.text)

          aray=list("".join(bs))
          a=[]

          for i in aray:
              a.append(i)
              a.append(random.choice(['$','@','@^','$^']))

          return "".join(a)

      def bs64decode(self,text):
          """
          Decoding Modifing base64 Encode.
          Usage:
             >>> import dst_enc
             >>> bs=dst_enc.base_dst()
             >>> bs.bs64decode('TextEncode')
          """
          self.text = text.encode("utf-8")
          repl = self.text.replace('$','').replace('@','').replace('@^','').replace('$^','')
          dc = base64.b64decode(repl)

          return dc

if __name__ == '__main__':
   pass
   sys.exit()
