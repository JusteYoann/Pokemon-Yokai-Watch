#include "global.h"
#include "m4a.h"
#include "constants/songs.h"
#include "yokai_music.h"

#ifdef YOKAI_PRIVATE_AUDIO
extern struct SongHeader *const gYokaiPrivateHeaders[YOKAI_MUSIC_SLOT_COUNT];
extern const u32 gYokaiPrivateAudioMask;
extern const u32 gYokaiPrivateSlotCount;
#endif

#include "data/yokai_music_aliases.h"

struct SongHeader *YokaiGetSongHeader(u16 song, struct SongHeader *fallback)
{
    u32 i;
    /* Resolve legacy script/engine BGM calls as well as map headers. Dedicated
     * character IDs are preserved; fanfares, cries and SE IDs are never aliased.
     * Public builds use the dedicated theme's native fallback, not private data.
     */
    for (i = 0; i < NELEMS(sYokaiMusicAliases); i++)
        if (sYokaiMusicAliases[i][0] == song)
        {
            song = sYokaiMusicAliases[i][1];
            fallback = gSongTable[song].header;
            break;
        }
#ifdef YOKAI_PRIVATE_AUDIO
    if (song >= MUS_YOKAI_BICYCLE && song <= MUS_YOKAI_LAST)
    {
        u32 slot = song - MUS_YOKAI_BICYCLE;
        if (slot < gYokaiPrivateSlotCount && gYokaiPrivateHeaders[slot] != NULL)
            return gYokaiPrivateHeaders[slot];
        /* A declared but unavailable sample must not silently reintroduce
         * FireRed BGM into the private soundtrack. Reuse an explicit active
         * cue until its own full arrangement is ready. Public fallback stays
         * unchanged. No recursion and no extra copied sample or RAM state.
         */
        for (i = 0; i < NELEMS(sYokaiUnavailableMusicFallbacks); i++)
            if (sYokaiUnavailableMusicFallbacks[i][0] == song)
            {
                slot = sYokaiUnavailableMusicFallbacks[i][1] - MUS_YOKAI_BICYCLE;
                if (slot < gYokaiPrivateSlotCount && gYokaiPrivateHeaders[slot] != NULL)
                    return gYokaiPrivateHeaders[slot];
                break;
            }
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


/* Calibrate at song start, then one cached integer multiply per volume update.
 * The fader, help reduction and cry ducking remain relative to this gain.
 * No changes to track sequence data or private sampled waveform bytes.
 */
#include "data/yokai_mixer_gains.h"
static EWRAM_DATA u16 sMixGain[4] = {256, 256, 256, 256};

static s32 MixerPlayerIndex(struct MusicPlayerInfo *player)
{
    if (player == &gMPlayInfo_BGM) return 0;
    if (player == &gMPlayInfo_SE1) return 1;
    if (player == &gMPlayInfo_SE2) return 2;
    if (player == &gMPlayInfo_SE3) return 3;
    return -1;
}

void YokaiCalibrateSong(struct MusicPlayerInfo *player, struct SongHeader *header)
{
    s32 index = MixerPlayerIndex(player);
    u32 n;
    if (index < 0) return;
    sMixGain[index] = 256;
#ifdef YOKAI_PRIVATE_AUDIO
    for (n = 0; n < gYokaiPrivateSlotCount && n < YOKAI_MUSIC_SLOT_COUNT; n++)
        if (gYokaiPrivateHeaders[n] != NULL && gYokaiPrivateHeaders[n] == header)
        {
            sMixGain[index] = sYokaiSongGain[MUS_YOKAI_BICYCLE + n];
            return;
        }
#endif
    for (n = 0; n <= MUS_YOKAI_LAST; n++)
        if (gSongTable[n].header == header)
        {
            sMixGain[index] = sYokaiSongGain[n];
            return;
        }
}

u32 YokaiScaleTrackVolume(struct MusicPlayerInfo *player, u32 volume)
{
    s32 index = MixerPlayerIndex(player);
    if (index >= 0)
        volume = (volume * sMixGain[index] + 128) >> 8;
    /* volML/volMR are bytes: prohibit wrap-around at boosted private levels. */
    if (volume > 510) volume = 510;
    return volume;
}
