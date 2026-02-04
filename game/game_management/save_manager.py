import csv

def save_results(players, mst, total_cost):
    with open("resultado.csv", "w", newline="", encoding="utf8") as f:
        writer = csv.writer(f)

        # Puntajes
        writer.writerow(["Jugador", "Puntaje"])
        for p in players:
            writer.writerow([p.name, p.score])

        writer.writerow([])

        # Kruskal
        writer.writerow(["KRUSKAL - Árbol de Expansión Mínima"])
        writer.writerow(["Nodo A", "Nodo B", "Peso"])
        for u, v, w in mst:
            writer.writerow([u, v, w])

        writer.writerow([])
        writer.writerow(["Costo total del recorrido", total_cost])
