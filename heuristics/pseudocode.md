### Greedy nearest neighbour
Losowany jest wierzchołek startowy dla pierwszego cyklu. Początkiem drugiego cyklu zostaje wierzchołem najbardziej oddalony od wcześniej wylosowanego wierzchołka. W liście free_vertices przechowujemy wierzchołki, które nie są częścią żadnej ścieżki. Dopóki lista ta nie jest pusta, na zmianę do każdej ścieżki dokładamy wolny wierzchołek, który powiększy długość ścieżki o najmniejszą wartość i usuwany go z listy free_vertices. Nowy wierzchołek może być dodany, na początku, na końcu lub w środku ścieżki (wtedy usuwamy połączenie między dwoma wierzchołkami i łączymy je dodając nowy wierzchołek pomiędzy nimi).
```
start_vertex_a = random vertex
start_vertex_b = vertex farthest from start_vertex_a
free_vertices = all vertices except start_vertex_a and start_vertex_b
path_a, path_b = [start_vertex_a], [start_vertex_b]
while free_vertices is not empty:
  for path in [path_a, path_b]:
    vertex_to_add, min_length = -1, inf
    for vertex in path:
      new_vertex, new_length  =  vertex and path length with shorter length after addition
      if new_length < min_length:
	      vertex_to_add, min_length = new_vertex, new_length
    remove vertex_to_add from free_vertices and add vertex_to_add to path
 ```

### Greedy cycles
Losowany jest wierzchołek startowy dla pierwszego cyklu. Początkiem drugiego cyklu zostaje wierzchołem najbardziej oddalony od wcześniej wylosowanego wierzchołka. Zostają stworzone dwa cykle poprzez dodanie do każdego wierzchołka startowego wierzchołka, który jest najbliżej, każdego z wierzchołków startowych. W liście free_vertices przechowujemy wierzchołki, które nie są częścią żadnego cyklu. Dopóki lista ta nie jest pusta, na zmianę do każdego cyklu dokładamy wolny wierzchołek, który powiększy długość cyklu o najmniejszą wartość i usuwany go z listy free_vertices. Przed dodaniem nowego wierzchołka do cyklu sprawdzamy wszystkie możliwe miejsca gdzie można go dodać. Przy badaniu dodania wierzchołka pomiędzy dwa wierzchołki, nie jest liczona długość całego cyklu, a jedynie długość pomiędzy nowym wierzchołkiem a dwoma wierzchołkami z cyklu.

```
start_vertex_a = random vertex
start_vertex_b = vertex farthest from start_vertex_a
close_vertex_a, Close_vertex_b = vertices which are closest to start_vertex_a and start_vertex_b respectively
cycle_a, cycle_b = [start_vertex_a, close_vertex_a, start_vertex_a], [start_vertex_b, close_vertex_b, start_vertex_b]
free_vertices = all vertices except start_vertex_a, start_vertex_b, close_vertex_a, and close_vertex_b
while free_vertices is not empty:
  for cycle in [cycle_a, cycle_b]:
    vertex_to_add, min_length = -1, inf
    for pair of vertices in cycle:
      new_vertex, new_length  =  vertex and cycle length with shorter length after addition of vertex between pair of vertices
      if new_length < min_length:
	      vertex_to_add, min_length = new_vertex, new_length
    remove vertex_to_add from free_vertices and add vertex_to_add to cycle
```
