1) Init db with schema.sql (or use existing)
2) Run pipenv shell && pipenv install
3) Run python parse_xml.py - to emulate request (or use existing)
4) Run python server.py


В папке два XML – это ответы на поисковые запросы.
В ответах лежат варианты перелётов (тег `Flights`) со всей необходимой информацией,
чтобы отобразить билет.

На основе этих данных, нужно сделать вебсервис,
в котором есть эндпоинты, отвечающие на следующие запросы:

* Какие варианты перелёта из DXB в BKK? 
curl -X GET http://127.0.0.1:8080/?dest=BKK&source=DXB
* Самый дорогой/дешёвый (cond=expensive/cheap), быстрый/долгий (cond=fast/long) и оптимальный варианты (cond=opt)
curl -X GET http://127.0.0.1:8080/top?cond=fast&dest=BKK&source=DXB
* В чём отличия между результатами двух запросов (изменение маршрутов/условий)?
many/single

Формат ответа: `json`
