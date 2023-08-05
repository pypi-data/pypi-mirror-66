# Parse the ida trace file line

the ida trace file format is :

thread_id   module:address instruction  changed register   
`
00001CCF	base.apk:00000071D43894C4	STP             X28, X27, [SP,#-0x60]!	SP=00000071D66FAB70                     	
`

when parsed will return a object, the object has:
- thread_id
- module_name
- address
- offset
- op_code
    - mnemonic
    - operands
- changed register
    - register_name
    - value

if you want use the `offset` must set `trace_begin_offset` 




