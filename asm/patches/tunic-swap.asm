; Change the comparison when loading
; Link's tunic textures from b.eq to b.ne

; onlyif tunic_swap == on
.offset 0x7100ab5930
b.ne 0x7100ab7b58
