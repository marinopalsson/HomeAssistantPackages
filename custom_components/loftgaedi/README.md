# Loftgæði

Þessi viðbót skoðar gögn frá valinni loftgæðastöð, ber saman gögnin við loftgæðavísi fyrir hvert mengunarefni og skilar hæsta/versta loftgæðavísinum fyrir stöðina á hverjum tímapunkti.

Dæmi: Ef SO2 mælist 400 µg/m3
 og PM10 mælist 120 µg/m3
, þá skilar þessi viðbót að loftgæðin séu "Óholl" vegna PM10 mælingarinnar.

| Loftgæðavísir  | Svifryk (PM2,5) | Svifryk (PM10) | Köfnunarefnisdíoxíð (NO2) | Brennisteinsdíoxíð (SO2) | Brennisteinsvetni (H2S) |
|--------------------------------------------------|-----------------|---------------------------|-------------------------|-------------------------|-----|
| Mjög góð                                         | 0               | 0                         | 0                       | 0                       | 0   |
| Góð                                              | 10              | 25                        | 50                      | 20                      | 25  |
| Sæmileg                                          | 15              | 50                        | 75                      | 350                     | 50  |
| Óholl fyrir viðkvæma                             | 25              | 75                        | 150                     | 600                     | 75  |
| Óholl                                            | 50              | 100                       | 200                     | 2600                    | 100 |

En hægt er að smella á skynjarann og sjá sundurliðun á gildunum eftir mengunarefnum.

Gögnin eru fengið frá Umhverfisstofnun og er vert að taka það fram að þetta eru óyfirfarin gögn. Umhverfisstofnun uppfærir flest gögnin á klukkustundarfresti (uþb 17 mínútur yfir heila tímann) svo ég sæki ný gögn sjálfur frá þeim 20 mínútur yfir.

Mælarnir eru ekki allir að mæla sömu mengunarefnin en ég skoða efnin í töfluni hér að ofan ef þau eru í boði.

Til að setja upp _**Loftgæði**_ þarf að gera þrennt. Ég mæli með að endurræsa eftir skref 1 og 2:

1. Koma skránum fyrir á réttan stað. Hér er annað hvort hægt að: 
   * Afrita skrárnar á réttan stað. þær þurfa að fara undir custom_components/loftgaedi í config möppunni.
   * Ef þú ert með HACS installað, þá er hægt að fara í það og setja inn **Custom repository**. Setja `https://github.com/marinopalsson/HomeAssistantPackages/tree/main/custom_components/loftgaedi` í _Repository_ reitinn og Integration i _Category_
2. Setja upp sensor fyrir hverja loftgæðastöð sem fylgjast skal með í configuration.yaml (eða þar sem þið eruð með ykkar sensors).
3. Setja skynjarana upp í Lovelace og njóta


---
## Staðsetning skráanna
```
/config
  └── custom_components
      └── loftgaedi
          ├── __init__.py
          ├── api.py
          ├── manifest.json
          ├── README.md
          ├── pollutant_levels.json
          └── sensor.py
```
---
## Skynjararnir
Dæmi um sensor uppsetningu í configuration.yaml:

```yaml
sensor:
  - platform: loftgaedi
    name: loftgaedi_grensas
    station_id: STA-IS0005A
```

Þarna þarf að skipta út **station_id** og **name**

Nafn skynjarans fer í  _**name**_. Takið eftir að ykkur er frjálst að skýra skynjarann hvað sem er, en ef þið ætlið að hafa fleiri en einn mæli þá er gott að hafa staðsetningu mælisins inni í nafninu.

Í [stodvar_listi.md](https://github.com/marinopalsson/HomeAssistantPackages/tree/main/custom_components/loftgaedi/stodvar_listi/stodvar_listi.md) skránni er að finna lista yfir allar loftgæðastöðvarnar. Þar þarf að finna þá stöð sem fylgjast skal með afrita _**stöðvarnúmer**_ gildið í _**station_id**_. Til að gera sér betur grein fyrir stöðvunum sem eru í boði er gott að skoða https://loftgaedi.is

---
## Lovelace
Lovelace kortið gæti verið svona:
```yaml
type: entities
entities:
  - entity: sensor.loftgaedi_grensas
    name: Loftgæði Grensás
```
