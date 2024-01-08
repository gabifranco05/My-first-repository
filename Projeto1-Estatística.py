import matplotlib.pyplot as plt

def read_txt_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', '')  
            return data.strip()  
    except FileNotFoundError:
        return "File not found."
    
def divide_string(input_string, substring_length):
    return [input_string[i:i+substring_length] for i in range(0, len(input_string), substring_length)]

teste = read_txt_file('seq1.txt')

integer_list = []
sub_strings = divide_string(teste, 6)

for string in sub_strings:
    integer = int(string[0])*(2**5) + int(string[1])*(2**4) + int(string[2])*(2**3) + int(string[3])*(2**2) + int(string[4])*(2) + int(string[5])
    integer_list.append(integer)

def plot_histogram(int_list):
    plt.hist(int_list, bins=max(int_list)-min(int_list)+1, align='left', edgecolor='black')
    plt.xlabel('Integers')
    plt.ylabel('Frequency')
    plt.title('Histogram of Integers')
    plt.grid(True)
    plt.show()

plot_histogram(integer_list)  

#Conseguimos ver que o histograma produzido está longe de representar uma distribuição normal, tanto que muitos inteiros nem chegam a aparecer
#uma única vez e, dos que têm frequência maior ou igual a 1, a sua distruibuição é bastante desuniforme.
#Concluímos que através deste teste é evidente verificar um enviesamento nos bits
