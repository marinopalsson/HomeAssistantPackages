Til að setja upp NÆSTI STRÆTÓ þarf að gera tvennt:

1. Kópera skrárnar á réttan stað, Þær þurfa að fara undir custom_components/naesti_straeto í config möppunni.
2. Endurræsa Home Assistant
3. Setja upp sensor fyrir hvern strætó sem fylgjast skal með í configuration.yaml (eða þar sem þið eruð með ykkar sensors).
4. Endurræsa Home Assistant
5. Setja skynjarana upp í Lovelace og njóta

---
## Staðsetning skráanna
```
/config
  └── custom_components
      └── naesti_straeto
          ├── __init__.py
          ├── api.py
          ├── manifest.json
          ├── README.md
          ├── stops.json
          └── sensor.py
```
---
## Skynjararnir
Dæmi um sensor uppsetningu í configuration.yaml:

```yaml
sensor:
  - platform: naesti_straeto
    busstop_id: 16040622
    bus_line: "15"
    stop_data_file_path: "custom_components/naesti_straeto/stops.json"
```

Þarna þarf að skipta út busstop_id og bus_line

busstop_id:

Í stops.json skránni er hægt að finna lista yfir allar stoppistöðvar. Þar þarf að finna þá stoppistöð sem fylgjast skal með og er _**stop_id**_ gildið sem setja skal í _**busstop_id**_

bus_line:

Númer strætósins sem fylgjast skal með.

---
## Lovelace
Lovelace kortið gæti verið svona:
```yaml
type: entities
entities:
  - entity: sensor.straeto_15_16040613
    name: Strætó 15
```
þar sem ykkar sensor væri `sensor.straeto_{bus_line}_{busstop_id}`