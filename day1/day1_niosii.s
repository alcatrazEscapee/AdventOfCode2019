# Nios II DE0 Assembly Source
# Runs on <https://cpulator.01xz.net/?sys=nios-de0>

    .text
	.global _start

_start:
	movi	r2, 0 # total fuel
	movia	r4, MODULES # module pointer
part1_loop:
	ldw		r5, 0(r4)
	beq		r5, r0, part1_end # end if zero
	# calculate the fuel for each module
	movi	r6, 3
	div		r5, r5, r6
	subi	r5, r5, 2
	# add to total
	add		r2, r2, r5
	addi	r4, r4, 4
	br		part1_loop

part1_end:
	mov		r10, r2 # save part 1 result in r10

	movi	r2, 0 # total fuel
	movia	r4, MODULES # module pointer
part2_loop_outer:
	ldw		r5, 0(r4)
	beq		r5, r0, part2_end
	mov		r3, r5
part2_loop_inner:
	movi	r6, 3 # calculate fuel
	div		r3, r3, r6
	subi	r3, r3, 2
	ble		r3, r0, part2_inner_end
	add		r2, r2, r3
	br		part2_loop_inner
part2_inner_end:
	addi	r4, r4, 4
	br		part2_loop_outer

part2_end:
	mov		r11, r2 # save part 2 result in r11
end:
	br		end

MODULES:
	.word	140517, 61738, 141916, 78376, 69208, 131761, 67212, 137805, 79089, 100457, 108707, 75235, 51118, 149457, 68888, 85722, 91418, 74481, 93441, 124911, 75441, 101542, 149092, 83149, 139256, 83398, 76398, 132252, 137763, 142758, 136279, 126238, 102888, 108723, 119982, 65216, 61412, 120894, 118761, 100221, 67132, 115494, 95623, 52819, 78612, 125505, 80523, 97774, 67569, 114514, 131671, 149811, 77679, 65540, 98415, 60595, 105589, 81927, 60249, 62514, 139506, 149532, 146885, 148831, 142896, 106300, 106313, 101456, 96521, 67104, 142037, 128258, 128769, 135081, 93181, 50735, 147720, 73775, 58113, 53478, 96705, 122060, 135329, 121513, 54539, 62404, 66334, 116924, 90977, 135383, 51479, 87581, 124040, 64048, 78616, 128068, 148184, 71714, 58847, 84640
	.word	0