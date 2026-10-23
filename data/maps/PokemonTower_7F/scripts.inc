PokemonTower_7F_MapScripts::
	.byte 0

PokemonTower_7F_EventScript_Grunt1::
	trainerbattle_single TRAINER_BUG_MANIAC, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

PokemonTower_7F_EventScript_Grunt2::
	trainerbattle_single TRAINER_RS_PSYCHIC_M, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

PokemonTower_7F_EventScript_Grunt3::
	trainerbattle_single TRAINER_RS_PSYCHIC_F, LavenderZombie_Text_Challenge, LavenderZombie_Text_Defeat
	msgbox LavenderZombie_Text_Calm, MSGBOX_AUTOCLOSE
	end

PokemonTower_7F_EventScript_MrFuji::
	lock
	faceplayer
	goto_if_set FLAG_BADGE04_GET, LavenderAlyzon_After
	trainerbattle_single TRAINER_LEADER_ERIKA, LavenderAlyzon_Text_Intro, LavenderAlyzon_Text_Defeat, LavenderAlyzon_Won, NO_MUSIC
	goto LavenderAlyzon_Won
LavenderAlyzon_Won::
	setflag FLAG_DEFEATED_ERIKA
	setflag FLAG_BADGE04_GET
	set_gym_trainers 4
	msgbox LavenderAlyzon_Text_Badge
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
LavenderAlyzon_After::
	goto_if_set FLAG_GOT_TM19_FROM_ERIKA, LavenderAlyzon_Return
	checkitemspace ITEM_TM19
	goto_if_eq VAR_RESULT, FALSE, LavenderAlyzon_NoRoom
	giveitem ITEM_TM19
	setflag FLAG_GOT_TM19_FROM_ERIKA
	msgbox LavenderAlyzon_Text_TM
LavenderAlyzon_Return::
	msgbox LavenderAlyzon_Text_After
	release
	end
LavenderAlyzon_NoRoom::
	msgbox LavenderAlyzon_Text_NoRoom
	release
	end
LavenderAlyzon_Text_Intro::
	.string "ALYZON: Te voilà! Tu as gravi\nma Tour jusqu'au bout!\p"
	.string "Mes petits zombies sont mignons,\nmais ils ne font pas de cadeaux!\p"
	.string "Un dernier obstacle avant ton\nbadge: moi. Montre-moi ton talent!$"

LavenderAlyzon_Text_Defeat::
	.string "Même mes chouchous ont craqué!\nTu es un formidable Dresseur!$"

LavenderAlyzon_Text_Badge::
	.string "ALYZON: Tu mérites le BADGE\nPRISME! Le quatrième badge!\p"
	.string "Tes Yo-kai pourront utiliser\nFORCE hors des combats.\p"
	.string "À CÉLADOPOLE, le repaire de la\nMAFIAMILLE te sera accessible.$"

LavenderAlyzon_Text_TM::
	.string "Voici aussi la CT19. Garde-la!\nUn cadeau qui ne mord pas.$"

LavenderAlyzon_Text_After::
	.string "ALYZON: Reviens voir mes petits!\nIls adorent les nouvelles têtes.\p"
	.string "Moi, je passe parfois dans ma\nseconde maison à CÉLADOPOLE.$"

LavenderAlyzon_Text_NoRoom::
	.string "Ton SAC est plein. Fais de la\nplace et reviens pour ta CT19!$"

LavenderZombie_Text_Challenge::
	.string "Grrr... Mes Yo-kai aussi\nveulent jouer!$"

LavenderZombie_Text_Defeat::
	.string "Grr... Bien joué...$"

LavenderZombie_Text_Calm::
	.string "Grr... Je me repose.\nTu peux passer...$"
