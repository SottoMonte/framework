modules = {'flow': 'framework.service.flow',}

import sys
import json
import asyncio
import datetime
import xml.etree.ElementTree as ET
import os
from jinja2 import Template

if sys.platform == 'emscripten':
    import pyodide

    async def backend(method, url, headers, payload):
        if method == 'GET':
            response = await pyodide.http.pyfetch(url, method=method, headers=headers)
        else:
            payload = json.dumps(payload if isinstance(payload, dict) else {})
            response = await pyodide.http.pyfetch(url, method=method, headers=headers, body=payload)
        if response.status in [200, 201]:
            return {"state": True, "result": await response.json()}
        else:
            return {"state": False, "result": [], "remark": f"Request failed with status {response.status}"}
else:
    import aiohttp

    async def backend(method, url, headers, payload):
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, json=payload) as response:
                rr = await response.json()
                print(rr)
                if response.status in [200, 201]:
                    return {"state": True, "result": rr}
                else:
                    return {"state": False, "remark": f"Request failed with status {response.status}"}


class adapter():

    def __init__(self, **constants):
        self.config = constants.get('config', {})
        self.api_url = self.config.get('url', '')
        self.token = self.config.get('token', '')
        self.authorization = self.config.get('authorization', 'token')
        self.accept = self.config.get('accept', 'application/vnd.github+json')
        self.scheduled_jobs = []  # Configurazioni caricate da XML
        self.load_flow_config("src/application/action")

    @flow.asynchronous(outputs='transaction')
    async def load(self, *services, **constants):
        await self.event_loop()
        #return await self.actuate(**constants | {'method': 'PUT'})

    async def actuate(self, **constants):
        headers = {
            "Authorization": f"{self.authorization} {self.token}",
            "Accept": self.accept,
        }
        location = constants.get('location', '').replace('//', '/')
        method = constants.get('method', '')
        payload = constants.get('payload', {})
        url = f"{self.api_url}/{location}"
        return await backend(method, url, headers, payload)

    def load_cron_config2(self, xml_dir_path):
        """Legge e renderizza con Jinja2 tutti i file XML in una cartella"""
        #self.scheduled_jobs.clear()

        for filename in os.listdir(xml_dir_path):
            if filename.endswith('.xml'):
                filepath = os.path.join(xml_dir_path, filename)

                try:
                    # Carica il contenuto del file
                    with open(filepath, "r", encoding="utf-8") as file:
                        raw_template = file.read()

                    # Esegui rendering Jinja2 con le variabili
                    rendered_xml = Template(raw_template).render(**self.config)

                    # Fai parsing del contenuto XML
                    root = ET.fromstring(rendered_xml)

                    for job in root.findall('job'):
                        config = {
                            'weekday': int(job.findtext('day', default='-1')),
                            'hour': int(job.findtext('hour', default='-1')),
                            'minute': int(job.findtext('minute', default='-1')),
                            'url': job.findtext('url'),
                            'method': job.findtext('method', default='GET'),
                            'token': job.findtext('token'),
                            'headers': {},
                            'payload': {}
                        }

                        headers_elem = job.find('headers')
                        if headers_elem is not None:
                            for h in headers_elem.findall('header'):
                                config['headers'][h.attrib['name']] = h.text

                        payload_text = job.findtext('payload')
                        if payload_text:
                            try:
                                config['payload'] = json.loads(payload_text)
                            except json.JSONDecodeError:
                                config['payload'] = {}

                        if config['url'] and config['weekday'] >= 0:
                            self.scheduled_jobs.append(config)

                except Exception as e:
                    print(f"❌ Errore nel file {filepath}: {e}")
    
    def load_flow_config(self, xml_dir_path):
        """Carica tutti i file XML nella cartella e aggiunge i job definiti nei <case>"""
        self.scheduled_jobs.clear()

        for filename in os.listdir(xml_dir_path):
            if filename.endswith('.xml'):
                filepath = os.path.join(xml_dir_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        raw_template = file.read()

                    # Esegui il rendering del template
                    rendered_xml = Template(raw_template).render(**self.config)

                    # Parsing XML
                    root = ET.fromstring(rendered_xml)

                    for case_elem in root.findall('case'):
                        case_name = case_elem.attrib.get('name', 'unknown')
                        description = case_elem.findtext('description', '')

                        schedule_elem = case_elem.find('schedule')
                        action_elem = case_elem.find('action/https')

                        if schedule_elem is None or action_elem is None:
                            print(f"⚠️  Skipping case '{case_name}' - missing schedule or action.")
                            continue

                        job = {
                            'name': case_name,
                            'description': description,
                            'weekday': int(schedule_elem.findtext('day', '-1')),
                            'hour': int(schedule_elem.findtext('hour', '-1')),
                            'minute': int(schedule_elem.findtext('minute', '-1')),
                            'interval': schedule_elem.findtext('interval', 'weekly'),
                            'url': action_elem.findtext('url'),
                            'method': action_elem.findtext('method', 'GET'),
                            'headers': {},
                            'payload': {}
                        }

                        headers_elem = action_elem.find('headers')
                        if headers_elem is not None:
                            for header in headers_elem.findall('header'):
                                name = header.attrib.get('name')
                                value = header.text
                                if name:
                                    job['headers'][name] = value

                        payload_text = action_elem.findtext('payload')
                        if payload_text:
                            try:
                                job['payload'] = json.loads(payload_text)
                            except json.JSONDecodeError:
                                job['payload'] = {}

                        if job['url'] and job['weekday'] >= 0:
                            self.scheduled_jobs.append(job)

                except Exception as e:
                    print(f"❌ Errore caricando {filepath}: {e}")

    async def run_cron_jobs(self):
        now = datetime.datetime.now()
        for job in self.scheduled_jobs:
            print(job)
            if (now.weekday() == job['weekday']):
                #and now.hour == job['hour'] and now.minute == job['minute']
                headers = job['headers']
                headers["Authorization"] = f"Bearer {job['token']}"
                
                #print(f"[{now}] Eseguo job {job['method']} {job['url']}")
                await backend(job['method'], job['url'], headers, {})
                self.scheduled_jobs.remove(job)
            else:
                print("falso",now.weekday(),now.date())

    async def event_loop(self):
        while True:
            await self.run_cron_jobs()
            await asyncio.sleep(60)





'''import sys

if sys.platform == 'emscripten':
    import pyodide
    import json

    async def backend(method,url,headers,payload):
        match method:
            case 'GET':
                response = await pyodide.http.pyfetch(url, method=method, headers=headers)
            case _:
                if type(payload) == dict:
                    payload = json.dumps(payload)
                else:
                    payload = json.dumps({})
                response = await pyodide.http.pyfetch(url, method=method, headers=headers,body=payload)
        if response.status in [200, 201]:
            data = await response.json()
            print(data)
            return {"state": True, "result": data}
        else:
            return {"state": False, "result":[],"remark": f"Request failed with status {response.status}"}
                
else:
    import aiohttp
    import json

    #@flow.asynchronous
    async def backend(method,url,headers,payload):
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, json=payload) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    
                    return {"state": True, "result": data}
                else:
                    return {"state": False, "remark": f"Request failed with status {response.status}"}

class adapter():
    
    def __init__(self, **constants):
        self.config = constants['config']
        self.api_url = self.config['url']
        self.token = self.config['token']
        self.authorization = self.config['authorization'] if 'authorization' in self.config else 'token '
        self.accept = self.config['accept'] if 'accept' in self.config else 'application/vnd.github+json'

    @flow.asynchronous(outputs='transaction')
    async def load(self, *services, **constants):
        return await self.actuate(**constants | {'method': 'PUT'})

    async def actuate(self, **constants):
        print('request:',constants)
        headers = {
            "Authorization": f"{self.authorization} {self.token}",
            "Accept": self.accept,
        }
        location = constants.get('location','').replace('//','/')
        method = constants.get('method','')
        payload = constants.get('payload',{})
        url = f"{self.api_url}/{location}"

        #if payload and method == 'GET':
        #    url += '?' + urlencode(payload)
        
        ok = await backend(method,url,headers,payload)
        print('request:',constants,'output:',ok)
        return ok  
    
    @flow.asynchronous(outputs='transaction')
    async def activate(self,*services,**constants):
        return await self.actuate(**constants|{'method':'PUT'})

    @flow.asynchronous(outputs='transaction')
    async def deactivate(self,*services,**constants):
        pass

    @flow.asynchronous(outputs='transaction')
    async def calibrate(self,*services,**constants):
        pass

    @flow.asynchronous(outputs='transaction')
    async def status(self,*services,**constants):
        pass

    @flow.asynchronous(outputs='transaction')
    async def reset(self,*services,**constants):
        pass'''