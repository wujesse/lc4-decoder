import sys
import re
# imem_out_regex = r"/(^.*?)imem_out: (\d+)$"
insn_regex = "(?:\[).*(?:\])"
arith_type = {"000": "ADD", "001": "MUL", "010": "SUB", "011": "DIV", "100": "ADDI", "110": "ADDI", "111": "ADDI", "101": "ADDI"}
log_type = {"000": "AND", "001": "NOT", "010": "OR", "011": "XOR", "100": "ANDI", "110": "ANDI", "111": "ANDI", "101": "ANDI"}
cmp_type = {"00": "CMP", "01": "CMPU", "10": "CMPI", "11": "CMPIU"}
shift_type = {"00": "SLL", "01": "SRA", "10": "SRL", "11": "MOD"}

def main():
    if (len(sys.argv) > 1):
        print("Decoding files...")
        for file_name in sys.argv[1:]:
            file = open(file_name, "r")
            decode_file = open("decoded-" + file_name, "w")
            line = file.readline()
            while (line):
                match = re.match(insn_regex, line).group(0)
                clean_insn = re.sub("[\[\]]", "", match)
                print(clean_insn)
                decode_file.write(decode(clean_insn) + "\n")
                line = file.readline()
            file.close()
            decode_file.close()
        print("Finished")
    else:
        print("Enter LC4 insn in binary")
        while (True):
            insn = input("\n>")
            if insn == "exit":
                break
            print(decode(insn))
    

def decode(insn):
    opcode = insn[0:4]
    r = insn[4:]

    if opcode == "0000":
        return "NOP" if (r == "000000000000") else f"BR {r[0:3]} {r[4:15]}\t\t\t{insn}"
    elif opcode == "0001":
        return f"{arith_type[r[6:9]]} Rd={int(r[0:3], 2)} Rs={int(r[3:6], 2)} Rt={int(r[9:], 2)}\t\t{insn}"
    elif opcode == "0010":
        rt = "Rt=" + str(int(r[9:], 2)) + "\t" if int(r[3:5], 2) < 2 else r[5:]
        return f"{cmp_type[r[3:5]]} Rs={int(r[0:3], 2)} {rt}\t\t{insn}"
    elif opcode == "0100":
        return f"{'JSRR' if r[0] == '0' else 'JSR'} {r[1:]}\t\t\t{insn}"
    elif opcode == "0101":
        if int(r[6:9], 2) == 1:
            return f"NOT Rd={int(r[0:3], 2)} Rs={int(r[3:6], 2)}\t\t\t{insn}"
        elif int(r[6:9], 2) > 3:
            return f"ANDI Rd={int(r[0:3], 2)} Rs={int(r[3:6], 2)} {r[7:]}\t\t{insn}"
        else:
            return f"{log_type[r[6:9]]} Rd={int(r[0:3], 2)} Rs={int(r[3:6], 2)} Rt={int(r[9:], 2)}\t\t{insn}"
    elif opcode == "0110":
        return f"LDR Rd={int(r[0:3], 2)} Rs={int(r[3:6], 2)} {r[6:]}\t\t{insn}"
    elif opcode == "0111":
        return f"STR Rt={int(r[0:3], 2)} Rs={int(r[3:6], 2)} {r[6:]}\t\t{insn}"
    elif opcode == "1000":
        return f"RTI\t\t{insn}"
    elif opcode == "1001":
        return f"CONST Rd={int(r[0:3], 2)} {r[3:]}\t\t{insn}"
    elif opcode == "1010":
        rt = "Rt=" + str(int(r[9:], 2)) if int(r[6:8], 2) == 3 else str(int(r[8:], 2))
        return f"{shift_type[r[6:8]]} Rd={int(r[0:3], 2)} Rs={int(r[3:6], 2)} {rt}\t\t{insn}"
    elif opcode == "1100":
        return f"JMP/JMPR {r[0:]}\t\t{insn}"
    elif opcode == "1101":
        return f"HICONST Rd={int(r[0:3], 2)} {r[4:]}\t\t{insn}"
    elif opcode == "1111":
        return f"TRAP {r[4:]}\t\t\t{insn}"
    else:
        return "err. Type 'exit' to stop."


if __name__ == '__main__':
    main()

