CeladonCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, LavenderResidence_Load
	map_script MAP_SCRIPT_ON_TRANSITION, LavenderResidence_Load
	.byte 0
LavenderResidence_Load::
	setflag FLAG_LAVENDER_HIDE_MATT
	clearflag FLAG_LAVENDER_HIDE_RESIDENT
	goto_if_set FLAG_BADGE04_GET, LavenderResidence_LoadEnd
	clearflag FLAG_LAVENDER_HIDE_MATT
	setflag FLAG_LAVENDER_HIDE_RESIDENT
LavenderResidence_LoadEnd::
	end
LavenderResidence_Matt::
	msgbox LavenderResidence_Text_Matt, MSGBOX_NPC
	end
LavenderResidence_Alyzon::
	lock
	faceplayer
	specialvar VAR_RESULT, LavanvilleRematchReady
	goto_if_eq VAR_RESULT, TRUE, LavenderResidence_PostLeague
	msgbox LavenderResidence_Text_Home
	release
	end
LavenderResidence_PostLeague::
	msgbox LavenderResidence_Text_Later
	release
	end
LavenderResidence_Text_Matt::
	.string "MATT: On dirait une Arène\nabandonnée. Personne à défier!\p"
	.string "La Championne vit à LAVANVILLE.\nBonne chance dans sa Tour!$"

LavenderResidence_Text_Home::
	.string "ALYZON: Ma deuxième maison!\nJe viens me reposer ici.\p"
	.string "Pas de combat aujourd'hui.\nMes zombies font la sieste!$"

LavenderResidence_Text_Later::
	.string "ALYZON: Le Panthéon, déjà!\nUne revanche me ferait plaisir.\p"
	.string "Laisse-moi préparer mon équipe.\nNous nous battrons plus tard!$"
