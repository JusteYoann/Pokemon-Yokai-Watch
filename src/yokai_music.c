#include "global.h"
#include "gba/m4a_internal.h"
#include "constants/songs.h"
#include "yokai_music.h"

#ifdef YOKAI_PRIVATE_AUDIO
extern struct SongHeader *const gYokaiPrivateHeaders[20];
extern const u32 gYokaiPrivateAudioMask;
#endif

struct SongHeader *YokaiGetSongHeader(u16 song, struct SongHeader *fallback)
{
#ifdef YOKAI_PRIVATE_AUDIO
    if (song >= MUS_YOKAI_BICYCLE && song <= MUS_YOKAI_MINI_BOSS)
    {
        struct SongHeader *header = gYokaiPrivateHeaders[song - MUS_YOKAI_BICYCLE];
        if (header != NULL)
            return header;
    }
#endif
    return fallback;
}

u32 YokaiGetPrivateAudioMask(void)
{
#ifdef YOKAI_PRIVATE_AUDIO
    return gYokaiPrivateAudioMask;
#else
    return 0;
#endif
}
