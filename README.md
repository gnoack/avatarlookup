# avatarlookup

Look up and display avatars for your contacts in mutt.

*Warning* Command line interface is still a bit unstable.

TODO: Write documentation. Add screenshot.

## Populating the Avatar database

The tough part you need to figure out yourself:
Get all your contacts in Vcard format.

Populate the database by piping your Vcards into:

    $ avatar-index < all-my-vcards.vcf

## Install in mutt

Add this line to your `.muttrc`:

    set display_filter="avatar-lookup --pipe-mail"

The display filters are meant for modifying the mails before display,
but the tool just writes out the same mail again, and - with a small
delay - draws a suitable avatar over the terminal.

