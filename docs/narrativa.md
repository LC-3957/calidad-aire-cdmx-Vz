# PROYECTO: Calidad del Aire en la CDMX

### PREGUNTA CENTRAL.
¿Respiramos peor los lunes? Patrones de contaminación en la ciudad más grande del país.

### DATOS OBTENIDOS DE.
https://repositorio-salud.conacyt.mx/jspui/handle/1000/235
SEDEMA · Sistema de Monitoreo Atmosférico (SIMAT) · 2011–2021 · 3.5 millones de registros · 69 estaciones

### PÚBLICO OBJETIVO:
Público general mexicano. Cualquier persona adulta, sin conocimientos técnicos, que vive en zona urbana, le interesa su salud y accede desde computadora o celular.



## INTRODUCCIÓN.

¿Has escuchado que los lunes el aire está más contaminado? Mucha gente lo dice, y tiene sentido: es el día que más autos salen a la calle después del fin de semana.

Pero los datos cuentan una historia diferente — y un poco inquietante: **el día que más emisiones hay NO es el mismo día que más daño respiramos.**

Para entenderlo, necesitamos separar dos fenómenos:
- El NO₂ (dióxido de nitrógeno) → sale del escape de los autos. Es el tráfico en tiempo real.
- El Ozono (O₃) → se forma cuando el sol "cocina" esas emisiones. Es la consecuencia retrasada.



## DESARROLLO.

--- Viz 1 — ¿Cuándo hay más autos en la ciudad?

Gráfica de barras agrupadas: tres momentos del día (6am, 12pm, 18pm) vs día de la semana
Contaminante: NO₂ (sale directamente del escape)

Lo que descubre el lector: La barra naranja (6am) es consistentemente la más alta de lunes a viernes, con el pico máximo entre martes y jueves. El domingo es el día más limpio en todos los horarios — menos autos, menos emisiones directas.

Justificación del tipo de gráfica: Las barras agrupadas son más intuitivas que un heatmap para público general. Cada hora se distingue por color (naranja=mañana, rojo=mediodía, azul=tarde-noche) y la altura de la barra comunica inmediatamente "más tráfico".


--- Viz 2 — Si hay más autos entre semana, ¿cuándo sube el Ozono?

Líneas comparativas normalizadas en escala 0–100 (100 = el peor momento de la semana para cada contaminante)
Contaminante: Ozono (irrita ojos y garganta, se forma con el sol)

Lo que descubre el lector: Ambas líneas están en la misma escala. El NO₂ sube gradualmente de lunes a viernes y cae el fin de semana — siguiendo exactamente el patrón del tráfico laboral. El Ozono, en cambio, es más estable entre semana y tiene su pico el domingo, cuando el sol acumula horas sobre las emisiones de días anteriores.

Justificación del tipo de gráfica: Una escala normalizada 0–100 elimina la confusión del doble eje Y. El público no necesita entender unidades técnicas (ppb, µg/m³) para ver el desfase temporal entre causa (NO₂) y consecuencia (Ozono).


--- Viz 3 — El ranking: ¿qué día es el PEOR para tu salud?

Barras horizontales ordenadas de peor a mejor. Selector interactivo para cambiar entre contaminantes (O₃, NO₂, PM2.5)

Lo que descubre el lector: Cada contaminante tiene su propio patrón semanal, y no todos apuntan al mismo día como el peor. Para el Ozono, el domingo es el día más alto — no el lunes ni el jueves. Las emisiones acumuladas de la semana, procesadas por el sol del fin de semana, producen su mayor concentración cuando menos lo esperamos.

Justificación del tipo de gráfica: El ranking es el formato más directo para que alguien recuerde un dato concreto. Las barras horizontales ordenadas evitan interpretación — el orden lo dice todo. El selector permite al lector explorar por cuenta propia.



## CONCLUSIÓN.

Los datos de 10 años de monitoreo en la CDMX revelan dos fenómenos que no se mueven al mismo tiempo:

- Lunes a viernes: más autos, más emisiones directas (NO₂ alto). El pico máximo se concentra en la mañana (6am), especialmente entre martes y jueves.
- Fin de semana: aunque el NO₂ baja, el Ozono alcanza su concentración más alta el domingo, cuando el sol ha tenido horas para transformar las emisiones de la semana.

Recomendación práctica: Si puedes elegir cuándo salir a caminar, hacer ejercicio o ventilar tu casa, considera que el domingo por la tarde puede tener más Ozono de lo que imaginas, especialmente tras una semana de tráfico intenso.

El mito del "lunes sucio" apunta al síntoma equivocado. El día que más daño respiramos no es cuando hay más autos en la calle, sino cuando esos autos ya se fueron y el sol llevó horas acumulando contaminación.