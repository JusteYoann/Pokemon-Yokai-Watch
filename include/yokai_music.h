#ifndef GUARD_YOKAI_MUSIC_H
#define GUARD_YOKAI_MUSIC_H
#define YOKAI_MUSIC_SLOT_COUNT 26
struct SongHeader;
struct SongHeader *YokaiGetSongHeader(u16 song, struct SongHeader *fallback);
u32 YokaiGetPrivateAudioMask(void);
struct MusicPlayerInfo;
void YokaiRememberPausedSample(struct MusicPlayerInfo *player);
void YokaiResumePausedSample(struct MusicPlayerInfo *player);
void YokaiDiscardPausedSample(struct MusicPlayerInfo *player);
void YokaiRetryPausedSample(void);
void YokaiCalibrateSong(struct MusicPlayerInfo *player, struct SongHeader *header);
u32 YokaiScaleTrackVolume(struct MusicPlayerInfo *player, u32 volume);
#endif
