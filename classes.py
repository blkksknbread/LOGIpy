#  logiPY 3.0
import string


# Logic Gate class
class Gate:
    def __init__(self, x, y, name, function):
        self.input_1 = x
        self.input_2 = y
        self.name = name
        self.func = function
        # Two inputs and a logic function are defined in the constructor

    def run(self):
        # Running the gate outputs the given function of the given inputs
        return int(self.func(self.input_1.run(), self.input_2.run()))


# Input driver class
class Input:
    def __init__(self, preset, name):
        self.value = preset
        self.name = name
        # Sets the initial input value

    def invert(self):
        self.value = int (not self.value)

    def run(self):
        # returns input value
        return self.value


class Controller:
    def __init__(self, file_name):
        self.name = file_name
        self.gate_list = []
        self.input_list = []
        self.import_list = []
        self.output_list = []

        self.data = []
        self.parse_file()
        self.run()


    def parse_file(self):
        # opens a description file and creates the described instances
        infile = open(self.name, 'r')

        imports = infile.readline().split()
        if imports[0] != "import":
            inputs = imports[1:]
        else:
            imports = imports[1:]
            inputs = infile.readline().split()[1:]

        outputs = infile.readline().split()[1:]

        for inp in inputs:
            self.input_list.append(Input(0, inp.strip()))

        for line in infile:
            var_name = line.split("=")[0].strip()
            var_value = line.split("=")[1].split()
            input_1 = None
            input_2 = None

            for inp in self.input_list:
                if inp.name ==  var_value[0].strip():
                    input_1 = inp
                if inp.name ==  var_value[2].strip():
                    input_2 = inp

            for gate in self.gate_list:
                if gate.name == var_value[0] :
                    input_1 = gate
                if gate.name == var_value[2] :
                    input_2 = gate
            
            if input_1 == None:
                print "Undefined input: " + var_value[0]
                print "Process failed!"
                infile.close()
                return

            if input_2 == None:
                print "Undefined input: " + var_value[2]
                print "Process failed!"
                infile.close()
                return

            gate_function = self.gate(var_value[1])
            self.gate_list.append(Gate(input_1, input_2, var_name, gate_function))

        
        for output in outputs:
            found = False
            for gate in self.gate_list:
                if output == gate.name:
                    self.output_list.append(gate)
                    found = True
                    break
            if not found:
                print "Undefined output: " + output
                print "Process failed!"
                infile.close()
                return
        infile.close()   


    def run(self):
        row = 0
        while row < 2**len(self.input_list):
            row_data = []
            col = len(self.input_list) - 1
            for inp in self.input_list:
                row_data.append(inp.run())

            for output in self.output_list:
                row_data.append(int(output.run()))

            for inp in self.input_list:         #Cycling Inputs
                if (row + 1)%(2**col) == 0:
                    inp.invert()
                col -= 1        
            
            self.data.append(row_data)
            row += 1
    

    def out_console(self):
        
        full_data_string = ""
        top_row = ""
        for inp in self.input_list:
            top_row +=  inp.name + "\t"

        for out in self.output_list:
            top_row +=  out.name + "\t"
        
        print "\n\n" + top_row.rstrip() + "\n"
        full_data_string += top_row.rstrip() + "\n"
        
        for row in self.data:
            row_string = ""
            for bit in row:
                row_string +=  str(bit) + "\t"
            print row_string.rstrip()
            full_data_string += row_string.rstrip() + "\n"
        print ""
        return full_data_string
    

    def out_file(self, file_name):        
        outfile = open(file_name, "w")
        outfile.write(self.out_console())
        outfile.close()

    
    def gate(self, gate):

        if gate == "and":
            return and_f

        if gate == "or":
            return or_f

        if gate == "xor":
            return xor_f

        if gate == "nand":
            return nand_f

        if gate == "nor":
            return nor_f

        if gate == "xnor":
            return xnor_f
        

        
#  LOGIC FUNCTIONS
def and_f(x, y):
    return x and y

def or_f(x, y):
    return x or y

def xor_f(x, y):
    if x == y:
        return 0
    else:
        return 1


def nand_f(x, y):
    return not and_f(x, y)

def nor_f(x, y):
    return not or_f(x, y)

def xnor_f(x, y):
    return not xor_f(x, y)