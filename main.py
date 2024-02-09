import requests
from bs4 import BeautifulSoup
import pandas
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import glob
import json

sns = glob.glob('github/sne-2020-2024-main/*.json')
data = []
no_redshift = 0
no_mag = 0
no_band = 0

for sn_path in sns:
	if sn_path.startswith('github/sne-2020-2024-main\\SN'):

		name = sn_path.split('\\')[-1].split('.')[-2]
		with open(sn_path, 'r') as f:
			sn = json.load(f)
		try:
			mag = float(sn[name]['maxappmag'][0]['value'])
			absmag = float(sn[name]['maxabsmag'][0]['value'])
			band = sn[name]['maxband'][0]['value']
			redshift = float(sn[name]['redshift'][0]['value'])
		except:
			no_mag += 1
			continue
		if band != "B":
			continue
		iaTrue = False
		for snType in sn[name]['claimedtype']:
			if snType['value'] == "Ia":
				iaTrue = True
		if not iaTrue:
			continue

		rs_error = 10**-int(len(sn[name]['redshift'][0]['value'].split(".")[-1]))
		app_error = 10**-int(len(sn[name]['maxappmag'][0]['value'].split(".")[-1]))
		abs_error = 10**-int(len(sn[name]['maxabsmag'][0]['value'].split(".")[-1]))
		Mm = mag - absmag
		distance = (10.**((Mm+5.)/5.))/1000000.
		distance_error = np.log(10.)*distance*((app_error+abs_error)/5.)
		velocity = redshift*300000.
		velocity_error = rs_error*300000.
		'''
		x.append(distance)
		y.append(velocity)
		'''
		data.append({
			'name':name,
			'redshift':redshift,
			'redshift_error':rs_error,
			'absmag':absmag,
			'absmag_error':abs_error,
			'appmag':mag,
			'appmag_error':app_error,
			'M-m':Mm,
			'distance':distance,
			'distance_error':distance_error,
			'velocity':velocity,
			'velocity_error':velocity_error
		})

print(no_mag)

df = pd.DataFrame(data) 
df.to_csv("hubble_constant_B.csv", index=False)

'''
url = 'https://www.wiserep.org/search/spectra?&name=&name_like=0&public=all&inserted_period_value=1&inserted_period_units=years&type%5B%5D=3&type_family%5B%5D=null&instruments%5B%5D=null&spectypes%5B%5D=10&qualityid%5B%5D=null&groupid%5B%5D=null&spectra_count=&redshift_min=&redshift_max=&obsdate_start%5Bdate%5D=2023-10-01&obsdate_end%5Bdate%5D=2023-11-01&spec_phase_min=&spec_phase_max=&spec_phase_unit=days&phase_types%5B%5D=null&filters%5B%5D=null&methods%5B%5D=null&wl_min=&wl_max=&obj_ids=&spec_ids=&ids_or=0&reporters=&publish=&contrib=&last_modified_start%5Bdate%5D=&last_modified_end%5Bdate%5D=&last_modified_modifier=&creation_start%5Bdate%5D=&creation_end%5Bdate%5D=&creation_modifier=&show_aggregated_spectra=1&show_all_spectra=0&table_phase_name=40&num_page=250&display%5Bobj_rep_internal_name%5D=1&display%5Bobj_type_family_name%5D=0&display%5Bobj_type_name%5D=1&display%5Bredshift%5D=1&display%5Bphases%5D=1&display%5Bexptime%5D=1&display%5Bobserver%5D=1&display%5Breducers%5D=1&display%5Bsource_group_name%5D=1&display%5Basciifile%5D=1&display%5Bfitsfile%5D=1&display%5Bspectype_name%5D=1&display%5Bquality_name%5D=1&display%5Bextinction_corr_name%5D=0&display%5Bflux_calib_name%5D=0&display%5Bwl_medium_name%5D=0&display%5Bgroups%5D=0&display%5Bpublic%5D=1&display%5Bend_pop_period%5D=0&display%5Breporters%5D=0&display%5Bpublish%5D=1&display%5Bcontrib%5D=0&display%5Bremarks%5D=0&display%5Bcreatedby%5D=1&display%5Bcreationdate%5D=1&display%5Bmodifiedby%5D=0&display%5Blastmodified%5D=0'
response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
content = BeautifulSoup(response.content, 'html.parser')
#print(content)
container = content.find('tbody')
snRows = container.findAll('tr')
supernovas = []

for sn in snRows:
	name = sn.find('td',attrs={'class':'cell-iauname_w_prefix'})
	redshift = sn.find('td',attrs={'class':'cell-redshift'})
	try:
		name = name.text
		redshift = redshift.text
		snid = name.split(' ')[-1]
		supernovas.append({'snid':snid,'name':name,'redshift':float(redshift)})
		#print(name, name.split(' ')[-1],redshift)
	except:
		continue

x = []
y = []

data = []

for sn in supernovas:
	url = 'https://www.wis-tns.org/object/' + sn['snid']
	response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
	content = BeautifulSoup(response.content, 'html.parser')
	magContainer = content.find('div',attrs={'class':'field-discoverymag'})
	try:
		mag = magContainer.find('b')
	except:
		print(sn['snid'])
		continue
	mag = float(mag.text)
	Mm = mag + 19.6
	distance = (10.**((Mm+5.)/5.))/1000000.
	velocity = sn['redshift']*300000.
	x.append(distance)
	y.append(velocity)
	data.append({
		'snid':sn['snid'],
		'name':sn['name'],
		'redshift':sn['redshift'],
		'mag':mag,
		'M-m':Mm,
		'distance':distance,
		'velocity':velocity
	})
	time.sleep(2)

df = pd.DataFrame(data) 
df.to_csv("hubble_constant.csv", index=False)
'''