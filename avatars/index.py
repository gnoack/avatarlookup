"""Index avatars by email from Vcards piped on stdin."""

import argparse
import sys
import vobject

from . import file_cache


def _populate_index_from_vcard(vcf, dry_run=False):
  if dry_run:
    from . import dry_run_cache
    cache = dry_run_cache
  else:
    cache = file_cache

  cache.maybe_create_cache()

  for card in vobject.readComponents(vcf):
    try:
      photo = card.photo
    except AttributeError:
      continue

    uid = card.uid.value
    cache.store(uid, photo.value)

    # Link email addresses.
    for child in card.getChildren():
      if child.name == "EMAIL":
        email_address = child.value
        cache.link(uid, email_address)


def main():
  parser = argparse.ArgumentParser(
    usage="%(prog)s [OPTIONS]",
    description=__doc__)
  parser.add_argument("-n", dest="dry_run", action="store_true",
                      help="Dry run mode (noop)")
  options = parser.parse_args(sys.argv[1:])

  _populate_index_from_vcard(sys.stdin, dry_run=options.dry_run)


if __name__ == "__main__":
  main()
