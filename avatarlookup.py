#!/usr/bin/python2

import email
import os
import re
import subprocess
import sys
import time
import vobject


W3MIMGDISPLAY = "/usr/lib/w3m/w3mimgdisplay"
BASEPATH = "~/.cache/avatarlookup"


def normalize_mail(address):
  address = address.strip().lower()
  address = re.sub(r'@(googlemail|gmail)\.(com|de)', '@gmail.com', address)
  return address


def path(filename):
  return os.path.expanduser(os.path.join(BASEPATH, filename))


def make_dir():
  path = os.path.expanduser(BASEPATH)
  if not os.path.exists(path):
    os.mkdir(path)


def convert(vcf):
  make_dir()

  for card in vobject.readComponents(vcf):
    try:
      photo = card.photo
    except AttributeError:
      continue

    canonical_name = path("%s.%s" % (card.uid.value, photo.params['TYPE'][0]))
    with open(canonical_name, "w") as writer:
      writer.write(photo.value)

    # Link email addresses.
    for child in card.getChildren():
      if child.name == "EMAIL":
        email_address = normalize_mail(child.value)
        try:
          os.link(canonical_name, path(email_address))
        except OSError:
          pass  # idempotently


def lookup(name):
  if not name:
    return

  filename = path(name)
  if os.path.exists(filename):
    windowsize_str = subprocess.check_output((W3MIMGDISPLAY, "-test"))
    windowx, windowy = map(int, windowsize_str.strip().split(" "))
    w, h = 48, 48
    x = windowx - w - 8 * 2
    y = 0 + 16 * 2

    drawing = subprocess.Popen(W3MIMGDISPLAY, stdin=subprocess.PIPE)
    drawing.stdin.write("0;1;%s;%s;%s;%s;;;;;%s\n4;\n3;" %
                        (x, y, w, h, filename))
    drawing.communicate()


def find_sender_mail(reader):
  mail = email.message_from_string(reader)
  addresses = email.utils.getaddresses(mail.get_all('From', []))
  if not addresses:
    return None
  addr_name, addr_email = addresses[0]
  return normalize_mail(addr_email)


def main(args):
  if args[1] == "--index":
    convert(sys.stdin)
  elif args[1] == "--lookup":
    lookup(args[2])
  elif args[1] == "--lookup-from-mail":
    mail_content = sys.stdin.read()
    print mail_content
    pid = os.fork()
    if pid == -1:
      pass  # Broken
    elif pid == 0:
      time.sleep(0.05)
      lookup(find_sender_mail(mail_content))
    else:
      #os.wait()
      pass  # Do not wait on purpose.
  else:
    sys.exit("bad args, use --index or --lookup EMAIL")


if __name__ == "__main__":
  main(sys.argv)
