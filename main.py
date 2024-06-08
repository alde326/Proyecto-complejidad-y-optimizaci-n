def generate_minizinc_model(N, cities):
    model = f"""
    int: N = {N};
    int: M = {len(cities)};
    
    set of int: N1 = 1..N;
    set of int: Cities = 1..M;
    
    array[Cities] of int: city_x = [{', '.join(str(city[1]) for city in cities)}];
    array[Cities] of int: city_y = [{', '.join(str(city[2]) for city in cities)}];
    
    var 1..N: x;
    var 1..N: y;
    
    var int: min_distance = sum(c in Cities) (abs(x - city_x[c]) + abs(y - city_y[c]));
    
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
Union 1 1
Cali 1 3
Tulua 3 3
Palmira 3 1'''

minizinc_code = main(input_text)
print(minizinc_code)
