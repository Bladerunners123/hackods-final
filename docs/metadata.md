# Metadatos del tablero

## Fuentes

- INEGI / SEP: abandono escolar en media superior por entidad y sexo, ciclo 2022-2023.
- CONEVAL: pobreza multidimensional y rezago educativo, 2022.
- ENDUTIH: hogares con acceso a internet, 2023.

## Cobertura

- 32 entidades federativas de México.
- Desagregación por sexo para abandono escolar.

## Variable construida

- `IVE = (pobreza_pct + (100 - internet_hogares_pct)) / 2`
- Se considera zona crítica cuando `IVE > 50`.

## Limitaciones

- La comparación es estatal y no sustituye análisis municipal o local.
- Las fuentes combinan cortes 2022 y 2023.
- El tablero sirve para priorización territorial, no para afirmar causalidad por sí solo.
