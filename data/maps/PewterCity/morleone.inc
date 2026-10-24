@ User-approved introduction. Wyatt joins the crowd with a scene-only actor.
@ Local object IDs 1,3,4 are existing residents; all previous IDs stay unchanged.
PewterCity_MorleoneOnTransition::
	goto_if_set FLAG_ARGENTA_MORLEONE_DONE, PewterCity_MorleoneHideActors
	goto_if_set FLAG_ARGENTA_MORLEONE_PENDING, PewterCity_MorleoneShowActors
	goto_if_set FLAG_WORLD_MAP_PEWTER_CITY, PewterCity_MorleoneLegacy
	getplayerxy VAR_TEMP_D, VAR_TEMP_E
	goto_if_lt VAR_TEMP_E, 36, PewterCity_MorleoneLegacy
	goto_if_lt VAR_TEMP_D, 20, PewterCity_MorleoneLegacy
	goto_if_gt VAR_TEMP_D, 23, PewterCity_MorleoneLegacy
	setflag FLAG_ARGENTA_MORLEONE_PENDING
PewterCity_MorleoneShowActors::
	clearflag FLAG_HIDE_ARGENTA_MAFIA
	clearflag FLAG_HIDE_ARGENTA_MATT
	return
PewterCity_MorleoneLegacy::
	setflag FLAG_ARGENTA_MORLEONE_DONE
PewterCity_MorleoneHideActors::
	setflag FLAG_HIDE_ARGENTA_MAFIA
	setflag FLAG_HIDE_ARGENTA_MATT
PewterCity_MorleoneReturn::
	return
PewterCity_EventScript_MorleoneArrival::
	goto_if_set FLAG_ARGENTA_MORLEONE_DONE, PewterCity_MorleoneEnd
	goto_if_unset FLAG_ARGENTA_MORLEONE_PENDING, PewterCity_MorleoneEnd
	lockall
	setvar VAR_TEMP_F, 1
	getplayerxy VAR_TEMP_D, VAR_TEMP_E
	msgbox Argenta_MattCall
	closemessage
	applymovement LOCALID_PLAYER, Argenta_Up1
	waitmovement 0
	call_if_eq VAR_TEMP_D, 20, Argenta_Normalize20
	call_if_eq VAR_TEMP_D, 21, Argenta_Normalize21
	call_if_eq VAR_TEMP_D, 22, Argenta_Normalize22
	applymovement LOCALID_ARGENTA_MATT, Argenta_MattApproach
	waitmovement 0
	applymovement LOCALID_PLAYER, Argenta_FaceRight
	waitmovement 0
	msgbox Argenta_MattInvite
	closemessage
	removeobject 1
	setobjectxyperm 1, 24, 11
	setobjectmovementtype 1, MOVEMENT_TYPE_FACE_UP
	addobject 1
	removeobject 3
	setobjectxyperm 3, 26, 11
	setobjectmovementtype 3, MOVEMENT_TYPE_FACE_UP
	addobject 3
	removeobject 4
	setobjectxyperm 4, 28, 11
	setobjectmovementtype 4, MOVEMENT_TYPE_FACE_UP
	addobject 4
	applymovement LOCALID_ARGENTA_MATT, Argenta_MattLead
	delay 24
	applymovement LOCALID_PLAYER, Argenta_PlayerFollow
	waitmovement 0
	special SpawnCameraObject
	fadenewbgm MUS_YOKAI_BADA_BING
	applymovement LOCALID_CAMERA, Argenta_CameraReveal
	waitmovement 0
	applymovement LOCALID_PLAYER, Argenta_Up2
	waitmovement 0
	msgbox Argenta_DonSpeech
	closemessage
	applymovement LOCALID_ARGENTA_MAFIA2, Argenta_Exit27
	waitmovement 0
	removeobject LOCALID_ARGENTA_MAFIA2
	applymovement LOCALID_ARGENTA_MAFIA4, Argenta_Exit27Lower
	waitmovement 0
	removeobject LOCALID_ARGENTA_MAFIA4
	applymovement LOCALID_ARGENTA_DON, Argenta_Exit25
	waitmovement 0
	removeobject LOCALID_ARGENTA_DON
	applymovement LOCALID_ARGENTA_MAFIA1, Argenta_Exit23
	waitmovement 0
	removeobject LOCALID_ARGENTA_MAFIA1
	applymovement LOCALID_ARGENTA_MAFIA3, Argenta_Exit23Lower
	waitmovement 0
	removeobject LOCALID_ARGENTA_MAFIA3
	applymovement 1, Argenta_Crowd1Exit
	waitmovement 0
	applymovement 3, Argenta_Crowd3Exit
	waitmovement 0
	applymovement 4, Argenta_Crowd4Exit
	waitmovement 0
	applymovement LOCALID_ARGENTA_WYATT, Argenta_WyattExit
	waitmovement 0
	removeobject LOCALID_ARGENTA_WYATT
	fadedefaultbgm
	applymovement LOCALID_CAMERA, Argenta_CameraReturn
	waitmovement 0
	special RemoveCameraObject
	removeobject 1
	setobjectxyperm 1, 6, 15
	setobjectmovementtype 1, MOVEMENT_TYPE_LOOK_AROUND
	addobject 1
	removeobject 3
	setobjectxyperm 3, 21, 28
	setobjectmovementtype 3, MOVEMENT_TYPE_FACE_DOWN
	addobject 3
	removeobject 4
	setobjectxyperm 4, 33, 27
	setobjectmovementtype 4, MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT
	addobject 4
	applymovement LOCALID_ARGENTA_MATT, Argenta_FaceLeft
	waitmovement 0
	applymovement LOCALID_PLAYER, Argenta_FaceRight
	waitmovement 0
	msgbox Argenta_MattExplain
	closemessage
	applymovement LOCALID_ARGENTA_MATT, Argenta_MattExit
	waitmovement 0
	removeobject LOCALID_ARGENTA_MATT
	setflag FLAG_ARGENTA_MORLEONE_DONE
	clearflag FLAG_ARGENTA_MORLEONE_PENDING
	releaseall
PewterCity_MorleoneEnd::
	end
Argenta_Normalize20::
	applymovement LOCALID_PLAYER, Argenta_Right3
	waitmovement 0
	return
Argenta_Normalize21::
	applymovement LOCALID_PLAYER, Argenta_Right2
	waitmovement 0
	return
Argenta_Normalize22::
	applymovement LOCALID_PLAYER, Argenta_Right1
	waitmovement 0
	return
Argenta_Up1::
	walk_up
	step_end
Argenta_Up2::
	walk_up
	walk_up
	step_end
Argenta_Right1::
	walk_right
	step_end
Argenta_Right2::
	walk_right
	walk_right
	step_end
Argenta_Right3::
	walk_right
	walk_right
	walk_right
	step_end
Argenta_MattApproach::
	walk_down
	face_left
	step_end
Argenta_FaceRight::
	face_right
	step_end
Argenta_FaceLeft::
	face_left
	step_end
Argenta_MattLead::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	face_up
	step_end
Argenta_PlayerFollow::
	walk_right
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end
Argenta_CameraReveal::
	walk_up
	walk_up
	walk_up
	walk_up
	step_end
Argenta_CameraReturn::
	walk_down
	walk_down
	step_end
Argenta_Exit23::
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end
Argenta_Exit25::
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end
Argenta_Exit27::
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end
Argenta_Exit23Lower::
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end
Argenta_Exit27Lower::
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end
Argenta_Crowd1Exit::
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end
Argenta_Crowd3Exit::
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end
Argenta_Crowd4Exit::
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	step_end
Argenta_MattExit::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

@ This open column avoids the crowd and leaves the revealed camera view.
Argenta_WyattExit::
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end
