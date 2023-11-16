## Introducción

Introducción
Redes neuronales recurrentes, memoria a largo plazo [13] y redes neuronales recurrentes y cerradas [7]
en particular, se han establecido firmemente como enfoques de última generación en el modelado de secuencias y
Problemas de transducción como el modelado de idiomas y la traducción automática [35, 2, 5].Numeroso
Desde entonces, los esfuerzos han seguido empujando los límites de los modelos de idiomas recurrentes y el codificador del codificador
Arquitecturas [38, 24, 15].
Los modelos recurrentes generalmente tienen en cuenta el cálculo a lo largo de las posiciones de símbolos de la entrada y salida
secuencias.Alineando las posiciones a los pasos en el tiempo de cálculo, generan una secuencia de ocultamiento
Estados HT, en función del estado oculto anterior HT - 1 y la entrada para la posición t.Esto inherentemente
La naturaleza secuencial impide la paralelización dentro de los ejemplos de entrenamiento, que se vuelve crítico en más tiempo
Longitudes de secuencia, a medida que las restricciones de memoria limitan el lote a través de los ejemplos.El trabajo reciente ha logrado
mejoras significativas en la eficiencia computacional a través de trucos de factorización [21] y condicional
Cálculo [32], al tiempo que mejora el rendimiento del modelo en el caso de este último.El fundamental
La restricción del cálculo secuencial, sin embargo, permanece.
Los mecanismos de atención se han convertido en una parte integral del modelado de secuencia convincente y
modelos de ción en varias tareas, lo que permite el modelado de dependencias sin tener en cuenta su distancia en
las secuencias de entrada o salida [2, 19].En todos menos unos pocos casos [27], sin embargo, tales mecanismos de atención
se utilizan junto con una red recurrente.
En este trabajo proponemos el transformador, una arquitectura modelo evita la recurrencia y en su lugar
Confiar completamente en un mecanismo de atención para atraer dependencias globales entre la entrada y la salida.
El transformador permite una paralelización significativamente más y puede llegar a un nuevo estado del arte en
Calidad de traducción después de recibir entrenamiento durante tan solo doce horas en ocho GPU P100.
2

