#!/usr/bin/python2

import argparse
import email
import os
import sys
import time

from . import file_cache
from . import terminal

def _lookup(email_address):
  terminal.draw_image(file_cache.lookup_filename(email_address))


def main(args):
  parser = argparse.ArgumentParser(
    usage=("%(prog)s --pipe-mail < one_mail.mbox\n"
           "%(prog)s --email-address FOO@EXAMPLE.COM"),
    description=__doc__)
  parser.add_argument(
    "--pipe-mail", dest="pipe_mail",
    action="store_true",
    help="Mail filter behaviour (read and write mail on stdin/out)")
  parser.add_argument(
    "-e", "--email-address", dest="email_address",
    type=str, help="Email address to look up")
  options = parser.parse_args(args)

  if options.pipe_mail:
    # TODO: This needs cleanup.
    mail_content = sys.stdin.read()
    print(mail_content)
    pid = os.fork()
    if pid == -1:
      pass  # Broken
    elif pid == 0:
      time.sleep(0.05)
      _lookup(find_sender_mail(mail_content))
    else:
      #os.wait()
      pass  # Do not wait on purpose.
  elif options.email_address:
    _lookup(options.email_address)
  else:
    argparse.error("Missing argument.")


if __name__ == "__main__":
  main(sys.argv[1:])
