Test_EventScript_NPC::
	msgbox Test_Text_WelcomeToWorldOfPokemon, MSGBOX_NPC
	end

EventScript_TestSignpostMsg::
	msgbox Test_Text_ThisIsASignpost, MSGBOX_SIGN
	end

Test_EventScript_CoordEvent::
	msgbox Test_Text_ThisIsACoordEvent, MSGBOX_SIGN
	end

Test_Text_WelcomeToWorldOfPokemon::
    .string "Message de test !\nBienvenue dans le monde des Yo-kai !$"

Test_Text_ThisIsASignpost::
    .string "Message de test !\nCeci est un panneau.$"

Test_Text_ThisIsACoordEvent::
    .string "Message de test !\nCeci est un événement de case.$"

	.align 2
Test_Text_Empty::
	.string "$"
