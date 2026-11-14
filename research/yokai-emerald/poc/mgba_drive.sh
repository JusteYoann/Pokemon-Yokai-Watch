#!/usr/bin/env bash
# Pilote mGBA (Qt, 0.10) dans un écran X virtuel (Xvfb) et capture l'image de l'émulateur (F12 de mGBA).
# Usage : mgba_drive.sh ROM DOSSIER_SORTIE "étapes"   (chemins absolus)
# étapes : "key:TOUCHE:N" (appuyer N fois ; X = A, Z = B, Return = Start, Up/Down/Left/Right),
#          "wait:S", "shot:nom" (capture -> DOSSIER/nom.png), "hold:TOUCHE:S",
#          "save:N" (état Maj+FN -> <rom>.ssN, copié en DOSSIER/stateN.ss)
# Variable STATE=fichier.ss : reprendre depuis un état sauvegardé (option -t de mGBA).
# Dépendances : mgba-qt, xvfb, xdotool. Les captures montrent le jeu : ne pas les versionner.
set -u
ROM=$1; OUT=$2; STEPS=$3; mkdir -p "$OUT/home/.config/mgba"
# sans carte son, l'émulation reste figée tant que audioSync est actif ; displayDriver=0 = rendu logiciel
[ -f "$OUT/home/.config/mgba/qt.ini" ] || printf '[ports.qt]\ndisplayDriver=0\nshowLibrary=0\npauseOnFocusLost=0\nmute=1\nupdateAutoCheck=0\naudioSync=0\nvideoSync=0\n' > "$OUT/home/.config/mgba/qt.ini"
export SDL_AUDIODRIVER=dummy
export DISPLAY=:99
Xvfb :99 -screen 0 800x600x24 >/dev/null 2>&1 & XPID=$!
sleep 1
HOME=$OUT/home /usr/games/mgba-qt -C mute=1 -3 ${STATE:+-t "$STATE"} "$ROM" >"$OUT/mgba.log" 2>&1 & MPID=$!
sleep 4
WIN=$(xdotool search --pid $MPID 2>/dev/null | tail -1)
xdotool windowactivate --sync $WIN 2>/dev/null; xdotool windowfocus $WIN 2>/dev/null
for s in $STEPS; do
  IFS=: read -r cmd a b <<<"$s"
  case $cmd in
    key) for i in $(seq 1 ${b:-1}); do xdotool keydown --window $WIN $a; sleep 0.12; xdotool keyup --window $WIN $a; sleep 0.5; done;;
    wait) sleep $a;;
    save) xdotool key --window $WIN shift+F$a; sleep 1; cp "${ROM%.*}.ss$a" "$OUT/state$a.ss" 2>/dev/null;;
    hold) xdotool keydown --window $WIN $a; sleep $b; xdotool keyup --window $WIN $a;;
    shot) xdotool key --window $WIN F12; sleep 1; f=$(ls -t "$(dirname "$ROM")"/*.png 2>/dev/null | head -1); [ -n "$f" ] && mv "$f" "$OUT/$a.png";;
  esac
done
kill $MPID; sleep 1; kill $XPID
