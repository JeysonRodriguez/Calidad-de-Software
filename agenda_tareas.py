import json
import os
from datetime import datetime, date

# ==========================================================
# Mini-proyecto: Agenda de Tareas
# Taller: Introducción a la Calidad en el Desarrollo de Software
# Enfoque: Calidad de Software (validaciones, pruebas básicas,
#    
# ==========================================================

ARCHIVO_TAREAS = "tareas.json"
ARCHIVO_LOG = "log.txt"
VALID_PRIORIDADES = {"baja", "media", "alta"}


# ----------------------------------------------------------
# Utilidades de calidad: bitácora (log)
# ----------------------------------------------------------
def log_evento(mensaje):
    """
    Registra un evento en la bitácora con marca de tiempo.
    Esto aporta trazabilidad al mini proyecto.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] {mensaje}\n"
    try:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
            f.write(linea)
    except IOError:
        # No detenemos la app por fallos de log, solo avisamos
        print("ADVERTENCIA: No se pudo escribir en el archivo de log.")


# ----------------------------------------------------------
# Persistencia de tareas (JSON)
# ----------------------------------------------------------
def cargar_tareas():
    """
    Carga las tareas desde el archivo JSON.
    Si no existe o ocurre un error, devuelve una lista vacía.
    """
    if not os.path.exists(ARCHIVO_TAREAS):
        log_evento("Archivo de tareas no encontrado, se inicia lista vacía.")
        return []

    try:
        with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                log_evento(f"Se cargaron {len(data)} tareas desde el archivo.")
                return data
            else:
                log_evento("Formato de tareas inválido, se inicia lista vacía.")
                return []
    except (json.JSONDecodeError, IOError):
        log_evento("Error al cargar tareas, se inicia lista vacía.")
        return []


def guardar_tareas(tareas):
    """
    Guarda la lista de tareas en el archivo JSON.
    """
    try:
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as f:
            json.dump(tareas, f, ensure_ascii=False, indent=4)
        log_evento(f"Se guardaron {len(tareas)} tareas en el archivo.")
    except IOError:
        print("ERROR: No se pudieron guardar las tareas en el archivo.")
        log_evento("ERROR: Fallo al guardar tareas en el archivo.")


# ----------------------------------------------------------
# Lógica de negocio de tareas
# ----------------------------------------------------------
def generar_nuevo_id(tareas):
    """
    Genera un ID incremental simple para una nueva tarea.
    """
    if not tareas:
        return 1
    ids = [t.get("id", 0) for t in tareas]
    return max(ids) + 1


def pedir_prioridad():
    """
    Pide al usuario la prioridad de la tarea.
    """
    print("Selecciona la prioridad de la tarea:")
    print("1. Baja")
    print("2. Media")
    print("3. Alta")
    opcion = input("Opción (1-3): ").strip()

    if opcion == "1":
        return "baja"
    elif opcion == "2":
        return "media"
    elif opcion == "3":
        return "alta"
    else:
        print("Prioridad inválida. Se asignará 'baja' por defecto.")
        log_evento("Prioridad inválida ingresada; se asignó 'baja' por defecto.")
        return "baja"


def pedir_fecha_limite():
    """
    Pide una fecha límite opcional en formato YYYY-MM-DD.
    - Si el usuario deja vacío: no se asigna fecha.
    - Si la fecha es inválida o pasada: se rechaza y no se asigna.
    """
    fecha_str = input("Fecha límite (YYYY-MM-DD) o deja vacío si no aplica: ").strip()
    if not fecha_str:
        return ""

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        print("Formato de fecha inválido. No se asignará fecha límite.")
        log_evento(f"Fecha inválida ingresada: {fecha_str}")
        return ""

    hoy = date.today()
    if fecha < hoy:
        print("ERROR: La fecha límite no puede ser anterior a hoy. No se asignará fecha.")
        log_evento(f"Fecha límite en el pasado rechazada: {fecha_str}")
        return ""

    return fecha_str


def crear_tarea(tareas):
    """
    Crea una nueva tarea con descripción, prioridad y fecha límite.
    """
    descripcion = input("Descripción de la tarea: ").strip()

    if not descripcion:
        print("ERROR: La descripción no puede estar vacía.")
        log_evento("Intento de crear tarea con descripción vacía.")
        return

    if len(descripcion) > 200:
        print("ERROR: La descripción es demasiado larga (máx. 200 caracteres).")
        log_evento("Intento de crear tarea con descripción > 200 caracteres.")
        return

    prioridad = pedir_prioridad()
    fecha_limite = pedir_fecha_limite()

    nueva = {
        "id": generar_nuevo_id(tareas),
        "descripcion": descripcion,
        "prioridad": prioridad,
        "fecha_limite": fecha_limite,
        "completada": False,
    }

    tareas.append(nueva)
    guardar_tareas(tareas)
    print(f"Tarea creada con ID {nueva['id']}.")
    log_evento(f"Se creó la tarea ID={nueva['id']} - '{descripcion}'.")


def mostrar_tareas(tareas, estado=None, prioridad=None, solo_vencidas=False):
    """
    Muestra las tareas en consola con filtros:
    - estado: None, 'pendiente' o 'completada'
    - prioridad: None o 'baja'/'media'/'alta'
    - solo_vencidas: True para mostrar solo tareas con fecha pasada y no completadas
    """
    if not tareas:
        print("No hay tareas registradas.")
        return

    hoy = date.today()
    print("\nLISTA DE TAREAS:")
    hay_al_menos_una = False

    for t in tareas:
        # Filtro por estado
        if estado is not None:
            if estado == "pendiente" and t.get("completada"):
                continue
            if estado == "completada" and not t.get("completada"):
                continue

        # Filtro por prioridad
        if prioridad is not None and t.get("prioridad") != prioridad:
            continue

        # Filtro por vencidas
        if solo_vencidas:
            fecha_str = t.get("fecha_limite") or ""
            if not fecha_str:
                continue
            try:
                fecha_tarea = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                continue
            # Solo vencidas y no completadas
            if not (fecha_tarea < hoy and not t.get("completada")):
                continue

        est = "✔ Completada" if t.get("completada") else "Pendiente"
        hay_al_menos_una = True
        print(
            f"ID: {t.get('id')} | {t.get('descripcion')} "
            f"| Prioridad: {t.get('prioridad')} "
            f"| Fecha límite: {t.get('fecha_limite') or 'N/A'} "
            f"| Estado: {est}"
        )

    if not hay_al_menos_una:
        print("No hay tareas que cumplan con los filtros seleccionados.")


def buscar_tarea_por_id(tareas, id_buscar):
    """
    Devuelve la tarea con el ID dado, o None si no existe.
    """
    for t in tareas:
        if t.get("id") == id_buscar:
            return t
    return None


def marcar_completada(tareas):
    """
    Marca una tarea como completada a partir de su ID.
    """
    if not tareas:
        print("No hay tareas.")
        return

    try:
        id_str = input("Ingresa el ID de la tarea a marcar como completada: ").strip()
        id_tarea = int(id_str)
    except ValueError:
        print("ERROR: Debes ingresar un número entero.")
        log_evento("ERROR: ID no numérico al marcar completada.")
        return

    tarea = buscar_tarea_por_id(tareas, id_tarea)

    if tarea is None:
        print("No existe una tarea con ese ID.")
        log_evento(f"ERROR: Intento de marcar tarea inexistente ID={id_tarea}.")
        return

    if tarea.get("completada"):
        print("La tarea ya está completada.")
        return

    tarea["completada"] = True
    guardar_tareas(tareas)
    print(f"Tarea '{tarea.get('descripcion')}' marcada como completada.")
    log_evento(f"Tarea ID={id_tarea} marcada como completada.")


def eliminar_tarea(tareas):
    """
    Elimina una tarea por ID.
    """
    if not tareas:
        print("No hay tareas.")
        return

    try:
        id_str = input("Ingresa el ID de la tarea a eliminar: ").strip()
        id_tarea = int(id_str)
    except ValueError:
        print("ERROR: Debes ingresar un número entero.")
        log_evento("ERROR: ID no numérico al eliminar tarea.")
        return

    tarea = buscar_tarea_por_id(tareas, id_tarea)

    if tarea is None:
        print("No existe una tarea con ese ID.")
        log_evento(f"ERROR: Intento de eliminar tarea inexistente ID={id_tarea}.")
        return

    tareas.remove(tarea)
    guardar_tareas(tareas)
    print(f"Tarea '{tarea.get('descripcion')}' eliminada.")
    log_evento(f"Tarea ID={id_tarea} eliminada.")


def editar_tarea(tareas):
    """
    Permite modificar descripción, prioridad y fecha límite de una tarea por ID.
    """
    if not tareas:
        print("No hay tareas.")
        return

    try:
        id_str = input("Ingresa el ID de la tarea a editar: ").strip()
        id_tarea = int(id_str)
    except ValueError:
        print("ERROR: Debes ingresar un número entero.")
        log_evento("ERROR: ID no numérico al editar tarea.")
        return

    tarea = buscar_tarea_por_id(tareas, id_tarea)

    if tarea is None:
        print("No existe una tarea con ese ID.")
        log_evento(f"ERROR: Intento de editar tarea inexistente ID={id_tarea}.")
        return

    print(
        f"Tarea actual: {tarea.get('descripcion')} "
        f"(Prioridad: {tarea.get('prioridad')}, "
        f"Fecha límite: {tarea.get('fecha_limite') or 'N/A'})"
    )

    nueva_desc = input("Nueva descripción (Enter para dejar igual): ").strip()
    if nueva_desc:
        if len(nueva_desc) > 200:
            print("La descripción nueva es demasiado larga. No se actualiza.")
            log_evento("Intento de descripción nueva > 200 caracteres al editar tarea.")
        else:
            tarea["descripcion"] = nueva_desc

    cambiar_prioridad = input("¿Deseas cambiar la prioridad? (s/n): ").strip().lower()
    if cambiar_prioridad == "s":
        tarea["prioridad"] = pedir_prioridad()

    cambiar_fecha = input("¿Deseas cambiar la fecha límite? (s/n): ").strip().lower()
    if cambiar_fecha == "s":
        tarea["fecha_limite"] = pedir_fecha_limite()

    guardar_tareas(tareas)
    print("Tarea actualizada.")
    log_evento(f"Tarea ID={id_tarea} actualizada.")


# ----------------------------------------------------------
# Interfaz de consola (menú)
# ----------------------------------------------------------
def mostrar_menu():
    """
    Muestra el menú principal de la aplicación.
    """
    print("\n======== MENÚ AGENDA DE TAREAS ========")
    print("1. Agregar tarea")
    print("2. Listar todas las tareas")
    print("3. Listar tareas pendientes")
    print("4. Listar tareas completadas")
    print("5. Listar tareas pendientes de alta prioridad")
    print("6. Marcar tarea como completada")
    print("7. Editar tarea")
    print("8. Eliminar tarea")
    print("9. Listar tareas vencidas")
    print("10. Salir")
    print("=======================================")


def main():
    """
    Punto de entrada principal de la aplicación.
    """
    log_evento("Aplicación iniciada.")
    tareas = cargar_tareas()
    print("Bienvenido a la Agenda de Tareas (Calidad de Software).")

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-10): ").strip()

        if opcion == "1":
            crear_tarea(tareas)
        elif opcion == "2":
            mostrar_tareas(tareas)
        elif opcion == "3":
            mostrar_tareas(tareas, estado="pendiente")
        elif opcion == "4":
            mostrar_tareas(tareas, estado="completada")
        elif opcion == "5":
            mostrar_tareas(tareas, estado="pendiente", prioridad="alta")
        elif opcion == "6":
            marcar_completada(tareas)
        elif opcion == "7":
            editar_tarea(tareas)
        elif opcion == "8":
            eliminar_tarea(tareas)
        elif opcion == "9":
            mostrar_tareas(tareas, solo_vencidas=True)
        elif opcion == "10":
            print("Saliendo de la aplicación. ¡Hasta luego!")
            log_evento("Aplicación finalizada por el usuario.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")
            log_evento(f"Opcion invalida ingresada en el menu: '{opcion}'.")


if __name__ == "__main__":
    main()
