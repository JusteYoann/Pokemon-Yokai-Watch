/* Hôte minimal pour le C émis par Clockwork (SIMULATION : programme synthétique, pas un jeu).
   Montre : (1) un crochet voit « mission finie » et « objet donné » ; (2) un programme extérieur
   peut donner un objet en appelant la fonction INTERNE du jeu (f_00100038) plutôt qu'en écrivant
   en mémoire. Les évènements sortent en lignes JSON (un vrai pont utiliserait un socket local). */
#include <stdio.h>
#include <stdlib.h>
#include "recomp.h"
#include "funcs.h"

uint8_t *recomp_mem;
void recomp_svc(Ctx *c, uint32_t imm, uint32_t a) { fprintf(stderr, "svc %x\n", imm); exit(2); }
void recomp_call_indirect(Ctx *c, uint32_t t) { fprintf(stderr, "indirect %x\n", t); exit(2); }
void recomp_unhandled(Ctx *c, uint32_t a, const char *w) { fprintf(stderr, "unhandled %s\n", w); exit(2); }
void recomp_coproc(Ctx *c, uint32_t a, uint32_t r) { exit(2); }

void ykap_hook(uint32_t addr, int phase, Ctx *ctx) {
    if (addr == 0x00100020u && phase == 1)
        printf("{\"event\":\"location_done\",\"mission\":%u,\"flags\":\"0x%08x\"}\n", ctx->r[0] & 0xFF, rd32(0x101000));
    if (addr == 0x00100038u && phase == 0)
        printf("{\"event\":\"item_given\",\"item\":%u}\n", ctx->r[0]);
}

int main(void) {
    recomp_mem = calloc(1, 0x200000);
    memcpy(recomp_mem + 0x100000, (uint8_t[]){0}, 0);
    FILE *f = fopen("extracted/code.bin", "rb"); fread(recomp_mem + 0x100000, 1, 0x2000, f); fclose(f);
    Ctx ctx = {0}; ctx.r[13] = 0x1F0000; ctx.r[14] = 0xFFFFFFF0;
    f_00100000(&ctx);                                   /* le « jeu » tourne */
    ctx.r[0] = 99; f_00100038(&ctx);                    /* objet AP reçu : fonction interne du jeu */
    printf("{\"state\":{\"flags\":\"0x%08x\",\"inventory_count\":%u,\"last_item\":%u}}\n",
           rd32(0x101000), rd32(0x101010), rd32(0x101014));
    return !(rd32(0x101000) == 0x80 && rd32(0x101010) == 3 && rd32(0x101014) == 99);
}
