#include "global.h"
#include "nuzlocke.h"
#include "battle.h"
#include "gflib.h"
#include "pokemon_storage_system.h"
#include "pokedex.h"
#include "save.h"
#include "main.h"
#include "overworld.h"
#include "menu.h"
#include "text_window.h"
#include "sound.h"
#include "event_data.h"
#include "constants/flags.h"
#include "constants/pokedex.h"

EWRAM_DATA bool8 gNewGameNuzlocke = FALSE;
static EWRAM_DATA bool8 sFirstEncounterEligible = FALSE;
const u8 gText_NuzlockeCaptureBlocked[] = _("Nuzlocke : espèce déjà obtenue\nou première rencontre déjà passée.");
static const u8 sGameOver[] = _("FIN DU DÉFI NUZLOCKE\nAucun Yo-kai n'a survécu.\nLa sauvegarde a été effacée.\n\nAppuie sur A pour recommencer.");
static const struct BgTemplate sBg[] = {{.bg = 0, .mapBaseIndex = 31}};
static const struct WindowTemplate sWindow[] = {{.bg = 0, .tilemapLeft = 2, .tilemapTop = 4, .width = 26, .height = 12, .paletteNum = 15, .baseBlock = 1}, DUMMY_WIN_TEMPLATE};
static const u8 sColors[] = {TEXT_COLOR_WHITE, TEXT_COLOR_DARK_GRAY, TEXT_COLOR_LIGHT_GRAY};

bool8 NuzlockeEnabled(void)
{
    return gSaveBlock1Ptr != NULL && gSaveBlock1Ptr->nuzlocke.magic == NUZLOCKE_SAVE_MAGIC;
}

void NuzlockeInit(void)
{
    if (gNewGameNuzlocke)
        gSaveBlock1Ptr->nuzlocke.magic = NUZLOCKE_SAVE_MAGIC;
    gNewGameNuzlocke = FALSE;
}

bool8 NuzlockeIsDead(struct Pokemon *mon)
{
    return NuzlockeEnabled() && (GetMonData(mon, MON_DATA_UNUSED_RIBBONS) & 1);
}

void NuzlockeMarkDead(struct Pokemon *mon)
{
    u8 ribbons;
    if (!NuzlockeEnabled() || !GetMonData(mon, MON_DATA_SPECIES) || GetMonData(mon, MON_DATA_IS_EGG))
        return;
    ribbons = GetMonData(mon, MON_DATA_UNUSED_RIBBONS) | 1;
    SetMonData(mon, MON_DATA_UNUSED_RIBBONS, &ribbons);
    mon->hp = 0;
}

bool8 NuzlockeBattleApplies(void)
{
    return NuzlockeEnabled() && !(gBattleTypeFlags & (BATTLE_TYPE_LINK | BATTLE_TYPE_OLD_MAN_TUTORIAL | BATTLE_TYPE_POKEDUDE));
}

void NuzlockeRecordOwned(struct Pokemon *mon)
{
    u16 species;
    if (!NuzlockeEnabled()) return;
    species = GetMonData(mon, MON_DATA_SPECIES);
    if (species == SPECIES_NONE || species >= NUM_SPECIES || GetMonData(mon, MON_DATA_IS_EGG)) return;
    gSaveBlock1Ptr->nuzlocke.ownedSpecies[species / 8] |= 1 << (species % 8);
    gSaveBlock1Ptr->nuzlocke.started = TRUE;
}

static bool8 SpeciesAlreadyObtained(u16 species)
{
    if (species == SPECIES_NONE || species >= NUM_SPECIES) return TRUE;
    return (gSaveBlock1Ptr->nuzlocke.ownedSpecies[species / 8] & (1 << (species % 8)))
        || GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_GET_CAUGHT);
}

void NuzlockeBeginBattle(void)
{
    u8 zone;
    u16 species;
    sFirstEncounterEligible = FALSE;
    if (!NuzlockeBattleApplies() || (gBattleTypeFlags & (BATTLE_TYPE_TRAINER | BATTLE_TYPE_GHOST | BATTLE_TYPE_LAVENDER_ZOMBIE))
        || !FlagGet(FLAG_SYS_POKEDEX_GET)) return;
    species = GetMonData(&gEnemyParty[0], MON_DATA_SPECIES);
    // Duplicate species and shinies do not consume the normal encounter.
    if (SpeciesAlreadyObtained(species) || IsMonShiny(&gEnemyParty[0])) return;
    zone = gMapHeader.regionMapSectionId;
    if (!(gSaveBlock1Ptr->nuzlocke.capturedZones[zone / 8] & (1 << (zone % 8))))
    {
        sFirstEncounterEligible = TRUE;
        gSaveBlock1Ptr->nuzlocke.capturedZones[zone / 8] |= 1 << (zone % 8);
    }
}

bool8 NuzlockeCanCapture(struct Pokemon *mon)
{
    if (!NuzlockeBattleApplies() || !FlagGet(FLAG_SYS_POKEDEX_GET) || IsMonShiny(mon)) return TRUE;
    return sFirstEncounterEligible && !SpeciesAlreadyObtained(GetMonData(mon, MON_DATA_SPECIES));
}

void NuzlockeRecordCapture(struct Pokemon *mon)
{
    if (!NuzlockeBattleApplies()) return;
    // The zone was consumed at encounter start, even if no Ball was thrown.
    NuzlockeRecordOwned(mon);
}

// Return 0: continue, 1: rescued by a PC survivor, 2: definitive game over.
// Called only after battle resources are no longer using party slot indices,
// or after all field-poison messages. Never during a switch or an attack.
u8 NuzlockeResolveParty(void)
{
    u8 i, count = 0, box, slot;
    if (!NuzlockeEnabled() || !gSaveBlock1Ptr->nuzlocke.started) return 0;
    for (i = 0; i < PARTY_SIZE; i++)
    {
        struct Pokemon *mon = &gPlayerParty[i];
        if (!GetMonData(mon, MON_DATA_SPECIES)) continue;
        if (!GetMonData(mon, MON_DATA_IS_EGG) && !GetMonData(mon, MON_DATA_HP)) NuzlockeMarkDead(mon);
        if (NuzlockeIsDead(mon)) continue;
        if (count != i) gPlayerParty[count] = *mon;
        count++;
    }
    for (i = count; i < PARTY_SIZE; i++) ZeroMonData(&gPlayerParty[i]);
    gPlayerPartyCount = count;
    for (i = 0; i < count; i++)
        if (!GetMonData(&gPlayerParty[i], MON_DATA_IS_EGG) && GetMonData(&gPlayerParty[i], MON_DATA_HP)) return 0;
    for (box = 0; box < TOTAL_BOXES_COUNT; box++)
    {
        for (slot = 0; slot < IN_BOX_COUNT; slot++)
        {
            struct BoxPokemon *mon = GetBoxedMonPtr(box, slot);
            if (!GetBoxMonData(mon, MON_DATA_SPECIES) || GetBoxMonData(mon, MON_DATA_IS_EGG)
                || (GetBoxMonData(mon, MON_DATA_UNUSED_RIBBONS) & 1)) continue;
            // If the party contains six eggs, exchange the first egg with the
            // survivor rather than overwriting or silently deleting an egg.
            {
                struct BoxPokemon egg;
                if (count == PARTY_SIZE) egg = gPlayerParty[0].box;
                BoxMonToMon(mon, &gPlayerParty[count == PARTY_SIZE ? 0 : count]);
                if (count == PARTY_SIZE) *mon = egg;
                else { ZeroBoxMonData(mon); gPlayerPartyCount = count + 1; }
            }
            return 1;
        }
    }
    return 2;
}

static void VBlank_GameOver(void)
{
    TransferPlttBuffer();
}

static void CB2_WaitGameOver(void)
{
    if (JOY_NEW(A_BUTTON)) DoSoftReset();
}

static void CB2_InitGameOver(void)
{
    SetVBlankCallback(NULL);
    SetHBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    ResetPaletteFade();
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    ResetBgsAndClearDma3BusyFlags(FALSE);
    InitBgsFromTemplates(0, sBg, ARRAY_COUNT(sBg));
    ChangeBgX(0, 0, 0); ChangeBgY(0, 0, 0);
    InitWindows(sWindow);
    DeactivateAllTextPrinters();
    LoadStdWindowGfx(0, 0x200, BG_PLTT_ID(15));
    FillWindowPixelBuffer(0, PIXEL_FILL(1));
    PutWindowTilemap(0);
    AddTextPrinterParameterized4(0, FONT_NORMAL, 0, 0, 0, 1, sColors, 0, sGameOver);
    CopyWindowToVram(0, COPYWIN_FULL);
    ShowBg(0);
    SetVBlankCallback(VBlank_GameOver);
    SetMainCallback2(CB2_WaitGameOver);
}

void NuzlockeGameOver(void)
{
    if (!NuzlockeEnabled()) return;
    // Erase both rotating save slots: the previous slot must not resurrect a run.
    StopMapMusic();
    ClearSaveData();
    SetMainCallback1(NULL);
    SetMainCallback2(CB2_InitGameOver);
}
