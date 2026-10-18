# Presentation is derived from canonical indexed art at build time, never on GBA.
YOKAI_DISPLAY_GFX := $(shell python3 tools/yokai/presentation_4bpp.py --list-targets)
$(YOKAI_DISPLAY_GFX): %-display.4bpp: %.4bpp data/yokai/sprite_presentation.json tools/yokai/presentation_4bpp.py
	python3 tools/yokai/presentation_4bpp.py --input $< --output $@
