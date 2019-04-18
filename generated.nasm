	default	rel
	global	_main
	extern	_printf

	section	.text
_main:
	push	rbx
	dec	rdi


    push    rax
    push    rcx
    lea     rdi, [chichachai]
    mov     rax, 1
    call    _printf
    pop     rcx
    pop     rax

        	pop	rbx
	ret

	section	.data

chichachEYASDADai:	db	"YEf", 10,"sfsAG", 10,"" ,0
chichachai:	db	"YEA", 10,"G" ,0
	section	.bss
