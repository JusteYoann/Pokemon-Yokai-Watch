#ifndef GUARD_YOKAI_MUSIC_H
#define GUARD_YOKAI_MUSIC_H
struct SongHeader;
struct SongHeader *YokaiGetSongHeader(u16 song, struct SongHeader *fallback);
u32 YokaiGetPrivateAudioMask(void);
#endif
