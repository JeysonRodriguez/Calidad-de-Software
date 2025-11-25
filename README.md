# Agenda de Tareas en Python  
**Mini–Proyecto del taller “Introducción a la Calidad en el Desarrollo de Software”**  
**Universidad Interamericana de Panamá**

---

## Descripción del Proyecto

Este mini–proyecto implementa una **Agenda de Tareas en consola**, desarrollada en Python, como parte del taller académico “Introducción a la Calidad en el Desarrollo de Software: de la teoría a la práctica”.

El sistema permite gestionar tareas mediante CRUD completo y se enfoca en prácticas de calidad: validaciones, manejo de errores, persistencia en JSON, bitácora (log), pruebas básicas y control de versiones (Git).

---

## Funcionalidades Principales

- Agregar una tarea con:
  - Descripción
  - Prioridad (baja, media, alta)
  - Fecha límite (validada)
- Listar todas las tareas  
- Listar tareas pendientes  
- Listar tareas completadas  
- Listar tareas pendientes de alta prioridad  
- Listar tareas vencidas  
- Editar una tarea  
- Eliminar una tarea  
- Marcar tarea como completada  
- Registro de eventos en **log.txt**  
- Persistencia en **tareas.json**

---

## 3. Requisitos Previos

- Python 3.8 o superior  
- Windows / Linux / macOS  
(No requiere librerías externas)

---

## Cómo ejecutar el programa


```bash
python main.py


## Enfoque de Calidad Aplicado

Este proyecto incorpora prácticas de calidad tales como:

Validación de entradas

- Descripciones no vacías
- Límite de caracteres
- Validación de prioridad
- Fecha válida y no vencida

Manejo de errores

- IDs numéricos
- Manejo de excepciones
- Entradas inválidas
- Persistencia en JSON
- Registro en bitácora (log.txt)
- Código modular y mantenible
- Uso de control de versiones (Git)

## Reflexión 

La calidad de software no es solo técnica, sino también ética y profesional. Un sistema sin validaciones ni manejo adecuado de errores puede fallar en producción y afectar a usuarios, datos y procesos críticos. Este proyecto demuestra la importancia de aplicar buenas prácticas desde el inicio del desarrollo.

## Autor

Jeyson Rodriguez
Universidad Interamericana de Panamá