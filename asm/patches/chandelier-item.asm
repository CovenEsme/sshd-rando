; Patch chandelier heart piece
.offset 0x08768694
ldrb w9, [x19, 0xD] ; load 00 00 FF 00 from param1 (the patched itemid)

; Don't patch rupees on chandelier
.offset 0x087686b8
mov w1, #0xfe00

; Replace call to dAcItem__spawnItemWithParams with dAcItem__spawnRandoItemWithParams
.offset 0x087686d4
bl dAcItem__spawnRandoItemWithParams


; Patch chandelier heart piece it another place xD
.offset 0x08768770
; mov w8, #0xbc00
ldrb w9, [x19, 0xD] ; load 00 00 FF 00 from param1 (the patched itemid)
; orr w1, w9, w8
; movk w1, #0xff9c, LSL #16

; Replace call to dAcItem__spawnItemWithParams with dAcItem__spawnRandoItemWithParams
.offset 0x08768794
bl dAcItem__spawnRandoItemWithParams


; Allow bonking down chandelier during Levias quest.
.offset 0x08767160
b 0x087671d0 ; branch over storyflag checks
