global  main
        extern  puts
        section .text
main:
        sub     rsp, 20h                        ; Reserve the shadow space
        mov     rcx, message                    ; First argument is address of message
        call    puts                            ; puts(message)
        add     rsp, 20h                        ; Remove shadow space
        ret
message:
        db      'Hello', 0                   