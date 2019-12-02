# Nios II DE0 Assembly Source
# Runs on <https://cpulator.01xz.net/?sys=nios-de0>

	.text
	.global _start

_start:
	movia	sp, 0x7FFFFC

	# Part 1 - copy input into memory, then run and query result
	movia	r3, INPUT
	call	copy

	movi	r3, 12
	movi	r4, 2
	call 	run

	movia	r2, RUN_MEMORY
	ldw		r10, 0(r2) # the result is the value of the first register

	# Part 2 - move the resuired result into r3, then call find
	movia	r3, 19690720
	call	find

	mov		r11, r2

_end:
	br		_end


# copies an intocde program from a pointer in r3 into RUN_MEMORY
copy:
	subi	sp, sp, 12
	stw		r2, 0(sp)
	stw		r3, 4(sp)
	stw		r4, 8(sp)

	movia	r4, RUN_MEMORY

copy__loop:
	ldw		r2, 0(r3)
	stw		r2, 0(r4)
	addi	r4, r4, 4
	addi	r3, r3, 4
	bge		r2, r0, copy__loop # exit condition is the last word, which is negative

	ldw		r2, 0(sp)
	ldw		r3, 4(sp)
	ldw		r4, 8(sp)
	addi	sp, sp, 12
	ret


# runs an intcode program loaded into RUN_MEMORY
# takes arguments of the noun and verb in r3 and r4
run:
	subi	sp, sp, 24
	stw		r2, 0(sp)
	stw		r3, 4(sp)
	stw		r4, 8(sp)
	stw		r5, 12(sp)
	stw		r6, 16(sp)
	stw		r7, 20(sp)

	movia	r5, RUN_MEMORY # run pointer (will be modified)
	mov		r7, r5 # base offset

	stw		r3, 4(r5) # copy noun and verb into positions 1 and 2
	stw		r4, 8(r5)

run__loop:
	ldw		r2, 0(r5) # opcode

	movi	r6, 99
	beq		r2, r6, run__ret # 99 = exit

	ldw		r3, 4(r5)
	muli	r3, r3, 4
	add		r3, r3, r7
	ldw		r3, 0(r3) # load value in first arg
	ldw		r4, 8(r5)
	muli	r4, r4, 4
	add		r4, r4, r7
	ldw		r4, 0(r4) # load value in second arg

	movi	r6, 1
	beq		r2, r6, run__add # 1 = add

	mul		r2, r3, r4 # 2 = multiply
	br		run__finish

run__add:
	add		r2, r3, r4

run__finish:
	ldw		r3, 12(r5)
	muli	r3, r3, 4
	add		r3, r3, r7
	stw		r2, 0(r3) # store result in the third arg pointer position

	addi	r5, r5, 16 # advance pointer by 4
	br		run__loop

run__ret:
	ldw		r2, 0(sp)
	ldw		r3, 4(sp)
	ldw		r4, 8(sp)
	ldw		r5, 12(sp)
	ldw		r6, 16(sp)
	ldw		r7, 20(sp)
	addi	sp, sp, 24
	ret


# finds a program with a given position 0 result, passed in r3
# iterates through a noun and verb within [0, 100] each
# returns 100 * noun + verb in r2
find:
	subi	sp, sp, 20
	stw		ra, 0(sp)
	stw		r3, 4(sp)
	stw		r4, 8(sp)
	stw		r5, 12(sp)
	stw		r6, 16(sp)

	mov		r2, r3 # move the expected result to r2
	movi	r5, 100 # counters for noun and verb
	movi	r6, 100

find__loop:
	movia	r3, INPUT # copy input
	call	copy

	mov		r3, r5 # move noun and verb
	mov		r4, r6
	call 	run # run program

	movia	r3, RUN_MEMORY
	ldw		r3, 0(r3) # fetch the result

	beq		r2, r3, find__ret

	subi	r5, r5, 1 # decrement noun
	bge		r5, r0, find__loop

	movi	r5, 100 # restart noun at 100, decrement verb
	subi	r6, r6, 1
	br		find__loop

find__ret:
	mov		r2, r5
	muli	r2, r2, 100
	add		r2, r2, r6

	ldw		ra, 0(sp)
	ldw		r3, 4(sp)
	ldw		r4, 8(sp)
	ldw		r5, 12(sp)
	ldw		r6, 16(sp)
	addi	sp, sp, 20
	ret


INPUT:
	.word 	1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,13,19,1,9,19,23,2,13,23,27,2,27,13,31,2,31,10,35,1,6,35,39,1,5,39,43,1,10,43,47,1,5,47,51,1,13,51,55,2,55,9,59,1,6,59,63,1,13,63,67,1,6,67,71,1,71,10,75,2,13,75,79,1,5,79,83,2,83,6,87,1,6,87,91,1,91,13,95,1,95,13,99,2,99,13,103,1,103,5,107,2,107,10,111,1,5,111,115,1,2,115,119,1,119,6,0,99,2,0,14,0
	.word 	-1

RUN_MEMORY:
	.skip 	512
	.word	-1
