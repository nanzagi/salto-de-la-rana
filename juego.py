import tkinter as tk
import os
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  # Necesario para usar imágenes en los botones
import json
import subprocess
import uuid  # Para generar identificadores únicos para cada sesión

def export_moves_to_github():
    """Exporta los movimientos a un archivo y lo sube a GitHub automáticamente."""
    # Generar un identificador único para la sesión
    session_id = str(uuid.uuid4())

    # Leer el archivo JSON existente (si existe)
    try:
        with open("move_log.json", "r") as file:
            all_sessions = json.load(file)
    except FileNotFoundError:
        # Si el archivo no existe, inicializar una lista vacía
        all_sessions = []

    # Agregar los movimientos de la sesión actual
    session_data = {
        "session_id": session_id,
        "movements": move_log
    }
    all_sessions.append(session_data)

    # Guardar los movimientos actualizados en el archivo JSON
    with open("move_log.json", "w") as file:
        json.dump(all_sessions, file, indent=4)

    # Subir el archivo a GitHub
    try:
        subprocess.run(["git", "add", "move_log.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Registro de movimientos del juego"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Movimientos exportados y subidos a GitHub correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al subir a GitHub: {e}")
# Cambiar al directorio donde están las imágenes
base_path = os.path.dirname(os.path.abspath(__file__))

# Construir rutas relativas para las imágenes
green_frog_path = os.path.join(base_path, "green_frog.png")
red_frog_path = os.path.join(base_path, "red_frog.png")
# Lista para registrar los movimientos
move_log = []

def is_valid_move(board, pos, direction):
    """Verifica si un movimiento es válido."""
    n = len(board)
    target = pos + direction

    # Verificar si el movimiento está dentro del rango del tablero
    if target < 0 or target >= n:
        return False

    # Movimiento simple a una casilla vacía
    if board[target] == "_":
        return True

    # Movimiento de salto sobre una rana del equipo contrario
    jump_target = pos + 2 * direction
    if (
        0 <= jump_target < n
        and board[target] != "_"
        and board[target] != board[pos]
        and board[jump_target] == "_"
    ):
        return True

    return False

def make_move(board, pos, direction):
    """Realiza un movimiento en el tablero."""
    target = pos + direction

    # Movimiento simple
    if board[target] == "_":
        board[target], board[pos] = board[pos], "_"
        move_log.append({"from": pos, "to": target, "type": "simple"})
    else:
        # Movimiento de salto
        jump_target = pos + 2 * direction
        board[jump_target], board[pos] = board[pos], "_"
        move_log.append({"from": pos, "to": jump_target, "type": "jump"})

def is_game_won(board, n):
    """Verifica si el juego ha terminado."""
    mid = (n - 1) // 2
    left_side = board[:mid]
    right_side = board[mid + 1 :]

    # Verificar si el equipo 'r' está completamente en el lado izquierdo
    if all(cell == "r" for cell in left_side) and all(cell == "v" for cell in right_side):
        return True

    return False

def export_moves_to_github():
    """Exporta los movimientos a un archivo y lo sube a GitHub automáticamente."""
    # Generar un identificador único para la sesión
    session_id = str(uuid.uuid4())

    # Leer el archivo JSON existente (si existe)
    try:
        with open("move_log.json", "r") as file:
            all_sessions = json.load(file)
    except FileNotFoundError:
        # Si el archivo no existe, inicializar una lista vacía
        all_sessions = []

    # Agregar los movimientos de la sesión actual
    session_data = {
        "session_id": session_id,
        "movements": move_log
    }
    all_sessions.append(session_data)

    # Guardar los movimientos actualizados en el archivo JSON
    with open("move_log.json", "w") as file:
        json.dump(all_sessions, file, indent=4)

    # Subir el archivo a GitHub
    try:
        subprocess.run(["git", "add", "move_log.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Registro de movimientos del juego"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Movimientos exportados y subidos a GitHub correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al subir a GitHub: {e}")

def play_game_gui():
    """Función principal para jugar el juego con interfaz gráfica."""
    # Crear ventana principal
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal temporalmente

    # Solicitar el número de casillas
    n = simpledialog.askinteger("Configuración", "Introduce el número de casillas (impar mayor a 3):")
    if n is None or n <= 2 or n % 2 == 0:
        messagebox.showerror("Error", "El número de casillas debe ser un impar mayor a 3.")
        return

    # Inicializar el tablero
    mid = (n - 1) // 2
    board = ["v"] * mid + ["_"] + ["r"] * mid

    # Crear ventana principal para el juego
    root.deiconify()
    root.title("Salto de la Rana")

    # Crear un contador de movimientos
    move_count = tk.IntVar(value=0)

    # Etiqueta para mostrar el conteo de movimientos
    move_label = tk.Label(root, text=f"Movimientos: {move_count.get()}", font=("Arial", 14))
    move_label.grid(row=1, column=0, columnspan=n)

    # Cargar imágenes para las ranas
    green_frog_image = ImageTk.PhotoImage(Image.open("green_frog.png").resize((50, 50)))
    red_frog_image = ImageTk.PhotoImage(Image.open("red_frog.png").resize((50, 50)))

    # Crear botones para representar el tablero
    buttons = []
    for i in range(n):
        if board[i] == "v":
            button = tk.Button(root, image=green_frog_image, width=50, height=50)
        elif board[i] == "r":
            button = tk.Button(root, image=red_frog_image, width=50, height=50)
        else:
            button = tk.Button(root, text=board[i], font=("Arial", 20), width=4, height=2)
        button.grid(row=0, column=i)
        buttons.append(button)

    # Variable para almacenar la posición seleccionada
    selected_pos = tk.IntVar(value=-1)

    def on_button_click(pos):
        """Selecciona una rana para mover."""
        player = board[pos]
        if player not in ["v", "r"]:
            messagebox.showwarning("Movimiento inválido", "Esa no es una rana.")
            return

        # Guardar la posición seleccionada
        selected_pos.set(pos)

    def on_key_press(event):
        """Maneja el movimiento de la rana seleccionada con las teclas A y D."""
        pos = selected_pos.get()
        if pos == -1:
            return  # No hay rana seleccionada

        direction = 0
        if event.keysym.lower() == "d":  # Mover a la derecha
            direction = 1
        elif event.keysym.lower() == "a":  # Mover a la izquierda
            direction = -1
        else:
            return  # Tecla no válida

        if not is_valid_move(board, pos, direction):
            messagebox.showwarning("Movimiento inválido", "Movimiento no permitido.")
            return

        # Realizar el movimiento
        make_move(board, pos, direction)
        for i, button in enumerate(buttons):
            if board[i] == "v":
                button.config(image=green_frog_image, text="", width=50, height=50)
            elif board[i] == "r":
                button.config(image=red_frog_image, text="", width=50, height=50)
            else:
                button.config(image="", text=board[i], width=4, height=2)

        # Incrementar el contador de movimientos
        move_count.set(move_count.get() + 1)
        move_label.config(text=f"Movimientos: {move_count.get()}")

        # Verificar si el juego ha terminado
        if is_game_won(board, n):
            messagebox.showinfo("¡Juego terminado!", f"¡El juego ha terminado en {move_count.get()} movimientos!")
            export_moves_to_github()  # Exportar los movimientos al finalizar el juego
            root.destroy()
            return

        # Limpiar la posición seleccionada
        selected_pos.set(-1)

    # Asignar eventos a los botones
    for i, button in enumerate(buttons):
        button.config(command=lambda i=i: on_button_click(i))

    # Asignar eventos de teclado
    root.bind("<KeyPress>", on_key_press)

    # Mostrar ventana
    root.mainloop()

# Jugar el juego
play_game_gui()