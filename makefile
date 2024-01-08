# ----------------------------
# Makefile Options
# ----------------------------

NAME = MAINCOM
ICON = icon.png
DESCRIPTION = "Handles communication between TI-84 and Rasp Pi pico"
COMPRESSED = NO

CFLAGS = -Wall -Wextra -Oz
CXXFLAGS = -Wall -Wextra -Oz

# ----------------------------

include $(shell cedev-config --makefile)
