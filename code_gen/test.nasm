    global   _main
    extern   _atoi
    extern   _printf
    default  rel

    section  .text
_main:
    
    push     rbx                    ; we don't ever use this, but it is necesary
                                    ; to align the stack so we can call stuff
    dec      rdi                    ; argc-1, since we don't count program name

text_msg    db     "Text",0
    lea     rdi, [text_msg]
    call    _printf
    pop     rbx
    ret
    section .bss
    section .data

msg:    db  "HelloMW",10,0