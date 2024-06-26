import tkinter as tk
from tkinter import scrolledtext
def generate_minizinc_model(N, cities):
    model = f"""

    int: N = {N};  % variable que representa al Valle del cauca
    int: M = {len(cities)};  % variable que representa el número de ciudades

    set of int: N1 = 0..N;  % define un conjunto de n números que son las posiciones válidas de las X y Y
    set of int: Cities = 1..M;  % define un conjunto de M números que son los índices válidos de las ciudades

    array[Cities] of int: city_x = [{', '.join(str(city[1]) for city in cities)}];  % posiciones X de las ciudades
    array[Cities] of int: city_y = [{', '.join(str(city[2]) for city in cities)}];  % posiciones Y de las ciudades

    var N1: x;  % Coordenada X del concierto
    var N1: y;  % Coordenada Y del concierto

    % Calculo la distancia Manhattan desde el concierto a cada ciudad
    array[Cities] of var 0..2*N: dist;

    constraint
        forall(i in Cities) ( %para todas las cidades
            dist[i] = abs(x - city_x[i]) + abs(y - city_y[i]) %Calcula la distancia manhattan con la formula
        );
        
    constraint forall(c in Cities) (x != city_x[c] \/ y != city_y[c]); %Restricción de que el concierto no puede ser en ciudades

    % Variable para la máxima distancia Manhattan
    var 0..2*N: max_dist;

    %Se añade una restricción que establece que max_dist es igual a la mayor distancia en el arreglo dist.
    constraint
        max_dist = max(i in Cities)(dist[i]); 

    % Minimizar la máxima distancia Manhattan
    solve
        minimize max_dist;

    output ["Concierto de  Benito-G debe de ser en en la posición: (\(x), \(y)) para evitar decesos de alcaldes"];
    """
    
    return model

def process_input(input_text):
    lines = input_text.strip().split('\n')
    
    N = int(lines[0].strip())
    M = int(lines[1].strip())
    
    cities = []
    for i in range(2, 2 + M):
        parts = lines[i].strip().split()
        city_name = parts[0]
        city_x = int(parts[1])
        city_y = int(parts[2])
        cities.append((city_name, city_x, city_y))
    
    return N, cities

def main(input_text):
    N, cities = process_input(input_text)
    minizinc_model = generate_minizinc_model(N, cities)
    return minizinc_model

# Ejemplo de uso
# input_text = '''12
# 5
# Palmira 2 3
# Cali 10 2
# Buga 11 0
# Tulua 0 3
# Riofrio 1 2'''

# minizinc_code = main(input_text)
# print(minizinc_code)

def update_output():
    input_text = input_area.get("1.0", tk.END)
    minizinc_code = main(input_text)
    output_area.delete("1.0", tk.END)
    output_area.insert(tk.END, minizinc_code)

root = tk.Tk()
root.title("Proyecto Complejidad y Optimización")
root.geometry("1500x1200")
root.configure(bg='#333b3c')
input_label = tk.Label(root, text=" ¿Dónde pongo mi concierto?",  fg="white", bg="#333b3c", font=("JetBrains Mono", 30, "bold"))
input_label.place(x=420, y=20)
input_label = tk.Label(root, text="Entrada", fg="white", bg="#333b3c", font=("JetBrains Mono", 16, "bold"))
input_label.place(x=230, y=90)
input_label = tk.Label(root, text="Ejemplo: \n 12 \n 5 \n Palmira 2 3 \n Cali 10 2 \n Buga 11 0\n Tulua 0 3\n Riofrio 1 2", fg="white", bg="#333b3c", font=("JetBrains Mono", 8))
input_label.place(x=130, y=115)
input_area = scrolledtext.ScrolledText(root, width=30, height=10, bg="#CAF0F8", font=("JetBrains Mono", 12))
input_area.place(x=130, y=240)
output_label = tk.Label(root, text="Salida",  fg="white", bg="#333b3c", font=("JetBrains Mono", 16, "bold"))
output_label.place(x=960, y=90)
output_area = scrolledtext.ScrolledText(root, width=90, height=36, bg= "#CAF0F8", font=("JetBrains Mono", 10))
output_area.place(x=700, y=130)

button = tk.Button(root, text=" Generar MiniZinc", command=update_output, font=("JetBrains Mono", 10, "bold"), bg="white", fg="black", bd=5)
button.place(x=500, y=300)

root.mainloop()
