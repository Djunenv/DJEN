import asyncio
import re
import redis
import json  
from communex._common import get_node_url
from communex.client import CommuneClient
from fastapi import FastAPI, File, UploadFile, Form, Depends
from pydantic import BaseModel, Field
from typing import Optional
from communex.module import Module, endpoint
from communex.module.client import ModuleClient
from substrateinterface import Keypair
from communex.compat.key import classic_load_key 

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


node_url = get_node_url(use_testnet=True)
client = CommuneClient(node_url)


class WasteReport(BaseModel):
    description: str
    location: str
    Waste_type: str
    timestamp: str
    file_data: str
    additional_details: Optional[str] = None


class Validator(Module):
    @endpoint
    def report_Waste(self, report: WasteReport):
        
        combined_mapping = redis_client.get('combined_mapping')
        
        if combined_mapping is None:
            print("Cache miss: Generating combined mapping.")
            asyncio.run(get_combined_mapping())  

            combined_mapping = redis_client.get('combined_mapping')

        if combined_mapping is not None:
            combined_mapping = json.loads(combined_mapping)
            print(combined_mapping)
            selected_entry = combined_mapping.get("1")
            if selected_entry:
                key = selected_entry.get("key")
                address = selected_entry.get("address")

                ip, port = address.split(":")

                port = int(port)

                print(f"Key: {key}")
                print(f"IP: {ip}")
                print(f"Port: {port} (as integer)")
                KeyPair:Keypair=classic_load_key("djen")
                print(KeyPair)
                client = ModuleClient(ip, port, KeyPair)
                response =asyncio.run(client.call("mine_Waste", key, {
                    "prompt":"It is Waste data"
                }, timeout=1000))
                print(f"Response from miner: {response}")
                return response
            else:
                print("Entry not found for index 1.")

        print(f"Received Report: {report}")
        
        return {"status": "success", "message": "Waste report received!"}

async def get_keys():
    return await asyncio.to_thread(client.query_map_key, 59)

async def get_addresses():
    return await asyncio.to_thread(client.query_map_address, 59)

async def get_names():
    return await asyncio.to_thread(client.query_map_name, 59)

def is_valid_address(address):
    ipv4_pattern = r'^\d{1,3}(\.\d{1,3}){3}(:\d{1,5})?$'
    url_pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(:\d{1,5})?$'
    return bool(re.match(ipv4_pattern, address)) or bool(re.match(url_pattern, address))

async def get_combined_mapping():
    keys, addresses, names = await asyncio.gather(get_keys(), get_addresses(), get_names())
    
    combined_mapping = {}
    
    for index in keys:
        name = names.get(index, '')
        address = addresses.get(index, 'None:None')
        
        if name.startswith('miner::') and is_valid_address(address):
            combined_mapping[index] = {'name': name, 'key': keys[index], 'address': address}
    
    print(json.dumps(combined_mapping))
    redis_client.set('combined_mapping', json.dumps(combined_mapping)) 
    print("Combined mapping cached in Redis")

asyncio.run(get_combined_mapping())
