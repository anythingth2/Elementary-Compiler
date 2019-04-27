    global   main
    extern   atoi
    extern   printf
    default  rel

    section  .text
main:
    
    push     rbx                    ; we don't ever use this, but it is necesary
                                    ; to align the stack so we can call stuff
    dec      rdi                    ; argc-1, since we don't count program name

    push    rax                     ; caller-save register
        push    rcx                     ; caller-save register

        mov     rdi, msg             ; set 1st parameter (format)

        push    rax
        push    rcx
        push    rdx


        mov     rax,[x]

        add     rax,3

        sub     rax,2

        imul    rax,-132



        ; and     rdx,0x8000000000000000
        cqo
        mov     rcx,111
        idiv    rcx
        ; mov     rax, rdx


        ; xor     rdx,rdx
        ; mov     rcx,19
        ; idiv    rcx

        ; mov     rax, rdx
        
        
        mov     [x],rax

        pop     rdx
        pop     rcx
        pop     rax


        mov     rsi, [x]                ; set 2nd parameter (current_number)
        xor     rax, rax                ; because printf is varargs

        ; Stack is already aligned because we pushed three 8 byte registers
        call    printf                  ; printf(format, current_number)

        pop     rcx                     ; restore caller-save register
        pop     rax                     ; restore caller-save register

    pop     rbx
    ; ret
    section .bss
    section .data

msg:    db  "%d",10,0
x:      db  10