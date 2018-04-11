import os
import json
import csv
import math

########################################儲存Location經緯度##########################################################
latitude=[None for i in range(500)]#緯
longitude=[None for i in range(500)]#經

with open('location.json','r') as location_file:
    location_data=json.load(location_file)
    islan=0
    for n in location_data["location"]:
        for nn in location_data["location"][n]:
            if islan==0:
                latitude[int(n)]=nn
                islan=1
            else:
                longitude[int(n)]=nn
                islan=0
########################################儲存Location經緯度##########################################################

########################################儲存當前目錄檔案列表#######################################################
files=[]

for f in os.listdir('.'):
    if os.path.isfile(f):
        if (f!="getall.py" and f!="All.csv" and f!="location.json"):
            files.append(f)
########################################儲存當前目錄檔案列表#######################################################

########################################以寫入模式打開CSV##########################################################
with open('All.csv','w',newline='') as csv_file:
    thewriter=csv.writer(csv_file)
    thewriter.writerow(['rx_spreadFactor','rx_rssi','rx_loRaSNR','power','location','distance'])#寫入第一行 ─ 各欄位名稱
    #初始化各欄位變數
    temp_sf=""
    temp_rssi=""
    temp_snr=""
    temp_power=""
    temp_gate=""
    temp_location=""
    temp_distance=0
    glatitude=0
    glongitude=0
    sum_distance=[0,0,0]
    ava_distance=[0,0,0]
    sum_rssi=[0,0,0]
    ava_rssi=[0,0,0]
    sum_snr=[0,0,0]
    ava_snr=[0,0,0]
    file_name_temp="initial"
    file_name_count=[0,0,0]
    last_sf=""
    last_power=""
    for file in files:
        with open(file,'r') as json_data:#逐項以讀取模式打開檔案
            data=json.load(json_data)#JSON格式讀取
            temp_sf=data['rx_spreadFactor']
            temp_rssi=data['rx_rssi']
            temp_snr=data['rx_loRaSNR']
            temp_gate=data['gateway']
            temp_location=data['location']

            temp_power=file[file[28:].find("_")+29:file[28:].find("_")+29+file[ file[28:].find("_")+29:].find("_")]

            if data['gateway']=="00800000a00006d4":#取毒gateway經緯度
                glatitude=24.96715
                glongitude=121.18766
            elif data['gateway']=="00800000a0000a1c":
                glatitude=24.96822
                glongitude=121.19437
            elif data['gateway']=="00800000a0000ed1":
                glatitude=24.97154
                glongitude=121.19268

#############################################計算距離#################################################################
            #紀錄：glatitude,glongitude為float
            #紀錄：latitude[location],longitude[location]為字串
            #算出temp_distance
            a=math.fabs(glatitude-float(latitude[int(temp_location)]))
            b=math.fabs(glongitude-float(longitude[int(temp_location)]))
            sina=math.sin(math.radians(a/2))
            sin2a=math.pow(sina,2)
            sinb=math.sin(math.radians(b/2))
            sin2b=math.pow(sinb,2)
            cos1=math.cos(math.radians(glatitude))
            cos2=math.cos(math.radians(float(latitude[int(temp_location)])))
            sqrtup=math.sqrt(sin2a+cos1*cos2*sin2b)
            arcsin=math.asin(sqrtup)
            temp_distance=2*arcsin*6378137

#############################################計算距離#################################################################

            if file[0:len(file)-6]!=file_name_temp:#計算平均值
                if file_name_temp!="initial":
                    #寫入檔案資訊
                    if file_name_count[0]!=0:
                        ava_distance[0]=sum_distance[0]/file_name_count[0]
                        ava_rssi[0]=sum_rssi[0]/file_name_count[0]
                        ava_snr[0]=sum_snr[0]/file_name_count[0]
                        thewriter.writerow([last_sf,ava_rssi[0],ava_snr[0],last_power,temp_location,ava_distance[0]])
                    if file_name_count[1]!=0:
                        ava_distance[1]=sum_distance[1]/file_name_count[1]
                        ava_rssi[1]=sum_rssi[1]/file_name_count[1]
                        ava_snr[1]=sum_snr[1]/file_name_count[1]
                        thewriter.writerow([last_sf,ava_rssi[1],ava_snr[1],last_power,temp_location,ava_distance[1]])
                    if file_name_count[2]!=0:
                        ava_distance[2]=sum_distance[2]/file_name_count[2]
                        ava_rssi[2]=sum_rssi[2]/file_name_count[2]
                        ava_snr[2]=sum_snr[2]/file_name_count[2]
                        thewriter.writerow([last_sf,ava_rssi[2],ava_snr[2],last_power,temp_location,ava_distance[2]])

                    sum_rssi=[0,0,0]
                    sum_snr=[0,0,0]
                    sum_distance=[0,0,0]
                    file_name_count=[0,0,0]



                if data['gateway']=="00800000a00006d4":#取毒gateway經緯度
                    sum_rssi[0]+=int(temp_rssi)
                    sum_snr[0]+=float(temp_snr)
                    sum_distance[0]+=temp_distance
                    file_name_count[0]+=1
                elif data['gateway']=="00800000a0000a1c":
                    sum_rssi[1]+=int(temp_rssi)
                    sum_snr[1]+=float(temp_snr)
                    sum_distance[1]+=temp_distance
                    file_name_count[1]+=1
                elif data['gateway']=="00800000a0000ed1":
                    sum_rssi[2]+=int(temp_rssi)
                    sum_snr[2]+=float(temp_snr)
                    sum_distance[2]+=temp_distance
                    file_name_count[2]+=1

                file_name_temp=file[0:len(file)-6]
                last_power=temp_power
                last_sf=temp_sf
            else:
                if data['gateway']=="00800000a00006d4":#取毒gateway經緯度
                    sum_rssi[0]+=int(temp_rssi)
                    sum_snr[0]+=float(temp_snr)
                    sum_distance[0]+=temp_distance
                    file_name_count[0]+=1
                elif data['gateway']=="00800000a0000a1c":
                    sum_rssi[1]+=int(temp_rssi)
                    sum_snr[1]+=float(temp_snr)
                    sum_distance[1]+=temp_distance
                    file_name_count[1]+=1
                elif data['gateway']=="00800000a0000ed1":
                    sum_rssi[2]+=int(temp_rssi)
                    sum_snr[2]+=float(temp_snr)
                    sum_distance[2]+=temp_distance
                    file_name_count[2]+=1



    #寫入檔案資訊
    if file_name_count[0]!=0:
        ava_distance[0]=sum_distance[0]/file_name_count[0]
        ava_rssi[0]=sum_rssi[0]/file_name_count[0]
        ava_snr[0]=sum_snr[0]/file_name_count[0]
        thewriter.writerow([last_sf,ava_rssi[0],ava_snr[0],last_power,temp_location,ava_distance[0]])
    if file_name_count[1]!=0:
        ava_distance[1]=sum_distance[1]/file_name_count[1]
        ava_rssi[1]=sum_rssi[1]/file_name_count[1]
        ava_snr[1]=sum_snr[1]/file_name_count[1]
        thewriter.writerow([last_sf,ava_rssi[1],ava_snr[1],last_power,temp_location,ava_distance[1]])
    if file_name_count[2]!=0:
        ava_distance[2]=sum_distance[2]/file_name_count[2]
        ava_rssi[2]=sum_rssi[2]/file_name_count[2]
        ava_snr[2]=sum_snr[2]/file_name_count[2]
        thewriter.writerow([last_sf,ava_rssi[2],ava_snr[2],last_power,temp_location,ava_distance[2]])
