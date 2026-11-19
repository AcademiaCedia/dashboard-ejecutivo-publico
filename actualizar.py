"""Genera el HTML público a partir de la extracción privada preparada por Academia."""
import argparse
import json
from html import escape
from pathlib import Path

def number(value):
    return f"{value:,.2f}".translate(str.maketrans(",.",".,"))

def money(value):
    return "USD " + number(value)

def card(name, value, detail):
    return f'<div class="card"><label>{name}</label><strong>{value}</strong><small>{detail}</small></div>'

def render(data):
    totals = data["totals"]
    groups = data["groups"]
    package = groups["PAQUETE"]["values"]
    outside = [round(sum(groups[g]["values"][i] or 0 for g in ("BD","SERVICIOS A OTRAS AREAS","PROYECTOS")),2) for i in range(2)]
    for i in range(2):
        if abs(totals[i]-package[i]-outside[i]) > 0.011:
            raise ValueError("Revise la conciliación financiera.")
    summary = card("Ingresos totales · 2026",money(totals[1]),"2025 · "+money(totals[0])) + card("Fuera del paquete · 2026",money(outside[1]),"2025 · "+money(outside[0]))
    delta=outside[1]-outside[0]
    summary += card("Variación fuera del paquete",money(delta),number(100*delta/outside[0])+" % frente a 2025" if outside[0] else "Sin base para calcular la variación")
    comparison = "".join(f"<tr><td>{year}</td><td>{money(package[i])}</td><td>{money(outside[i])}</td><td>{number(100*outside[i]/totals[i])} %</td></tr>" for i,year in enumerate((2025,2026)))
    segments=[]
    for key, title in (("PAQUETE UNIVERSIDADES","Paquete Universidades"),("PAQUETE COLEGIOS","Paquete Colegios")):
        members=[row[3] for row in data["members"] if row[0]==key]
        counts=[]
        for service in data["packages"][key]:
            values=[member[service] for member in members]
            count=sum(v=="Utiliza" or isinstance(v,(float,int)) and v>0 for v in values)
            counts.append((service,count))
        bars=""
        for name,count in sorted(counts,key=lambda x:-x[1]):
            percent=100*count/len(members) if members else 0
            bars+=f'<div class="bar"><div class="cap"><span>{escape(name)}</span><b>{count} de {len(members)} · {number(percent)} %</b></div><div class="track"><span class="ink" style="width:{percent:.2f}%"></span></div></div>'
        segments.append(f'<article data-segment><h3>{title}</h3><p class="desc">{len(members)} instituciones en el segmento</p>{bars}</article>')
    offers=[r[2] for r in data["deals"] if r[0]=="EN NEGOCIACIÓN"]
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Dashboard ejecutivo público · Academia CEDIA</title><link rel="stylesheet" href="assets/estilo.css"><script defer src="assets/navegacion.js"></script></head><body>
<header><div class="wrap head"><img alt="CEDIA" src="assets/cedia.png"><span>Academia / Dirección Ejecutiva</span></div></header><main class="wrap"><div class="hero"><div><small>ACADEMIA CEDIA</small><h1>Dashboard ejecutivo</h1></div></div>
<nav aria-label="Vistas del dashboard"><button aria-controls="resumen" aria-current="true">Resumen financiero</button><button aria-controls="uso">Uso de servicios</button><button aria-controls="ingresos">Ingresos fuera del paquete</button></nav>
<section id="resumen"><h2>Resumen financiero</h2><div class="cards">{summary}</div><article><h3>Composición de los ingresos</h3><div class="tablewrap"><table><thead><tr><th>Año</th><th>Paquete institucional</th><th>Fuera del paquete</th><th>Participación fuera del paquete</th></tr></thead><tbody>{comparison}</tbody></table></div></article><p class="note">Fuera del paquete suma BD, Servicios a otras áreas y Proyectos. La fuente no especifica las fechas de corte de los periodos comparados.</p></section>
<section id="uso" hidden><h2>Uso de servicios</h2><div class="filters"><label>Segmento<select id="segmento"><option>Ambos paquetes</option><option>Paquete Universidades</option><option>Paquete Colegios</option></select></label></div><div class="grid">{''.join(segments)}</div><p class="note">Cada barra muestra la proporción de instituciones del segmento con uso documentado del servicio. El paquete Universidades incluye distintos tipos de miembros. La matriz de uso carece de fecha de corte.</p></section>
<section id="ingresos" hidden><h2>Ingresos fuera del paquete · 2026</h2><article class="portfolio"><h3>Cartera en negociación</h3><div class="portfolio-metrics"><div><span>Valor total de las ofertas</span><strong>{money(sum(offers))}</strong></div><div><span>Ofertas en negociación</span><strong>{len(offers)}</strong></div></div><p>Estas ofertas están pendientes de cierre y se excluyen de los ingresos registrados.</p></article><div class="cards">{card("Ingresos fuera del paquete",money(outside[1]),number(100*outside[1]/totals[1])+" % del total registrado en 2026")}</div></section>
<footer>Fuente · Revisión dirección ejecutiva <span>Academia CEDIA</span></footer></main></body></html>'''

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extraccion_privada",type=Path)
    args=parser.parse_args()
    raw=args.extraccion_privada.read_text(encoding="utf-8")
    data=json.loads(raw.removeprefix("const DATA = ").strip().removesuffix(";"))
    Path(__file__).with_name("index.html").write_text(render(data),encoding="utf-8")
