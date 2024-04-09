import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np

st.title("Cargar archivo JSON")

# Función para cargar el archivo JSON y devolver el mapa
def load_json_file():
    uploaded_file = st.file_uploader("Selecciona un archivo JSON", type="json")
    if uploaded_file is not None:
        data = json.load(uploaded_file)
        #st.write(data)
        return data.get("mapa", [])  # Devuelve el mapa si está presente en los datos
    else:
        return []  # Devuelve una lista vacía si no se ha cargado ningún archivo

# Función para procesar las adyacencias
def procesar_adyacencias(adyacencias):
    adyacencias_procesadas = []
    for adyacencia in adyacencias:
        if adyacencia == "dobleVia":
            adyacencias_procesadas.append((True, "dobleVia"))
        elif adyacencia == "entra":
            adyacencias_procesadas.append((True, "entra"))
        elif adyacencia == "sale":
            adyacencias_procesadas.append((True, "sale"))
        else:
            adyacencias_procesadas.append((False, None))
    return adyacencias_procesadas

# Función para crear la matriz del mapa
def crear_matriz(mapa):
    matriz = []
    for fila in mapa:
        fila_matriz = []
        for elemento in fila:
            transitable, semaforo, punto_interes, adyacencias = elemento
            adyacencias_procesadas = procesar_adyacencias(adyacencias)
            fila_matriz.append([transitable, semaforo, punto_interes, adyacencias_procesadas])
        matriz.append(fila_matriz)
    return matriz

# Función para visualizar la matriz como una ciudad
def visualizar_ciudad(matriz):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xticks(np.arange(len(matriz[0]) + 1))
    ax.set_yticks(np.arange(len(matriz) + 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)

    for i, fila in enumerate(matriz):
        for j, elemento in enumerate(fila):
            transitable, semaforo, punto_interes, adyacencias = elemento

            if transitable == 0:
                color_calle = "gray"  # Calle transitable (gris)
                color_entorno = "green"  # Entorno (verde)
            else:
                color_calle = "red"  # Calle no transitable (rojo)
                color_entorno = "red"  # Entorno (rojo)

            # Dibujar el entorno
            ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=True, edgecolor="black", facecolor=color_entorno))

            # Dibujar la calle y sus conexiones
            if transitable == 0:
                if adyacencias[0][0]:  # Arriba
                    ax.add_patch(plt.Rectangle((j + 0.2, i - 0.2), 0.6, 0.4, fill=True, edgecolor="black", facecolor=color_calle))
                    
                    if adyacencias[0][1] == "dobleVia":
                        ax.annotate("↕", xy=(j + 0.5, i - 0.1), ha="center", va="center", fontsize=22)
                    elif adyacencias[0][1] == "entra":
                        ax.annotate("↑", xy=(j + 0.5, i - 0.1), ha="center", va="center", fontsize=22)
                    elif adyacencias[0][1] == "sale":
                        ax.annotate("↓", xy=(j + 0.5, i - 0.1), ha="center", va="center", fontsize=22)
                    
                if adyacencias[1][0]:  # Abajo
                    ax.add_patch(plt.Rectangle((j + 0.2, i + 0.6), 0.6, 0.4, fill=True, edgecolor="black", facecolor=color_calle))

                    if adyacencias[1][1] == "dobleVia":
                        ax.annotate("↕", xy=(j + 0.5, i + 1.1), ha="center", va="center", fontsize=22)
                    elif adyacencias[1][1] == "entra":
                        ax.annotate("↓", xy=(j + 0.5, i + 1.1), ha="center", va="center", fontsize=22)
                    elif adyacencias[1][1] == "sale":
                        ax.annotate("↑", xy=(j + 0.5, i + 1.1), ha="center", va="center", fontsize=22)

                if adyacencias[2][0]:  # Izquierda
                    ax.add_patch(plt.Rectangle((j - 0.2, i + 0.2), 0.4, 0.6, fill=True, edgecolor="black", facecolor=color_calle))

                    if adyacencias[2][1] == "dobleVia":
                        ax.annotate("↔", xy=(j - 0.1, i + 0.5), ha="center", va="center", fontsize=22)
                    elif adyacencias[2][1] == "entra":
                        ax.annotate("→", xy=(j - 0.1, i + 0.5), ha="center", va="center", fontsize=22)
                    elif adyacencias[2][1] == "sale":
                        ax.annotate("←", xy=(j - 0.1, i + 0.5), ha="center", va="center", fontsize=22)
                    
                if adyacencias[3][0]:  # Derecha
                    ax.add_patch(plt.Rectangle((j + 0.6, i + 0.2), 0.4, 0.6, fill=True, edgecolor="black", facecolor=color_calle))

                    if adyacencias[3][1] == "dobleVia":
                        ax.annotate("↔", xy=(j + 1.1, i + 0.5), ha="center", va="center", fontsize=22)
                    elif adyacencias[3][1] == "entra":
                        ax.annotate("←", xy=(j + 1.1, i + 0.5), ha="center", va="center", fontsize=22)
                    elif adyacencias[3][1] == "sale":
                        ax.annotate("→", xy=(j + 1.1, i + 0.5), ha="center", va="center", fontsize=22)


                # Dibujar la calle central
                ax.add_patch(plt.Rectangle((j + 0.2, i + 0.2), 0.6, 0.6, fill=True, edgecolor="black", facecolor=color_calle))

    st.pyplot(fig)

# Mostrar el botón de carga de archivos y procesar el mapa
mapa = load_json_file()
if mapa:
    matriz = crear_matriz(mapa)
    visualizar_ciudad(matriz)
