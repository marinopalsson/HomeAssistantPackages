# Næsti strætó

Til að setja upp _**Næsti strætó**_ þarf að gera þrennt. Ég mæli með að endurræsa eftir skref 1 og 2:

1. Koma skránum fyrir á réttan stað. Hér er annað hvort hægt að: 
   * Afrita skrárnar á réttan stað. þær þurfa að fara undir custom_components/naesti_straeto í config möppunni.
   * Ef þú ert með HACS installað, þá er hægt að fara í það og setja inn **Custom repository**. Setja `https://github.com/marinopalsson/HomeAssistantPackages/tree/main/custom_components/naesti_straeto` í _Repository_ reitinn og Integration i _Category_
2. Setja upp sensor fyrir hvern strætó sem fylgjast skal með í configuration.yaml (eða þar sem þið eruð með ykkar sensors).
3. Setja skynjarana upp í Lovelace og njóta


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

Þarna þarf að skipta út **busstop_id** og **bus_line**

Númer strætósins fer í _**bus_line**_

Í stops.json skránni er hægt að finna lista yfir allar stoppistöðvar. Þar þarf að finna þá stoppistöð sem fylgjast skal með og er _**stop_id**_ gildið sem setja skal í _**busstop_id**_

Í flestum tilfellum eru tvær stoppistöðvar með sama nafn, því þær eru sitthvoru megin við götuna. Til að finna út hvor þeirra er sú sem þú ert að leita að er hægt að setja inn gps hnitin í google maps, eða fara á þessa slóð:</br>
`https://data01.straeto.is/data/dyn-data/s/90000175.json`
</br>
skipta út 90000175 fyrir stop_id á stöðinni sem þú ert að skoða. Finna strætónúmerið sem þú hefur áhuga á og skoða "til" reitinn fyrir þann strætó.

---
## Lovelace
Lovelace kortið gæti verið svona:
```yaml
type: entities
entities:
  - entity: sensor.straeto_15_16040613
    name: Strætó 15
```
þar sem þinn sensor væri `sensor.straeto_{bus_line}_{busstop_id}`