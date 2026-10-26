; 65C816 native-mode DMA0 replacement, assembled by build_routine_prototype.py.
; Entry via JSL $64:8000 with the same A/P as the replaced STA $420B.
; Exact bytes and labels are recorded in routine_handler.bin/routine_port.json.
; Full-key variant: channel 0 at $64:8000, channel 1 at $64:8100.
; Channel 1 changes $430x operands to $431x.
org $648000
entry:
 php
 rep #$30
 pha
 phx
 phb
 sep #$20
 lda #$00
 pha
 plb
 lda $4300
 and #$08
 beq passthrough
 lda $4304
 cmp #$c0
 bcc passthrough
 pha
 rep #$20
 lda $4302
 pha
 sep #$20
 lda $4300
 pha
 ldx $4302
 lda $04,s
lookup:
 cmp.l $600000,x
 beq bank_match
 pha
 lda.l $600000,x
 beq missing
 pla
 inx
 bra lookup
bank_match:
 pha
 lda.l $650000,x
 cmp $03,s
 bne key_mismatch
 lda.l $660000,x
 cmp $04,s
 bne key_mismatch
 pla
 bra found
key_mismatch:
 pla
 inx
 bra lookup
found:
 lda.l $610000,x
 sta $4302
 lda.l $620000,x
 sta $4303
 lda.l $630000,x
 sta $4304
 lda $4300
 and #$f7
 sta $4300
 lda $08,s
 sta $420b
 pla
 sta $4300
 rep #$20
 pla
 sta $4302
 sep #$20
 pla
 sta $4304
 bra done
passthrough:
 lda $04,s
 sta $420b
done:
 plb
 rep #$30
 plx
 pla
 plp
 rtl
missing:
 pla
trap:
 bra trap
