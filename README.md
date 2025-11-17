# Práctica 5 – Programación

**Autor:** Ismael Alexis Beh de la Rosa  
**Matrícula:** AL077957  
**Curso:** Programación  
**Profesor:** Juan A. Chuc Méndez  
**Fecha:** 18/11/2025  

---

## 🏗 Descripción general

Este proyecto aborda un problema real de **Ingeniería Civil** mediante **Python**: la dosificación de materiales para la elaboración de concreto utilizando una interfaz gráfica.  

El programa permite:  
- Recibir datos de entrada del usuario.  
- Realizar cálculos de dosificación.  
- Mostrar resultados de manera clara y organizada.  

Todo el código se encuentra en la carpeta `mi_modelado/`, cumpliendo con las indicaciones de la práctica.

---

## 📘 Marco teórico

La **dosificación del concreto** consiste en determinar la cantidad de cemento, arena, grava y agua necesarios para obtener una mezcla adecuada según los requerimientos estructurales.  

En ingeniería civil se emplean principalmente:  
- **Proporciones volumétricas** (ejemplo: 1 : 2 : 3).  
- **Relación agua/cemento (w/c)**.  
- **Conversión entre unidades** (kg, m³, latas, etc.).  

El objetivo de la dosificación es garantizar:  
- Buena trabajabilidad.  
- Resistencia mecánica adecuada.  
- Durabilidad de la mezcla.  

El método implementado en este proyecto se basa en **reglas proporcionales**, calculando los materiales a partir de una proporción base.

---

## 🧮 Modelado del problema

El programa se estructura en tres etapas principales:

### 1. Análisis
- Ingreso de datos requeridos (ejemplo: número de latas o tipo de mezcla).  
- Validación de que los datos sean numéricos.  
- Almacenamiento de proporciones mediante diccionarios y listas.  

### 2. Diseño
El código se organiza en funciones que realizan:  
- Cálculo de cemento, arena y grava según la proporción seleccionada.  
- Conversión entre diferentes unidades.  
- Presentación clara de los resultados.  
- Integración con la interfaz gráfica.  

**Ejemplo de estructura utilizada:**

```python
proporciones = {
    "f'c 150": (1, 2, 3),
    "f'c 200": (1, 1.5, 3)
}
