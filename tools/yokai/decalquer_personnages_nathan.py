#!/usr/bin/env python3
"""Compatibility entry point: export native pixel grids, never sample artwork.

The previous imagegen-to-native conversion has been replaced at the creator's
request. Edit source/overworld-grille.json to change an individual native pixel.
"""
from exporter_grilles_personnages import main
if __name__=='__main__':main()
