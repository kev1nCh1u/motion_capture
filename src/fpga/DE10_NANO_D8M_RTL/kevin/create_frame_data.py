f = open("src/fpga/DE10_NANO_D8M_RTL/kevin/BINARY_FRAME_DATA.txt", "w")

for i in range(100): # y
    for j in range(200): # x
        f.write("0 ")
    f.write("\n")

f.close()