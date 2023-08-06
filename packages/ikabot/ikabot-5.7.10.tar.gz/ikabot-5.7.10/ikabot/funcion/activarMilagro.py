#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import gettext
from ikabot.config import *
from ikabot.helpers.gui import *
from ikabot.helpers.varios import *
from ikabot.helpers.botComm import *
from ikabot.helpers.pedirInfo import *
from ikabot.helpers.getJson import getCiudad

t = gettext.translation('activarMilagro',
                        localedir,
                        languages=idiomas,
                        fallback=True)
_ = t.gettext

def obtenerMilagrosDisponibles(s):
	idsIslas = getIdsdeIslas(s)
	islas = []
	for idIsla in idsIslas:
		html = s.get(urlIsla + idIsla)
		isla = getIsla(html)
		isla['activable'] = False
		islas.append(isla)

	ids, citys = getIdsDeCiudades(s)
	for ciudad in citys:
		city = citys[ciudad]
		wonder = [ isla['wonder'] for isla in islas if city['coords'] == '[{}:{}] '.format(isla['x'], isla['y']) ][0]
		if wonder in [ isla['wonder'] for isla in islas if isla['activable'] ]:
			continue
		html = s.get(urlCiudad + str(city['id']))
		ciudad = getCiudad(html)
		if 'temple' in [ edificio['building'] for edificio in ciudad['position'] ]:
			for i in range( len( ciudad['position'] ) ):
				if ciudad['position'][i]['building'] == 'temple':
					ciudad['pos'] = str(i)
					break
			for isla in islas:
				if isla['id'] == ciudad['islandId']:
					isla['activable'] = True
					isla['ciudad'] = ciudad
					break

	return [ isla for isla in islas if isla['activable'] ]

def activarMilagroImpl(s, isla):
	params = {'action': 'CityScreen', 'cityId': isla['ciudad']['id'], 'function': 'activateWonder', 'position': isla['ciudad']['pos'], 'backgroundView': 'city', 'currentCityId': isla['ciudad']['id'], 'templateView': 'temple', 'actionRequest': s.token(), 'ajax': '1'}
	rta = s.post(params=params)
	return json.loads(rta, strict=False)

def activarMilagro(s):
	banner()

	islas = obtenerMilagrosDisponibles(s)
	if islas == []:
		print(_('No existen milagros disponibles.'))
		enter()
		return
	print(_('¿Qué milagro quiere activar?'))
	i = 0
	print(_('(0) Salir'))
	for isla in islas:
		i += 1
		print('({:d}) {}'.format(i, isla['wonderName']))
	index = read(min=0, max=i)
	if index == 0:
		return
	isla = islas[index - 1]

	print(_('\nSe activará el milagro {}').format(isla['wonderName']))
	print(_('¿Proceder? [Y/n]'))
	rta = read(values=['y', 'Y', 'n', 'N', ''])
	if rta.lower() == 'n':
		return

	rta = activarMilagroImpl(s, isla)

	if rta[1][1][0] == 'error':
		print(_('No se pudo activar el milagro {}.').format(isla['wonderName']))
		enter()
		return

	print(_('Se activó el milagro {}.').format(isla['wonderName']))

	print(_('¿Desea activarlo nuevamente al terminar? [y/N]'))

	rta = read(values=['y', 'Y', 'n', 'N', ''])
	if rta.lower() != 'y':
		return

	enddate     = rta[2][1]['js_WonderTextDuration']['countdown']['enddate']
	currentdate = rta[2][1]['js_WonderTextDuration']['countdown']['currentdate']
	wait_time   = enddate - currentdate

	iterations = read(msg=_('¿Cuántas veces?: '), digit=True)

	if iterations == 0:
		return

	duration = wait_time * iterations

	print(_('Terminará en:{}').format(diasHorasMinutos(duration)))

	print(_('¿Proceder? [Y/n]'))
	rta = read(values=['y', 'Y', 'n', 'N', ''])
	if rta.lower() == 'n':
		return

	forkear(s)
	if s.padre is True:
		return

	info = _('\nActivo el milagro {} {:d} veces\n').format(isla['wonderName'], iterations)
	setInfoSignal(s, info)
	try:
		do_it(s, isla, wait_time, iterations)
	except:
		msg = _('Error en:\n{}\nCausa:\n{}').format(info, traceback.format_exc())
		sendToBot(s, msg)
	finally:
		s.logout()


def do_it(s, isla, wait_time, iterations):

	for i in range(iterations):
		esperar(wait_time + 5)

		rta = activarMilagroImpl(s, isla)

		if rta[1][1][0] == 'error':
			msg = _('No se pudo activar el milagro {}.').format(isla['wonderName'])
			sendToBot(s, msg)
			return

		enddate     = rta[2][1]['js_WonderTextDuration']['countdown']['enddate']
		currentdate = rta[2][1]['js_WonderTextDuration']['countdown']['currentdate']
		wait_time   = enddate - currentdate
