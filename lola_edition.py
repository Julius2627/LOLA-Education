"""Edition setting: which modes this copy of LOLA contains.

The development repository contains all modes. Each published edition gets its own version of this
file that lists only its modes, and ships only the folders of those modes plus common/.
Possible modes: "education", "applied", "research". With a single mode, START opens it directly.
"""
MODES = ("education",)
