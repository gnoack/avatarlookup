import os
import re

BASEPATH = "~/.cache/avatarlookup"


def _normalize_mail(address):
  address = address or ''
  address = address.strip().lower()
  address = re.sub(r'@(googlemail|gmail)\.(com|de)', '@gmail.com', address)
  return address


def _path(filename):
  return os.path.expanduser(os.path.join(BASEPATH, filename))


def maybe_create_cache():
  # Idempotent one-time set up.
  path = os.path.expanduser(BASEPATH)
  if not os.path.exists(path):
    os.mkdir(path)


def store(uid, photo_data):
  canonical_name = _path(uid)
  with open(canonical_name, "w") as writer:
    writer.write(photo_data)


def link(uid, email_address):
  email_address = _normalize_mail(email_address)
  try:
    os.symlink(_path(uid), _path(email_address))
  except OSError:
    pass  # idempotently


def lookup_filename(email_address):
  # May return a non-existing filename.
  return _path(_normalize_mail(email_address))
