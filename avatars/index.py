"""Index avatars by email from Vcards piped on stdin."""
import sys
import vobject

from . import file_cache


def index(vcf):
  make_dir()

  for card in vobject.readComponents(vcf):
    try:
      photo = card.photo
    except AttributeError:
      continue

    uid = card.uid.value
    file_cache.store(uid, photo.value)

    # Link email addresses.
    for child in card.getChildren():
      if child.name == "EMAIL":
        email_address = child.value
        file_cache.link(uid, email_address)


def main():
  index(sys.stdin)


if __name__ == "__main__":
  main()
