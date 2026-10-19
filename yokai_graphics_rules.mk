# Indexed presentation derivatives. Battle textures are centered without resize;
# the battle engine applies their hardware affine geometry at render time.
YOKAI_PRESENTATION_GFX := $(shell python3 tools/yokai/presentation_4bpp.py --list-targets)
YOKAI_BATTLE_GFX := $(filter %-battle.4bpp,$(YOKAI_PRESENTATION_GFX))
YOKAI_DISPLAY_GFX := $(filter-out $(YOKAI_BATTLE_GFX),$(YOKAI_PRESENTATION_GFX))
$(YOKAI_DISPLAY_GFX): %-display.4bpp: %.4bpp data/yokai/sprite_presentation.json tools/yokai/presentation_4bpp.py
	python3 tools/yokai/presentation_4bpp.py --input $< --output $@
$(YOKAI_BATTLE_GFX): %-battle.4bpp: %.4bpp data/yokai/sprite_presentation.json tools/yokai/presentation_4bpp.py
	python3 tools/yokai/presentation_4bpp.py --input $< --output $@
