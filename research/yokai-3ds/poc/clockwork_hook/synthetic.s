@ Programme ARM SYNTHÉTIQUE (aucune donnée de jeu) : imite « mission finie » puis « objet donné ».
    .syntax unified
    .arm
    .text
_start:
    push {r4, lr}
    mov r0, #7              @ n° de mission
    bl complete_mission
    mov r0, #42             @ n° d'objet
    bl give_item
    mov r0, #43
    bl give_item
    pop {r4, pc}
complete_mission:           @ FLAGS |= 1 << r0
    ldr r1, =0x00101000
    ldr r2, [r1]
    mov r3, #1
    orr r2, r2, r3, lsl r0
    str r2, [r1]
    bx lr
give_item:                  @ INV.count++, INV.last = r0
    ldr r1, =0x00101010
    ldr r2, [r1]
    add r2, r2, #1
    str r2, [r1]
    str r0, [r1, #4]
    bx lr
    .ltorg
