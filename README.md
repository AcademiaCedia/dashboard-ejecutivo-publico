# Dashboard ejecutivo público de Academia CEDIA

[Consultar el dashboard](https://academiacedia.github.io/dashboard-ejecutivo-publico/)

El resumen financiero compara los ingresos agregados en 2025 y 2026. Uso de servicios permite seleccionar uno o ambos paquetes institucionales. La tercera pestaña muestra el ingreso fuera del paquete de 2026 y destaca la cantidad y el valor total de las ofertas en negociación.

## Ejecución y mantenimiento

Abra index.html en un navegador moderno. El visor utiliza HTML, CSS y JavaScript con recursos locales en assets/. GitHub Pages publica la raíz de la rama main.

La fuente institucional es el libro Revisión dirección ejecutiva. En el equipo autorizado, actualice la extracción privada y ejecute `python actualizar.py "/ruta/privada/datos.js"` con Python 3.10 o superior. Revise las cifras agregadas en index.html y registre el HTML actualizado en main. El generador solo escribe indicadores agregados. Conserve el libro y la extracción de origen fuera de este repositorio.
