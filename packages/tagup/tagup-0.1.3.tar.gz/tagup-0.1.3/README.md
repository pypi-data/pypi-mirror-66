# tagup

**tagup** is a Python module which provides a reference implementation of the [Tagup Language](https://fairburn.dev/tagup/).

This module currently implements [version 1.0.0](https://fairburn.dev/tagup/1.0.0/) of the Tagup Language.

## Changelog

**v0.1.3**

- Fixed bug where the "trim_args" option didn't properly remove leading and trailing whitespace in some situations.

**v0.1.2**

- Fixed bug where code called "trim()" rather than "strip()."

**v0.1.1**

- Added non-standard option to trim whitespace from arguments before tag evaluation.
- Fixed bug where whitespace was considered when specifying a name/position for argument substitution.

**v0.1.0**

- Initial release.
