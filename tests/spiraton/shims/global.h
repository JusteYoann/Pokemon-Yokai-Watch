#ifndef SPIRATON_HOST_GLOBAL_H
#define SPIRATON_HOST_GLOBAL_H
#include <stddef.h>
#include <stdint.h>
typedef uint8_t u8; typedef int8_t s8; typedef uint16_t u16;
typedef uint32_t u32; typedef uint8_t bool8;
#define TRUE 1
#define FALSE 0
#define ARRAY_COUNT(a) (sizeof(a) / sizeof((a)[0]))
#endif
