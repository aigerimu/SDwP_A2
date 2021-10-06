import sys
import os, timeit
import subprocess
import dis, marshal, py_compile
from tempfile import NamedTemporaryFile


# Task 1
def task1():
    with open("task1.txt", "a") as f:
        result = dict()
        for i in sys.argv[1:]:
            if os.path.exists(i):
                timer = timeit.timeit(lambda: subprocess.run(['python3', i], stdout=subprocess.PIPE), number=1)
                result[i] = timer
        ranking_list = sorted(result.items(), key=lambda item: item[1])
        f.write('PROGRAM | RANK | TIME ELAPSED')

        count = 0
        for i in ranking_list:
            count += 1
            f.write(f'\n{i[0]}\t {count} \t  {i[1]}')

task1()

def get_bytecode(arg):
    return dis.Bytecode(arg)


def expand_bytecode(bytecode):
    result = []
    for instruction in bytecode:
        if str(type(instruction.argval)) == "<class 'code'>":
            result += expand_bytecode(dis.Bytecode(instruction.argval))
        else:
            result.append(instruction)
    return result


# Task 2&3

def bc_printer():
    with open("task2&3.txt", "a") as f1:
        for i in sys.argv[2:]:
            source = None
            if sys.argv[1] == "-py":
                with open(i, 'r') as f:
                    source = f.read()
            elif sys.argv[1] == "-pyc":
                header_size = 12
                if sys.version_info >= (3, 7):
                    header_size = 16
                with open(i, 'rb') as f:
                    f.seek(header_size)
                    source = marshal.load(f)
            elif sys.argv[1] == "-s":
                source = i
            else:
                print("Error")
                return

            bc = get_bytecode(source)
            res = expand_bytecode(bc)
            for instruction in res:
                print(f'{instruction.opname}\t {instruction.argrepr}', file=f1)


bc_printer()


# Task 4
def compile():
    for i in sys.argv[3:]:
        if sys.argv[2] == "-s":
            with NamedTemporaryFile("w", delete=False) as tmp:
                tmp.write(i)
                tmp.seek(0)
                py_compile.compile(tmp.name, cfile="out.pyc")
        elif sys.argv[2] == "-py":
            try:
                py_compile.compile(i, cfile=i+"c")
            except Exception as e:
                print(f"We`re skipping...{i}")

    if len(sys.argv) == 1:
        print('usage: bc.py action [-flag value]*\nThis program\ncompile\n\t-py file.py compile file into bytecode and '
              'store it as file.pyc\n\t-s "src" compile src into bytecode and store it as out.pyc\nprint\n\t-py src.py '
              'produce human-readable bytecode from python \n\t-pyc src.pyc produce human-readable bytecode from '
              'compiled .pyc file\n\t-s "src" produce human-readable bytecode from normal string')


compile()

# Task 5
def compare():

    comb_opn = set()
    dictt = {}
    dict_list = []
    file_names = sys.argv[3::2]

    for i in sys.argv[3::2]:

        if len(i) > 13:
            continue
        if sys.argv[sys.argv.index(i) - 1] == "-py":
            with open(i, 'r') as f:
                source = f.read()
        elif sys.argv[sys.argv.index(i) - 1] == "-s":
            source = i
        elif sys.argv[sys.argv.index(i) - 1] == "-pyc":
            header_size = 12
            if sys.version_info >= (3, 7):
                header_size = 16
            with open(i, 'rb') as f:
                f.seek(header_size)
                source = marshal.load(f)
        else:
            print("Error")
            return

        bc = get_bytecode(source)
        res = expand_bytecode(bc)
        opnames = list(map(lambda instr: instr.opname, res))
        comb_opn.update(opnames)
        instr_dict = {i: opnames.count(i) for i in opnames}

        def keys_val(list1):
            count = {}
            for i in list1:
                count[i] = count.get(i, 0) + 1
            return count

        dictt = keys_val(opnames)

        dict_list.append(dictt)
        print(dict_list)

    with open("task5.txt", "a") as f:

        print('INSTRUCTION          ', end='', file=f)
        for i in file_names:
            print('|  ' + i + (12-len(i))*' ', end='', file=f)
        print(file=f)

        for i in comb_opn:
            print(i + (22-len(i))*' ', end='', file=f)
            for k in dict_list:
                value = 0
                try:
                    value = k[i]
                except:
                    value = 0
                print('   ' + str(value) + (12-len(str(value)))*' ', end='', file=f)
            print(file=f)

        print(file=f)
        print(file=f)

       # dict1 = {i: values.index() for i in comb_opn}
       # print(dict1)

        #peaks = sorted(instr_dict.items(), key=operator.itemgetter(1), reverse=True)
#        print(peaks)


compare()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('usage: bc.py action [-flag value]*\nThis program\ncompile\n\t-py file.py compile file into bytecode and '
              'store it as file.pyc\n\t-s "src" compile src into bytecode and store it as out.pyc\nprint\n\t-py src.py '
              'produce human-readable bytecode from python \n\t-pyc src.pyc produce human-readable bytecode from '
              'compiled .pyc file\n\t-s "src" produce human-readable bytecode from normal string')
    else:
        if sys.argv[1] == "print":
            bc_printer()
        elif sys.argv[1] == "compile":
            compile()
        elif sys.argv[1] == "compare":
            pass
        else:
            print("Error")

