onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /T/CLK
add wave -noupdate /T/VGA_HS
add wave -noupdate /T/VGA_VS
add wave -noupdate -radix decimal /T/H_CNT
add wave -noupdate -radix decimal /T/V_CNT
add wave -noupdate /T/i
add wave -noupdate /T/j
add wave -noupdate -radix decimal /T/POINTS_GROUP
add wave -noupdate -radix decimal /T/POINTS_NUM
add wave -noupdate /T/BINARY_FLAG
add wave -noupdate -radix decimal /T/test
add wave -noupdate -radix decimal /T/POINTS_H_0
add wave -noupdate -radix decimal /T/POINTS_V_0
add wave -noupdate -radix decimal /T/POINTS_H_1
add wave -noupdate -radix decimal /T/POINTS_V_1
add wave -noupdate -radix decimal /T/POINTS_H_2
add wave -noupdate -radix decimal /T/POINTS_V_2
add wave -noupdate -radix decimal /T/POINTS_H_3
add wave -noupdate -radix decimal /T/POINTS_V_3
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {3574 ns} 0}
quietly wave cursor active 1
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {10250 ns} {11250 ns}
