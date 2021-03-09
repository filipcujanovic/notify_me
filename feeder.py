import requests
import demoji
from bs4 import BeautifulSoup
from src.models.models import Bus
from src.models.models import Municipality

url = "https://www.busevi.com/wp-admin/admin-ajax.php"

payload="action=vc_get_vc_grid_data&vc_action=vc_get_vc_grid_data&tag=vc_basic_grid&data%5Bvisible_pages%5D=5&data%5Bpage_id%5D=67518&data%5Bstyle%5D=all&data%5Baction%5D=vc_get_vc_grid_data&data%5Bshortcode_id%5D=1614781682063-e72c8a85-c894-9&data%5Btag%5D=vc_basic_grid&vc_post_id=67518&_vcnonce=ee4672782d"
headers = {
  'authority': 'www.busevi.com',
  'accept': 'text/html, */*; q=0.01',
  'x-requested-with': 'XMLHttpRequest',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'sec-gpc': '1',
  'origin': 'https://www.busevi.com',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.busevi.com/gradski-prevoz-beograd-autobuske-linije-brojevi-linija/',
  'accept-language': 'en-US,en;q=0.9',
  'cookie': '__cfduid=d0f378334d3daf7b8a177b847da524d041613471454'
}

response = requests.request("POST", url, headers=headers, data=payload).text
data = BeautifulSoup(response, 'html.parser')

bus_routes = data.find_all('div', {'class': 'linija'})

payload="action=vc_get_vc_grid_data&vc_action=vc_get_vc_grid_data&tag=vc_basic_grid&data%5Bvisible_pages%5D=5&data%5Bpage_id%5D=65711&data%5Bstyle%5D=all&data%5Baction%5D=vc_get_vc_grid_data&data%5Bshortcode_id%5D=1609576187901-b768d395-3633-10&data%5Btag%5D=vc_basic_grid&vc_post_id=65711&_vcnonce=ee4672782d"

response = requests.request("POST", url, headers=headers, data=payload).text
data = BeautifulSoup(response, 'html.parser')

bus_routes = data.find_all('div', {'class': 'linija'}) + bus_routes

payload="action=vc_get_vc_grid_data&vc_action=vc_get_vc_grid_data&tag=vc_basic_grid&data%5Bvisible_pages%5D=5&data%5Bpage_id%5D=65715&data%5Bstyle%5D=all&data%5Baction%5D=vc_get_vc_grid_data&data%5Bshortcode_id%5D=1609576237746-3a6d7d0e-f656-4&data%5Btag%5D=vc_basic_grid&vc_post_id=65715&_vcnonce=ee4672782d"

response = requests.request("POST", url, headers=headers, data=payload).text
data = BeautifulSoup(response, 'html.parser')

bus_routes = data.find_all('div', {'class': 'linija'}) + bus_routes


for bus_route in bus_routes:
    bus_route_number = bus_route.get_text().strip()
    bus = Bus.where('bus_route_number' , '=' , bus_route_number).first()
    if bus is None:
      bus = Bus()
      bus.bus_route_number = bus_route_number
      bus.save()

municipalities = ['Чукарица','Нови Београд','Палилула','Раковица','Савски венац','Стари град','Вождовац','Врачар','Земун','Звездара','Барајево','Гроцка','Лазаревац','Младеновац','Обреновац','Сопот','Сурчин']

for municipality_name in municipalities:
    municipality = Municipality.where('name' , '=', municipality_name).first()
    if municipality is None:
      municipality = Municipality()
      municipality.name = municipality_name
      municipality.save()

demoji.download_codes()