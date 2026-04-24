# Declaratoria de Uso de Inteligencia Artificial
## Plantilla oficial HackODS UNAM 2026

**Equipo:** Bladerunners
**Integrantes:** Luis Fernando Martínez Moreno · Guadalupe Herrera Barragán · Ana Lydia Herrera Macías
**Fecha:** Abril 2026 · **ODS:** 4, 1, 5, 10

---

## 1. Herramientas de IA utilizadas

| Herramienta | Proveedor | Versión | Uso específico |
|---|---|---|---|
| Claude | Anthropic | Sonnet 4 | Estructuración del flujo de trabajo, revisión de código R/Quarto, borrador de narrativa |
| GitHub Copilot | GitHub/Microsoft | — | Autocompletado de sintaxis en RStudio |

## 2. Descripción del uso

- **Datos:** Los datos utilizados son 100% de fuentes oficiales (INEGI, CONEVAL, SEP, UNESCO). La IA no generó ni inventó ningún dato.
- **Análisis:** El diseño de la pregunta de investigación, la selección de variables y la interpretación de resultados fueron decididos por el equipo. La IA fue usada para revisar código R y sugerir alternativas de visualización.
- **Código:** Todo el código fue revisado, entendido y validado por el equipo antes de ser incorporado al repositorio.
- **Narrativa:** El framing del problema, la justificación de la selección de datos y las conclusiones son del equipo.

## 3. Transparencia sobre datos

Todos los valores numéricos del dashboard provienen directamente de:
- INEGI Tabulado Educacion_11 (abandono por entidad y sexo, ciclo 2022-23)
- CONEVAL Comunicado 07/2023 (pobreza multidimensional 2022)
- INEGI Comunicado ENDUTIH 372/24 (hogares con internet 2023)

Las URLs de todas las fuentes están documentadas en `datos/metadata.md` y en el `README.md`.

## 4. Limitaciones reconocidas

- Los datos de ENDUTIH están disponibles a nivel estatal. Un análisis municipal requeriría el Censo de Población 2020 (INEGI) como proxy de conectividad.
- El modelo de regresión es correlacional/observacional; no implica causalidad.
- Los datos de abandono por sexo a nivel estatal son los más recientes disponibles públicamente (ciclo 2022-23); datos municipales desagregados por sexo no están en acceso abierto.

---

*Firmado por los integrantes del equipo Bladerunners.*
