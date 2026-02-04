import csv


def save_results(players, mst, total_cost):
    with open("resultado.csv", "w", newline="", encoding="utf8") as f:
        writer = csv.writer(f)

        writer.writerow(["Jugador", "Puntaje"])
        for player in players:
            writer.writerow([player.name, player.score])

        writer.writerow([])

        writer.writerow(["KRUSKAL - Arbol de Expansión Minima"])
        writer.writerow(["Nodo A", "Nodo B", "Peso"])
        for u, v, w in mst:
            writer.writerow([u, v, w])

        writer.writerow([])
        writer.writerow(["Costo total del recorrido", total_cost])
