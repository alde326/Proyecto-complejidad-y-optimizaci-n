def generate_minizinc_model(N, cities):
    model = f"""
    int: N = {N}; %variable que representa al valle del cauca
    int: M = {len(cities)};  %variable que representa el número de ciudades

    set of int: N1 = 1..N;  %define un conjunto de n numeros que son las posiciones validas de las X and Y
    set of int: Cities = 1..M;  %Define un conjunto de M números que son los indices válidos de las ciudades

    array[Cities] of int: city_x = [{', '.join(str(city[1]) for city in cities)}];  %posiciones X de las ciudades
    array[Cities] of int: city_y = [{', '.join(str(city[2]) for city in cities)}];  %Posiciones Y de las ciudades

    var 1..N: x;  %Coordenada x del concierto
    var 1..N: y;  %Coordenada Y del concierto

    % Calcular el punto medio de las ciudades
    var float: center_x = sum(c in Cities) (city_x[c]) / M;
    var float: center_y = sum(c in Cities) (city_y[c]) / M;

    % Definir la distancia al punto medio como la distancia a minimizar
    var float: min_distance = abs(x - center_x) + abs(y - center_y);

    % Restricciones
    constraint forall(c in Cities) (x != city_x[c] \/ y != city_y[c]);

    solve minimize min_distance;

    output ["x =", show(x), "y =", show(y)];
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
input_text = '''10
4
Union 0 0
Cali 10 0
Tulua 0 10
Palmira 10 10'''

minizinc_code = main(input_text)
print(minizinc_code)
