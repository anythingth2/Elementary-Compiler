    global _main
    extern _puts

    section .text

_main:
    mov     rax, 0x2000004 ; write
    mov     rdi, 1 ; stdout
    mov     rsi, msg
    mov     rdx, msg.len
    syscall

    push    rbx
    lea     rdi, [rel msg]
    call    _puts
    pop     rbx


    mov     rax, 0x2000001 ; exit
    mov     rdi, 0
    syscall




    section .data

msg:    db      "Hello, world!", 0
.len:   equ     $ - msg