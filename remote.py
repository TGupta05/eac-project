import speech_recognition as sr
import paramiko
from scp import SCPClient
import time

remote_start_time = time.time()

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname="172.20.10.2",username="tushitagupta",password="i8MyDog2!")
scp = SCPClient(client.get_transport())

scp.put("audio.npy", "audio.npy")
scp.put("sample_rate.npy", "sample_rate.npy")
scp.put("sample_width.npy", "sample_width.npy")

scp.get("audio.npy")
scp.get("sample_rate.npy")
scp.get("sample_width.npy")
remote_end_time = time.time()

print("Elapsed time for remote computation = " + str(remote_end_time-remote_start_time))