# Metadatos de los Datos — Bladerunners HackODS 2026

---

## Dataset 1: Tasa de Abandono Escolar por Entidad Federativa

- **Fuente:** INEGI / Secretaría de Educación Pública (SEP)
- **Nombre oficial:** "Tasa de abandono escolar por entidad federativa según nivel educativo"
- **URL:** https://www.inegi.org.mx/app/tabulados/interactivos/?px=Educacion_11&bd=Educacion
- **Año de referencia:** Ciclo escolar 2022-2023
- **Fecha de consulta:** Abril 2026
- **Licencia:** Datos públicos del gobierno de México (uso libre con atribución)
- **Nivel de desagregación:** Entidad federativa × nivel educativo × sexo
- **Variables utilizadas:**
  | Variable | Descripción |
  |---|---|
  | `abandono_total` | Tasa de abandono en media superior, ambos sexos (%) |
  | `abandono_hombres` | Tasa de abandono — hombres (%) |
  | `abandono_mujeres` | Tasa de abandono — mujeres (%) |
- **Valores nacionales verificados (2022-23):** Total=11.2%, H=13.5%, M=9.1%

---

## Dataset 2: Pobreza Multidimensional — CONEVAL 2022

- **Fuente:** Consejo Nacional de Evaluación de la Política de Desarrollo Social (CONEVAL)
- **URL:** https://www.coneval.org.mx/Medicion/MP/Paginas/Pobreza_2022.aspx
- **Comunicado:** https://www.coneval.org.mx/SalaPrensa/Comunicadosprensa/Documents/2023/Comunicado_07_Medicion_Pobreza_2022.pdf
- **Año de referencia:** 2022 (ENIGH 2022 — publicada 26 julio 2023)
- **Fecha de consulta:** Abril 2026
- **Licencia:** Datos públicos del gobierno de México
- **Nivel de desagregación:** Entidad federativa
- **Variables utilizadas:**
  | Variable | Descripción |
  |---|---|
  | `pobreza_pct` | % población en pobreza multidimensional |
  | `pobreza_ext_pct` | % población en pobreza extrema |
  | `rezago_edu_pct` | % población con carencia por rezago educativo |
- **Valores nacionales:** Pobreza=36.3%, Pobreza extrema=7.1%
- **Estados con mayor pobreza:** Chiapas (67.4%), Guerrero (60.4%), Oaxaca (58.4%)

---

## Dataset 3: Acceso a Internet en Hogares — ENDUTIH 2023

- **Fuente:** INEGI / Instituto Federal de Telecomunicaciones (IFT)
- **Nombre oficial:** Encuesta Nacional sobre Disponibilidad y Uso de Tecnologías de la Información en los Hogares (ENDUTIH) 2023
- **URL:** https://www.inegi.org.mx/programas/endutih/2023/
- **Comunicado:** https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2024/ENDUTIH/ENDUTIH_23.pdf
- **Año de referencia:** 2023
- **Fecha de consulta:** Abril 2026
- **Licencia:** Datos públicos del gobierno de México
- **Nivel de desagregación:** Nacional, ámbito urbano/rural, entidad federativa
- **Variables utilizadas:**
  | Variable | Descripción |
  |---|---|
  | `internet_hogares_pct` | % hogares con acceso a internet |
- **Valores nacionales:** 71.7% hogares con internet; urbano=85.5%, rural=66.0%
- **Mayor cobertura:** CDMX (89.5%), Baja California (86.4%)
- **Menor cobertura:** Chiapas (44.3%), Oaxaca (53.0%), Guerrero (53.9%)

---

## Dataset 4: Metas ODS 4 — UNESCO UIS

- **Fuente:** UNESCO Institute for Statistics (UIS)
- **URL:** https://www.uis.unesco.org/en/data/sdg4-country-profiles
- **Año de referencia:** 2023
- **Uso en el proyecto:** Contextualización de indicadores mexicanos vs. metas internacionales ODS 4

---

## Notas de Integración

Los datasets 1-3 se cruzan a nivel de **entidad federativa** (32 estados).
La granularidad municipal no está disponible para todos los indicadores; el análisis
se realiza a nivel estatal como unidad de comparación más robusta estadísticamente.

El `Índice de Vulnerabilidad Educativa (IVE)` es una variable construida:
`IVE = (pobreza_pct + (100 − internet_hogares_pct)) / 2`
