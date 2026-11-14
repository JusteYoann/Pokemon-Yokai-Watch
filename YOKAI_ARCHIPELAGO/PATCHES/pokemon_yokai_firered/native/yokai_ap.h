#ifndef GUARD_YOKAI_AP_H
#define GUARD_YOKAI_AP_H

#define YOKAI_AP_MAGIC 0x31504B59
#define YOKAI_AP_VERSION 1
#define YOKAI_AP_SAVE_OFFSET 0x300
#define YOKAI_AP_CMD_BIND 1
#define YOKAI_AP_CMD_ITEM 2
#define YOKAI_AP_ERR_SESSION 1
#define YOKAI_AP_ERR_SEQUENCE 2
#define YOKAI_AP_ERR_BAG_FULL 3
#define YOKAI_AP_ERR_ITEM 4
#define YOKAI_AP_ERR_UNBOUND 5

// These fields occupy only the audited gap between the Blasters party backup
// (0x000..0x260) and the vacuum's held BoxPokemon (0x380..0x3D0).
struct YokaiAPSave
{
    u32 magic;
    u16 version;
    u16 slot;
    u8 seed[16];
    u32 appliedCount;
    u32 lastItem;
    u8 reserved[32];
};

struct YokaiAPMailbox
{
    u32 magic;
    u16 version;
    u16 command;
    u16 slot;
    u16 itemId;
    u32 itemIndex;
    u8 seed[16];
    u32 appliedCount;
    u16 error;
    u8 ready;
    u8 bound;
    u16 checkBits;
    u8 goal;
    u8 reserved;
    u16 lastItemCount;
    u16 saveSchema;
};

struct YokaiAPRomInfo
{
    u32 magic;
    u16 version;
    u16 mailboxSize;
    u8 gameName[32];
    u8 baseSHA1[41];
};

extern EWRAM_DATA volatile struct YokaiAPMailbox gYokaiAPMailbox;
extern const struct YokaiAPRomInfo gYokaiAPRomInfo;
void YokaiAPUpdate(void);
void YokaiAPTryCollect(void);
#endif
