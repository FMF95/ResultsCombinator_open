# 馃殌 Combinador de Resultados - Ayuda

Bienvenido a **Combinador de Resultados**. Esta aplicaci贸n te permite combinar, analizar y exportar resultados en formato CSV generados por ResultsQuery o Results2CSV.

---

## 馃搨 Carga de Archivos

- **Carga m煤ltiple:** Puedes cargar varios archivos CSV a la vez.

> Al volver a cargar archivos los anteriores se eliminan de la aplicaci贸n.

- **Soporte para ResultsQuery y Results2CSV:** Elige el formato al iniciar la aplicaci贸n.

- **Detecci贸n autom谩tica de errores:** Los archivos con problemas de lectura se marcan en el 谩rbol.

---


## 馃М Operaciones Disponibles

### Suma / M谩ximo / M铆nimo / Promedio (con agrupaci贸n)
- Selecciona una o varias columnas de texto en 鈥淎grupar por鈥?

> Selecciona columnas para ver el resultado por grupo. Si no seleccionas ninguna, se muestra el valor global.

- Marca las 鈥淐olumnas objetivo鈥?sobre las que aplicar la operaci贸n.

- El resultado contiene una fila por combinaci贸n 煤nica de las columnas de texto.

Ejemplo:
| Nodo | Caso | V1 | V2 |
|-----:|:----:|---:|---:|
| N1   | C1   | 10 |  5 |
| N1   | C1   | 20 |  7 |
| N2   | C1   | 15 |  8 |

Agrupar por [Nodo, Caso], operaci贸n 鈥淪uma鈥?
| Nodo | Caso | V1 | V2 |
|-----:|:----:|---:|---:|
| N1   | C1   | 30 | 12 |
| N2   | C1   | 15 |  8 |

---

### Filtrar por m谩ximo / m铆nimo (con agrupaci贸n)
- Columna izquierda: 鈥淎grupar por (columnas de texto)鈥?para definir los grupos.

- Columna derecha: 鈥淐olumna objetivo (una)鈥?para elegir el valor a optimizar.

- Devuelve la fila completa (todas las columnas) correspondiente al m谩ximo o m铆nimo por grupo.

Ejemplo:
| Nodo | Caso | V1 | V2 |
|-----:|:----:|---:|---:|
| N1   | C1   | 10 |  5 |
| N1   | C1   | 20 |  7 |
| N2   | C1   | 15 |  8 |

Agrupar por [Nodo, Caso], filtrar por m谩ximo de V1:
| Nodo | Caso | V1 | V2 |
|-----:|:----:|---:|---:|
| N1   | C1   | 20 |  7 |
| N2   | C1   | 15 |  8 |

Esto preserva coherencia: una fila por cada combinaci贸n 煤nica de [Nodo, Caso], y cada fila es la que tiene el m谩ximo (o m铆nimo) en la columna objetivo.

---

### Envolvente (m谩x/m铆n con factores)
- Escala cada tabla por un 鈥淔actor global鈥?y un 鈥淔actor鈥?por tabla.

- Combina columna a columna tomando el m谩ximo o el m铆nimo entre tablas para columnas num茅ricas.

- Las columnas de texto se conservan de la primera tabla; columnas exclusivas se a帽aden.

> F贸rmula conceptual:
>
> Para cada columna num茅rica j y fila i:
> max-envelope: result[i,j] = max_k( factor_global * factor_tabla_k * tabla_k[i,j] )

---

## 馃彿锔?Clasificaci贸n de Columnas

- **Texto/Valor:** Puedes clasificar las columnas como texto o valor para personalizar las operaciones.

- **Acceso r谩pido:** Haz clic en el encabezado del 谩rbol para modificar la clasificaci贸n.

---

## 馃攳 Visualizaci贸n y Filtros

- **Vista de tabla y texto:** Alterna entre la tabla de datos y la informaci贸n textual de cada archivo.

- **Filtros por columna:** Filtra r谩pidamente los datos visibles en la tabla.

---

## 馃捑 Exportaci贸n

- **Exporta cualquier resultado:** Selecciona la tabla y columnas a exportar.

- **Formato CSV:** Compatible con la mayor铆a de hojas de c谩lculo.

---

## 馃摑 Consola de Diagn贸stico

- **Mensajes de log y errores:** Consulta todo lo que ocurre en la aplicaci贸n.

- **Exporta el log:** Guarda el historial de mensajes para auditor铆a o soporte.

---

## 鉁?Renombrar entradas

- En la vista de Informaci贸n, usa el bot贸n 鈥淩enombrar entrada鈥?para cambiar el nombre de la clave seleccionada.
- El nombre debe ser 煤nico y no puede estar vac铆o.
- El cambio se refleja autom谩ticamente en el 谩rbol de visualizaci贸n, el 谩rbol de operaciones y el panel de exportaci贸n.

---

## 馃鈥嶐煉?Atajos 煤tiles

- **Ctrl+C:** Abrir archivos.
- **Ctrl+L:** Limpiar datos.
- **Ctrl+V:** Mostrar panel de visualizaci贸n.
- **Ctrl+O:** Mostrar panel de operaciones.
- **Ctrl+E:** Mostrar panel de exportar.
- **Ctrl+H:** Mostrar esta ayuda.

---
##  馃摡 Contacto 

franciscomiralles95@gmail.com

---
---

_Disfruta combinando y analizando tus resultados de forma profesional y sencilla._