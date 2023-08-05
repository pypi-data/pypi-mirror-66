'''
URAPY stands for

U - Uptime
R - Robot
APY - Like API but cheesier (get it? API? APY? Ok...)

Literally with no dependencies how cool is that
'''


import json
import html
import requests


PREFIXES = ('https://', 'http://')

class MonitorNotFound(Exception):
  pass

class InvalidURL(Exception):
  pass

class APIError(Exception):
  pass

class PSPNotFound(Exception): 
  pass

class EditError(Exception):
  pass




class Client:
  def __init__(self, secret):
    self.base = 'https://api.uptimerobot.com/v2/'
    self.secret = secret
    self.headers = {
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded"
    }

  
  def get_api(self, url, payload):
    return json.loads(html.unescape(requests.request('POST', url, data=payload, headers=self.headers).text))

  def get_account_details(self):
    url = self.base + 'getAccountDetails'
    payload = f'api_key={self.secret}&format=json'
    response = self.get_api(url, payload)
    if self.response_ok(response):
      return response['account']
    else:
      raise APIError(response['error']['message'].title())

  def response_ok(self, response):
    return response['stat'] == 'ok'
  
  def get_monitor(self, friendly):
    return Monitor(self, friendly)
  
  def get_psp(self, friendly):
    return PSP(self, friendly)
  
  def new_monitor(self, friendly, target_url, interval=5, no_cache=False): 
    '''Only supports creating HTTP(S) monitors'''
    interval *= 60
    if not target_url.startswith(PREFIXES):
      raise InvalidURL('The given URL is invalid.')
    
    if no_cache:
      target_url += '?*cachebuster*'

    url = self.base + 'newMonitor'
    payload  = f'api_key={self.secret}' # Welp quarintine is killing me
    payload += '&format=json'
    payload += '&type=1'
    payload += f'&url={target_url}'
    payload += f'&friendly_name={friendly}'
    payload += f'&interval={interval}'
    response = self.get_api(url, payload)
    if self.response_ok(response):
      return response
    else:
      raise APIError(response['error']['message'].title())
  
  def delete_monitor(self, friendly):
    id = self.get_monitor(friendly).id
    url = self.base + 'deleteMonitor'
    payload = '&format=json'
    payload += f'&api_key={self.secret}'
    payload += f'&id={id}'
    response = self.get_api(url, payload)

    if self.response_ok(response):
      return response
    else:
      raise APIError(response['error']['message'].title())


  def new_psp(self, friendly, monitors=[], password=None):
    ids = []
    for items in monitors:
      ids.append(str(self.get_monitor(items).id))
    
    if ids != []:
      ids = '-'.join(ids)
    else:
      ids = '0'
    
    url = self.base + 'newPSP'

    payload = 'format=json'
    payload += f'&api_key={self.secret}'
    payload += '&type=1'
    payload += f'&friendly_name={friendly}'
    payload += f'&monitors={ids}'
    
    if password != None:
      payload += f'&password={password}'
    
    response = self.get_api(url, payload)
    if self.response_ok(response):
      return response
    else:
      raise APIError(response['error']['message'].title())

  def delete_psp(self, friendly):
    id = self.get_psp(friendly).id
    
    url = self.base + 'deletePSP'

    payload = f'format=json&api_key={self.secret}'
    payload += f'&id={id}'

    response = self.get_api(url, payload)

    if self.response_ok(response):
      return response
    else:
      raise APIError(response['error']['message'])



class Monitor:
  def __init__(self, client, friendly):
    if not isinstance(client, Client):
      raise TypeError(f'Excepted {Client}, received {type(client)}')
    self.friendly = friendly
    self.client = client
    self.id = None
    #print(json.loads(requests.request('POST', self.base + 'getMonitors', data=f"api_key={self.secret}&format=json", headers=self.headers).text))

    for items in self.client.get_api(self.client.base + 'getMonitors', f"api_key={self.client.secret}&format=json")['monitors']:
      if items['friendly_name'] == self.friendly:
        self.id = items['id']
    if self.id == None:
      raise MonitorNotFound('Monitor Not Found')
  
  def get_stats(self):
    url = self.client.base + 'getMonitors'
    payload = f'api_key={self.client.secret}&monitors={self.id}&format=json'
    response = self.client.get_api(url, payload)
    if self.client.response_ok(response):
      return response['monitors'][0]
    else:
      raise APIError(response['error']['message'].title())
  
  def get_logs(self):
    url = self.client.base + 'getMonitors'
    payload = f'api_key={self.client.secret}&monitors={self.id}&logs=1&format=json'
    raw = self.client.get_api(url, payload)
    if self.client.response_ok(raw):
      return raw['monitors'][0]['logs']
    else:
      raise APIError(raw['error']['message'].title())
  

  
  def edit(self, friendly=None, target_url=None, interval=None, pause=None):

    if not (friendly or target_url or interval or pause):
      raise EditError('You need to supply at least one field to change')

    if pause == True: pause=0
    elif pause == False: pause=1
    elif pause == None: pass
    else: raise TypeError(f'Pause must be a boolean, not {type(pause)}')

    if not isinstance(interval, int) and interval != None: raise TypeError(f'Interval must be an int, not {type(interval)}')

    url = self.client.base + 'editMonitor'

    payload = f'api_key={self.client.secret}'
    payload += f'&format=json&id={self.id}'

    if friendly:
      payload += f'&friendly_name={friendly}'

    if target_url:

      if not target_url.startswith(('https://', 'http://')):
        raise InvalidURL('The given URL is invalid.')

      payload += f'&url={target_url}'

    
    if interval:
      interval *= 60
      payload += f'&interval={interval}'
    
    if pause != None:
      payload += f'&status={pause}'
    
    response = self.client.get_api(url, payload)

    if self.client.response_ok(response):
      return response
    else:
      raise APIError(response['error']['message'].title())
  



class PSP:
  def __init__(self, client, friendly):
    self.friendly = friendly
    self.client = client
    self.id = None
    for items in self.client.get_api(self.client.base + 'getPSPs', f'api_key={self.client.secret}&format=json')['psps']:
      if items['friendly_name'] == friendly:
        self.id = items['id']

    if self.id == None:
      raise PSPNotFound('PSP Not Found.')
  

  def get_stats(self):
    url = self.client.base + 'getPSPs'

    payload = f'api_key={self.client.secret}'
    payload += '&format=json'
    payload += f'&psps={self.id}'

    response = self.client.get_api(url, payload)
    if self.client.response_ok(response):
      return response
    else:
      raise APIError(response['error']['message'].title())
  
  def edit(self, friendly=None, target_url=[], password=None):
    if not (friendly or target_url or password):
      raise EditError('You need to supply at least one field to change')
    
    ids = []
    for items in target_url:
      ids.append(str(self.client.get_monitor(items).id))
    
    url = self.client.base + 'editPSP'

    payload = f'format=json&api_key={self.client.secret}'
    payload += f'&id={self.id}'

    if friendly != None:
      payload += f'&friendly_name={friendly}'
    
    if ids != []:
      ids = '-'.join(ids)
    
    if ids == []: # Because Uptime Robot API requires the id parameter, we need to get the ids from the previous psp. smh 
      ids = '-'.join(str(i) for i in self.get_stats()['psps'][0]['monitors'])

    payload += f'&monitors={ids}'
    
    if password != None:
      payload += f'&password={password}'
    
    response = self.client.get_api(url, payload)
    if self.client.response_ok(response):
      return response
    else:
      raise APIError(response['error']['message'].title())
