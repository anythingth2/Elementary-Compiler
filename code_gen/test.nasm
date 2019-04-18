    global   _main
    extern   _atoi
    extern   _printf
    default  rel

    section  .text
_main:
    
    push     rbx                    ; we don't ever use this, but it is necesary
                                    ; to align the stack so we can call stuff
    dec      rdi                    ; argc-1, since we don't count program name

    push    rax                     ; caller-save register
        push    rcx                     ; caller-save register

        mov     rdi, format             ; set 1st parameter (format)
        mov     rsi, rax                ; set 2nd parameter (current_number)
        xor     rax, rax                ; because printf is varargs

        ; Stack is already aligned because we pushed three 8 byte registers
        call    printf                  ; printf(format, current_number)

        pop     rcx                     ; restore caller-save register
        pop     rax                     ; restore caller-save register

    pop     rbx
    ret
    section .bss
    section .data

msg:    db  "HelloMW",10,0