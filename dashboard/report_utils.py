from pathlib import Path
from textwrap import dedent
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime, timezone
from xml.sax.saxutils import escape
import re

import pandas as pd
import plotly.io as pio


def export_methodology_report(
    report_dir: Path,
    palette: dict,
    fig_tendencia,
    fig_relaciones,
    fig_heatmap,
    fig_mapa,
    zonas_criticas: pd.DataFrame,
    resumen_modelos: pd.DataFrame,
    nota_recalculo: bool = False,
) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "reporte_metodologia.html"
    tendencia_html = pio.to_html(fig_tendencia, include_plotlyjs="cdn", full_html=False)
    relaciones_html = pio.to_html(fig_relaciones, include_plotlyjs=False, full_html=False)
    heatmap_html = pio.to_html(fig_heatmap, include_plotlyjs=False, full_html=False)
    mapa_html = pio.to_html(fig_mapa, include_plotlyjs=False, full_html=False)

    zonas_html = zonas_criticas.to_html(index=False, classes="tabla") if not zonas_criticas.empty else "<p>No hay entidades con IVE &gt; 50.</p>"
    modelos_html = resumen_modelos.round(3).to_html(index=False, classes="tabla") if not resumen_modelos.empty else "<p>No se encontró resumen_modelos.csv.</p>"
    nota_html = (
        '<p class="nota"><strong>Nota de consistencia:</strong> el archivo <code>zonas_criticas.csv</code> estaba vacío. '
        'El reporte recalcula la clasificación correcta directamente desde <code>datos_estados.csv</code> con la regla IVE &gt; 50.</p>'
        if nota_recalculo else ""
    )

    body = dedent(
        f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Reporte metodológico | Bladerunners</title>
          <style>
            body {{ font-family: Inter, Arial, sans-serif; margin: 0; background: {palette['bg']}; color: {palette['text']}; }}
            main {{ max-width: 1180px; margin: 0 auto; padding: 40px 24px 64px; }}
            h1, h2 {{ color: {palette['primary']}; }}
            .hero {{ background: {palette['primary']}; color: white; padding: 28px 32px; border-radius: 24px; margin-bottom: 24px; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin: 24px 0; }}
            .card {{ background: white; border-radius: 22px; padding: 22px; box-shadow: 0 12px 30px rgba(10, 80, 102, 0.12); }}
            .tag {{ display: inline-block; background: {palette['accent']}; color: white; border-radius: 999px; padding: 6px 12px; font-size: 12px; font-weight: 700; }}
            .formula {{ background: #f7fafb; border-left: 8px solid {palette['accent']}; padding: 18px 20px; border-radius: 16px; margin: 16px 0; }}
            .tabla {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
            .tabla th, .tabla td {{ border-bottom: 1px solid #d8e0e5; padding: 10px 12px; text-align: left; }}
            .tabla th {{ background: #f4f7f8; }}
            .nota {{ background: #fff3f8; border-left: 6px solid {palette['accent']}; padding: 12px 14px; border-radius: 12px; }}
            ul {{ line-height: 1.6; }}
          </style>
        </head>
        <body>
          <main>
            <section class="hero">
              <p class="tag">Bladerunners · HackODS UNAM 2026</p>
              <h1>Reporte metodológico detallado</h1>
              <p>Este reporte documenta la lógica del tablero, las señales del modelo exploratorio, la serie histórica, el mapa del IVE y la regla final usada para definir zonas críticas.</p>
            </section>

            <section class="grid">
              <article class="card">
                <h2>Regla de priorización</h2>
                <div class="formula">
                  <strong>IVE = (pobreza + porcentaje de hogares sin internet) / 2</strong>
                  <p>Una entidad entra a zona crítica cuando <strong>IVE &gt; 50</strong>. Esta es la regla operativa vigente del tablero final.</p>
                </div>
                {nota_html}
              </article>
              <article class="card">
                <h2>Lectura del modelo</h2>
                {modelos_html}
                <p>El modelo se usa para lectura exploratoria y priorización, no para afirmar causalidad mecánica. Su valor está en ordenar señales y guiar inversión temprana.</p>
              </article>
            </section>

            <section class="card">
              <h2>Tendencia histórica</h2>
              {tendencia_html}
            </section>

            <section class="grid">
              <article class="card">
                <h2>Relaciones del modelo</h2>
                {relaciones_html}
              </article>
              <article class="card">
                <h2>Mapa de correlaciones</h2>
                {heatmap_html}
              </article>
            </section>

            <section class="card">
              <h2>Mapa del IVE por entidad</h2>
              {mapa_html}
            </section>

            <section class="card">
              <h2>Entidades en zona crítica</h2>
              {zonas_html}
            </section>
          </main>
        </body>
        </html>
        """
    )
    report_path.write_text(body, encoding="utf-8")
    return report_path


def _sanitize_sheet_name(name: str, used: set[str]) -> str:
    name = re.sub(r"[\\/*?:\[\]]", "_", str(name)).strip() or "Hoja"
    name = name[:31]
    base = name
    i = 1
    while name in used:
        suffix = f"_{i}"
        name = (base[: 31 - len(suffix)] + suffix)[:31]
        i += 1
    used.add(name)
    return name


def _col_letter(idx: int) -> str:
    letters = ""
    while idx > 0:
        idx, rem = divmod(idx - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def _excel_cell(value) -> tuple[str, str] | None:
    if pd.isna(value):
        return None
    if isinstance(value, (pd.Timestamp, datetime)):
        text = value.isoformat()
        return "inlineStr", f"<is><t>{escape(text)}</t></is>"
    if isinstance(value, bool):
        return "b", "1" if value else "0"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "n", str(value)
    text = str(value)
    return "inlineStr", f"<is><t>{escape(text)}</t></is>"


def _sheet_xml(df: pd.DataFrame) -> str:
    rows = []
    header_vals = list(df.columns)
    data_rows = [header_vals] + df.astype(object).where(pd.notnull(df), None).values.tolist()
    for r_idx, row in enumerate(data_rows, start=1):
        cells = []
        for c_idx, value in enumerate(row, start=1):
            cell = _excel_cell(value)
            if cell is None:
                continue
            cell_type, payload = cell
            ref = f"{_col_letter(c_idx)}{r_idx}"
            if cell_type == "inlineStr":
                cells.append(f'<c r="{ref}" t="inlineStr">{payload}</c>')
            else:
                cells.append(f'<c r="{ref}" t="{cell_type}"><v>{payload}</v></c>')
        rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    max_col = max(1, len(df.columns))
    max_row = max(1, len(df) + 1)
    dim = f"A1:{_col_letter(max_col)}{max_row}"
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="{dim}"/>'
        '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
        '<sheetFormatPr defaultRowHeight="15"/>'
        f'<sheetData>{"".join(rows)}</sheetData>'
        '</worksheet>'
    )


def _write_xlsx_fallback(path: Path, sheets: dict[str, pd.DataFrame]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    used = set()
    sheet_names = [_sanitize_sheet_name(name, used) for name in sheets.keys()]
    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for i in range(1, len(sheet_names) + 1):
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content_types.append('</Types>')

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        '</Relationships>'
    )

    workbook_sheets = []
    workbook_rels = []
    for i, name in enumerate(sheet_names, start=1):
        workbook_sheets.append(f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>')
        workbook_rels.append(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        )
    workbook_rels.append(
        f'<Relationship Id="rId{len(sheet_names)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )

    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<bookViews><workbookView xWindow="0" yWindow="0" windowWidth="24000" windowHeight="12000"/></bookViews>'
        f'<sheets>{"".join(workbook_sheets)}</sheets>'
        '</workbook>'
    )

    workbook_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'{"".join(workbook_rels)}'
        '</Relationships>'
    )

    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        '</styleSheet>'
    )

    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:creator>OpenAI</dc:creator>'
        '<cp:lastModifiedBy>OpenAI</cp:lastModifiedBy>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{created}</dcterms:modified>'
        '</cp:coreProperties>'
    )

    titles = ''.join(f'<vt:lpstr>{escape(name)}</vt:lpstr>' for name in sheet_names)
    app = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        '<Application>Python</Application>'
        f'<TitlesOfParts><vt:vector size="{len(sheet_names)}" baseType="lpstr">{titles}</vt:vector></TitlesOfParts>'
        f'<HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>{len(sheet_names)}</vt:i4></vt:variant></vt:vector></HeadingPairs>'
        '</Properties>'
    )

    with ZipFile(path, 'w', compression=ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', ''.join(content_types))
        zf.writestr('_rels/.rels', rels)
        zf.writestr('docProps/core.xml', core)
        zf.writestr('docProps/app.xml', app)
        zf.writestr('xl/workbook.xml', workbook)
        zf.writestr('xl/_rels/workbook.xml.rels', workbook_rels_xml)
        zf.writestr('xl/styles.xml', styles)
        for i, (_, df) in enumerate(sheets.items(), start=1):
            zf.writestr(f'xl/worksheets/sheet{i}.xml', _sheet_xml(df))
    return path


def _xlsxwriter_report(excel_path: Path, sheets: dict[str, pd.DataFrame]) -> Path:
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        workbook = writer.book
        fmt_header = workbook.add_format({"bold": True, "bg_color": "#0b4f66", "font_color": "#FFFFFF"})
        fmt_note = workbook.add_format({"text_wrap": True})

        sheet_refs = {}
        for name, df in sheets.items():
            sheet_name = name[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            ws = writer.sheets[sheet_name]
            ws.freeze_panes(1, 0)
            ws.set_row(0, None, fmt_header)
            width = min(18, max(12, int(max(len(str(c)) for c in df.columns) * 1.15)))
            ws.set_column(0, max(0, len(df.columns) - 1), width)
            sheet_refs[name] = sheet_name

        if "panorama_abandono" in sheets and not sheets["panorama_abandono"].empty:
            ws = writer.sheets[sheet_refs["panorama_abandono"]]
            chart = workbook.add_chart({"type": "bar"})
            rows = len(sheets["panorama_abandono"])
            chart.add_series({
                "name": "Abandono MS %",
                "categories": [sheet_refs["panorama_abandono"], 1, 0, rows, 0],
                "values": [sheet_refs["panorama_abandono"], 1, 1, rows, 1],
                "fill": {"color": "#1e6a83"},
                "border": {"color": "#1e6a83"},
            })
            chart.set_title({"name": "Top 5 abandono"})
            chart.set_x_axis({"name": "Tasa (%)"})
            chart.set_y_axis({"reverse": True})
            chart.set_legend({"none": True})
            ws.insert_chart("F2", chart, {"x_scale": 1.15, "y_scale": 1.15})

        if "tendencia_ms" in sheets and not sheets["tendencia_ms"].empty:
            ws = writer.sheets[sheet_refs["tendencia_ms"]]
            rows = len(sheets["tendencia_ms"])
            chart = workbook.add_chart({"type": "line"})
            chart.add_series({
                "name": "Media superior",
                "categories": [sheet_refs["tendencia_ms"], 1, 0, rows, 0],
                "values": [sheet_refs["tendencia_ms"], 1, 1, rows, 1],
                "line": {"color": "#0b4f66", "width": 2.25},
                "marker": {"type": "circle", "size": 6, "border": {"color": "#0b4f66"}, "fill": {"color": "#0b4f66"}},
            })
            chart.set_title({"name": "Tendencia histórica"})
            chart.set_x_axis({"name": "Año"})
            chart.set_y_axis({"name": "Tasa (%)"})
            chart.set_legend({"none": True})
            ws.insert_chart("E2", chart, {"x_scale": 1.15, "y_scale": 1.15})

        if "relaciones_modelo" in sheets and not sheets["relaciones_modelo"].empty:
            ws = writer.sheets[sheet_refs["relaciones_modelo"]]
            rows = len(sheets["relaciones_modelo"])
            chart = workbook.add_chart({"type": "bar"})
            chart.add_series({
                "name": "Estimación",
                "categories": [sheet_refs["relaciones_modelo"], 1, 0, rows, 0],
                "values": [sheet_refs["relaciones_modelo"], 1, 1, rows, 1],
                "fill": {"color": "#c12ca0"},
                "border": {"color": "#c12ca0"},
            })
            chart.set_title({"name": "Modelo exploratorio"})
            chart.set_x_axis({"name": "Coeficiente"})
            chart.set_y_axis({"reverse": True})
            chart.set_legend({"none": True})
            ws.insert_chart("F2", chart, {"x_scale": 1.15, "y_scale": 1.15})

        if "brecha_genero" in sheets and not sheets["brecha_genero"].empty:
            ws = writer.sheets[sheet_refs["brecha_genero"]]
            rows = len(sheets["brecha_genero"])
            chart = workbook.add_chart({"type": "bar"})
            chart.add_series({
                "name": "Brecha de género",
                "categories": [sheet_refs["brecha_genero"], 1, 0, rows, 0],
                "values": [sheet_refs["brecha_genero"], 1, 3, rows, 3],
                "fill": {"color": "#1e6a83"},
                "border": {"color": "#1e6a83"},
            })
            chart.set_title({"name": "Top 5 brecha de género"})
            chart.set_x_axis({"name": "pp"})
            chart.set_y_axis({"reverse": True})
            chart.set_legend({"none": True})
            ws.insert_chart("G2", chart, {"x_scale": 1.15, "y_scale": 1.15})

        if "metodologia" in sheets:
            ws = writer.sheets[sheet_refs["metodologia"]]
            ws.set_column(0, 1, 42)
            ws.write("D2", "Contenido del Excel", fmt_header)
            ws.write("D3", "Incluye las bases que alimentan cada gráfica del dashboard y, cuando xlsxwriter está disponible, agrega gráficas de apoyo dentro del mismo archivo.", fmt_note)

    return excel_path


def export_excel_report(
    report_dir: Path,
    datos_estados: pd.DataFrame,
    panorama_abandono: pd.DataFrame,
    tendencia_ms: pd.DataFrame,
    relaciones_modelo: pd.DataFrame,
    brecha_genero: pd.DataFrame,
    mapa_ive: pd.DataFrame,
    correlaciones: pd.DataFrame,
    resumen_modelos: pd.DataFrame,
    nota_recalculo: bool = False,
) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    excel_path = report_dir / "reporte_dashboard_completo.xlsx"
    metodologia = pd.DataFrame(
        {
            "componente": [
                "Regla de zona crítica",
                "Fórmula IVE",
                "Contenido exportado",
                "Lectura del modelo",
                "Fuente pobreza",
                "Fuente conectividad",
                "Fuente abandono",
                "Nota de consistencia",
            ],
            "detalle": [
                "IVE > 50",
                "(pobreza + sin internet) / 2",
                "Datos y hojas base de cada gráfica del dashboard",
                "Modelo exploratorio útil para priorización temprana",
                "CONEVAL 2022",
                "ENDUTIH 2023",
                "INEGI / SEP 2022-2023",
                "Se recalculó zonas críticas desde datos_estados.csv" if nota_recalculo else "Sin observaciones adicionales",
            ],
        }
    )

    sheets = {
        "datos_estados": datos_estados,
        "panorama_abandono": panorama_abandono,
        "tendencia_ms": tendencia_ms,
        "relaciones_modelo": relaciones_modelo,
        "brecha_genero": brecha_genero,
        "mapa_ive_estados": mapa_ive,
        "correlaciones": correlaciones,
        "resumen_modelos": resumen_modelos,
        "metodologia": metodologia,
    }

    try:
        import xlsxwriter  # noqa: F401
        return _xlsxwriter_report(excel_path, sheets)
    except Exception:
        pass

    try:
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            for sheet_name, df in sheets.items():
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
        return excel_path
    except Exception:
        pass

    return _write_xlsx_fallback(excel_path, sheets)
