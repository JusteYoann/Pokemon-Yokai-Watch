#ifndef GUARD_SPIRATON_BATTLE_H
#define GUARD_SPIRATON_BATTLE_H
/* Shared scripted encounter arm; historical Prototype name retained for QA. */
void SpiratonBattleArmPrototype(void);
bool8 SpiratonBattlePrototypeArmed(void);
void SpiratonBattleReset(void);
void SpiratonBattleBegin(void);
bool8 SpiratonBattleIsBoss(u8 battler);
bool8 SpiratonBattlePresentationIsBoss(u8 battler);
bool8 SpiratonBattlePending(u8 battler);
bool8 SpiratonBattleIgnoreFaint(u8 battler);
bool8 SpiratonBattleFirstTurn(void);
bool8 SpiratonBattleEndTurn(void);
u16 SpiratonBattleTransformSpecies(u8 battler);
u32 SpiratonBattleInspect(u8 field);
extern const u8 gSpiratonBattleName[];
extern const u8 gSpiratonHealthboxName[];
#endif
