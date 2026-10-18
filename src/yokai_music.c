#include "global.h"
#include "m4a.h"
#include "constants/songs.h"
#include "yokai_music.h"

#ifdef YOKAI_PRIVATE_AUDIO
extern struct SongHeader *const gYokaiPrivateHeaders[YOKAI_MUSIC_SLOT_COUNT];
extern const u32 gYokaiPrivateAudioMask;
#endif

struct SongHeader *YokaiGetSongHeader(u16 song, struct SongHeader *fallback)
{
#ifdef YOKAI_PRIVATE_AUDIO
    if (song >= MUS_YOKAI_BICYCLE && song <= MUS_YOKAI_TAKE_CARE)
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

/* One BGM sampled voice, never saved to flash. The original sequencer stops
 * channels for a fanfare; a TIE has no later note event to recreate that voice.
 * Keep its exact sample cursor/fraction and restore only into a free channel.
 */
#ifdef YOKAI_PRIVATE_AUDIO
static struct SoundChannel sPausedChannel;
static struct SongHeader *sPausedHeader;
static bool8 sPausedValid;
static bool8 sResumePending;

static bool8 IsPrivateSampleHeader(struct SongHeader *header)
{
    u32 i;
    for (i = 0; i < YOKAI_MUSIC_SLOT_COUNT; i++)
        if (gYokaiPrivateHeaders[i] != NULL && header == gYokaiPrivateHeaders[i])
            return TRUE;
    return FALSE;
}
#endif

void YokaiDiscardPausedSample(struct MusicPlayerInfo *player)
{
#ifdef YOKAI_PRIVATE_AUDIO
    if (player == &gMPlayInfo_BGM)
    {
        sPausedValid = FALSE;
        sResumePending = FALSE;
    }
#endif
}

void YokaiRememberPausedSample(struct MusicPlayerInfo *player)
{
#ifdef YOKAI_PRIVATE_AUDIO
    struct SoundChannel *channel;
    if (player != &gMPlayInfo_BGM)
        return;
    if (!IsPrivateSampleHeader(player->songHeader))
    {
        YokaiDiscardPausedSample(player);
        return;
    }
    channel = player->tracks[0].chan;
    if (channel != NULL && (channel->statusFlags & SOUND_CHANNEL_SF_ON))
    {
        sPausedChannel = *channel;
        sPausedHeader = player->songHeader;
        sPausedValid = TRUE;
        sResumePending = FALSE;
    }
#endif
}

void YokaiRetryPausedSample(void)
{
#ifdef YOKAI_PRIVATE_AUDIO
    struct SoundChannel *channel;
    struct MusicPlayerTrack *track;
    u32 i;
    if (!sPausedValid || !sResumePending)
        return;
    if (gMPlayInfo_BGM.songHeader != sPausedHeader)
    {
        YokaiDiscardPausedSample(&gMPlayInfo_BGM);
        return;
    }
    if (gMPlayInfo_BGM.status & MUSICPLAYER_STATUS_PAUSE)
        return;
    for (i = 0; i < gSoundInfo.maxChans; i++)
    {
        channel = &gSoundInfo.chans[i];
        if (channel->statusFlags & SOUND_CHANNEL_SF_ON)
            continue;
        track = &gMPlayInfo_BGM.tracks[0];
        *channel = sPausedChannel;
        channel->track = track;
        channel->prevChannelPointer = NULL;
        channel->nextChannelPointer = track->chan;
        if (track->chan != NULL)
            track->chan->prevChannelPointer = channel;
        track->chan = channel;
        channel->xpi = 0xFFFF;
        sPausedValid = FALSE;
        sResumePending = FALSE;
        return;
    }
    /* Never steal a sound effect; retry before a later mixer frame. */
#endif
}

void YokaiResumePausedSample(struct MusicPlayerInfo *player)
{
#ifdef YOKAI_PRIVATE_AUDIO
    if (player == &gMPlayInfo_BGM && sPausedValid && player->songHeader == sPausedHeader)
    {
        sResumePending = TRUE;
        YokaiRetryPausedSample();
    }
#endif
}
