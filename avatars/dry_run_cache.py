"""Dry-run version of the file_cache module."""


def maybe_create_cache():
  pass


def store(uid, photo_data):
  print("Store %s" % uid)


def link(uid, email_address):
  print("Link  %s <-> %s" % (uid, email_address))


# No lookup_filename, dry_run is just supported for indexing.
