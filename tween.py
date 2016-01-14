'''
tween para BGE, v0.4
Mario Mey - http://www.mariomey.com.ar

Funcion Tween, para mover objetos y bones y cambiar influence de Constraints
en un tiempo determinado, usando diferentes equaciones para la interpolacion.


Based in Tweener, for ActionScript 2 and 3.
https://code.google.com/p/tweener/

Using Robert Penner's Easing Functions
http://www.robertpenner.com/easing/
'''

import bge, mathutils, time

gd = bge.logic.globalDict
scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()
own = cont.owner

# TWEEN - Principal, hace funcionar el Loop
def tween(**kwargs):

	# claves y valores por defecto
	function = ''
	element = own.name
	
	prop_value_begin = None
	prop_value = None
	
	enforce_begin = None
	enforce = None
	
	color_begin = None
	color = None

	loc_obj_begin = None
	loc_begin = None
	loc_obj_target = None
	loc_target = None

	rot_obj_begin = None
	rot_begin = None
	rot_obj_target = None
	rot_target = None

	scl_obj_begin = None
	scl_begin = None
	scl_obj_target = None
	scl_target = None

	delay = 0
	duration = 1.0
	ease_type = 'outQuad'
	
	own_prop_on_start = None
	own_prop_on_start_value = None
	own_prop_on_end = None
	own_prop_on_end_value = None
	
	gd_key_on_start = None
	gd_key_on_start_value = None
	gd_key_on_end = None
	gd_key_on_end_value = None
	
	seg_orden_on_end = None
	
	if 'element' in kwargs:             element                = kwargs['element']

	if 'prop_value_begin' in kwargs:    prop_value_begin       = kwargs['prop_value_begin']
	if 'prop_value' in kwargs:          prop_value             = kwargs['prop_value']
	
	if 'enforce_begin' in kwargs:       enforce_begin          = kwargs['enforce_begin']
	if 'enforce' in kwargs:             enforce                = kwargs['enforce']

	if 'color_begin' in kwargs:         color_begin            = kwargs['color_begin']
	if 'color' in kwargs:               color                  = kwargs['color']

	if 'loc_obj_begin' in kwargs:       loc_obj_begin          = kwargs['loc_obj_begin']
	if 'loc_begin' in kwargs:           loc_begin              = kwargs['loc_begin']
	if 'loc_obj_target' in kwargs:      loc_obj_target         = kwargs['loc_obj_target']
	if 'loc_target' in kwargs:          loc_target             = kwargs['loc_target']

	if 'rot_obj_begin' in kwargs:       rot_obj_begin          = kwargs['rot_obj_begin']
	if 'rot_begin' in kwargs:           rot_begin              = kwargs['rot_begin']
	if 'rot_obj_target' in kwargs:      rot_obj_target         = kwargs['rot_obj_target']
	if 'rot_target' in kwargs:          rot_target             = kwargs['rot_target']

	if 'scl_obj_begin' in kwargs:       scl_obj_begin          = kwargs['scl_obj_begin']
	if 'scl_begin' in kwargs:           scl_begin              = kwargs['scl_begin']
	if 'scl_obj_target' in kwargs:      scl_obj_target         = kwargs['scl_obj_target']
	if 'scl_target' in kwargs:          scl_target             = kwargs['scl_target']

	if 'delay' in kwargs:               delay                  = kwargs['delay']
	if 'duration' in kwargs:            duration               = kwargs['duration']
	if 'ease_type' in kwargs:           ease_type              = kwargs['ease_type']
	
	if 'own_prop_on_start' in kwargs:       own_prop_on_start          = kwargs['own_prop_on_start']
	if 'own_prop_on_start_value' in kwargs: own_prop_on_start_value    = kwargs['own_prop_on_start_value']
	if 'own_prop_on_end' in kwargs:         own_prop_on_end            = kwargs['own_prop_on_end']
	if 'own_prop_on_end_value' in kwargs:   own_prop_on_end_value      = kwargs['own_prop_on_end_value']

	if 'gd_key_on_start' in kwargs:       gd_key_on_start          = kwargs['gd_key_on_start']
	if 'gd_key_on_start_value' in kwargs: gd_key_on_start_value    = kwargs['gd_key_on_start_value']
	if 'gd_key_on_end' in kwargs:         gd_key_on_end            = kwargs['gd_key_on_end']
	if 'gd_key_on_end_value' in kwargs:   gd_key_on_end_value      = kwargs['gd_key_on_end_value']

	if 'seg_orden_on_end' in kwargs:   seg_orden_on_end      = kwargs['seg_orden_on_end']
			
	# ERRORES ERRORES ERRORES
	# ERRORES ERRORES ERRORES
	# ERRORES ERRORES ERRORES
	
	# si no se ingreso ningun dato.
	cond1 = loc_obj_target == loc_target == None
	cond2 = rot_obj_target == rot_target == None
	cond3 = scl_obj_target == scl_target == None
	cond4 = prop_value == color == enforce == None
	if cond1 and cond2 and cond3 and cond4:
		print('Tween Error. Falta, al menos, uno de los siguientes datos:')
		print('       loc_obj_target, loc_target,')
		print('       rot_obj_target, rot_target,')
		print('       scl_obj_target, scl_target,')
		print('       prop_value, color, enforce')
		return
	
	# para evitar multiples acciones
	cond1 = loc_obj_begin != None or loc_begin != None or loc_obj_target != None or loc_target != None
	cond2 = rot_obj_begin != None or rot_begin != None or rot_obj_target != None or rot_target != None
	cond3 = scl_obj_begin != None or scl_begin != None or scl_obj_target != None or scl_target != None
	cond4 = color_begin != None or color != None
	cond5 = enforce_begin != None or enforce != None
	cond6 = prop_value != None
	if int(cond1) + int(cond2) + int(cond3) + int(cond4) + int(cond5) + int(cond6) > 1 :
		print('Tween Error. Por favor, de a una accion a la vez.')
		return
	
	# para evitar mover un bone a un worldLocation
	if len(element.split(':')) == 2 and (loc_obj_begin != None or loc_obj_target != None):
		print('Tween Error. Por el momento, no se puede mover un bone a/de un Word Location')
		return
	
	# si no se asigna un valor a own_prop_on_start o own_prop_on_end
	if own_prop_on_start != None and own_prop_on_start_value == None:
		print('Tween Error. No se asigno un valor a own_prop_on_start')
		return

	if own_prop_on_end != None and own_prop_on_end_value == None:
		print('Tween Error. No se asigno un valor a own_prop_on_end')
		return

	if prop_value != None and element.split(':') == 1 and element not in own:
		print('Tween Error. No existe la propiedad del objeto:', own.name)
		return

	if prop_value != None and element.split(':') == 2 and element.split(':')[1] not in scene.objects[element.split(':')[0]]:
		print('Tween Error. No existe la propiedad del objeto: ', element.split(':')[0])
		return

	#~ if prop_value != None and (type(prop_value) == int or type(prop_value) == float:
		#~ print('Error. Valores en int o float para prop_value')
		#~ return

	
	# FIN - ERRORES
	# FIN - ERRORES
	# FIN - ERRORES

	# propiedad (clave) de objeto
	if prop_value != None:
		# si es 'prop' pasa a ser ['objeto', 'prop']
		if len(element.split(':')) == 1:
			element = [own.name, element]
		else:
			element = element.split(':')
		
		function = 'property'
		if prop_value_begin == None:
			prop_value_begin = scene.objects[element[0]][element[1]]
			
		
	else:
	
		element = element.split(':')
		
		# objeto
		if len(element) == 1:
			# si es para mover un obj, setea loc_begin[x,y,z]
			# dejando '' si no tiene nada.
			if loc_obj_target != None or loc_target != None:
				function = 'obj_move'

				if loc_begin == None and loc_obj_begin == None:
					loc_begin = list(scene.objects[element[0]].worldPosition)
			
				elif loc_obj_begin != None:
					loc_begin = list(scene.objects[loc_obj_begin].worldPosition)
					#~ print(loc_begin)
			
			# si es para rotar un obj, setea rot_begin[x,y,z]
			# dejando '' si no tiene nada.
			if rot_obj_target != None or rot_target != None:
				function = 'obj_rotate'

				if rot_begin == None and rot_obj_begin == None:
					rot_begin = list(scene.objects[element[0]].worldOrientation.to_euler())
			
				elif rot_obj_begin != None:
					rot_begin = list(scene.objects[rot_obj_begin].worldOrientation.to_euler())
					#~ print(rot_begin)
			
			# si es para escalar un obj, setea scl_begin[x,y,z]
			# dejando '' si no tiene nada.
			if scl_obj_target != None or scl_target != None:
				function = 'obj_scale'

				if scl_begin == None and scl_obj_begin == None:
					scl_begin = list(scene.objects[element[0]].worldScale)
			
				elif scl_obj_begin != None:
					scl_begin = list(scene.objects[scl_obj_begin].worldScale)
					#~ print(scl_begin)
			
			# si es para cambiar color de un obj, setea color_begin[r,g,b,a]
			if color != None :
				function = 'obj_color'

				if color_begin == None:
					color_begin = list(scene.objects[element[0]].color)
		
		# bone en Local
		# si es para mover un bone, setea begin[x,y,z] del bone
		elif len(element) == 2:
			function = 'bone_move'
			if loc_begin == None:
				arm = scene.objects[element[0]]
				bone = element[1]
				loc_begin = list(arm.channels[bone].location)

		# constraint
		elif len(element) == 3:
			function = 'constraint_enforce'
			if enforce_begin == None:
				arm = scene.objects[element[0]]
				bone_constraint = element[1] + ':' + element[2]
				enforce_begin = arm.constraints[bone_constraint].enforce
	
	number = -1
	
	# Escanea si existe own['tween1 -> 16']
	# Si esta en uso, pero es del mismo objeto y
	# la misma funcion, la borra y la usa
	for i in range(16):
		
		num = str(i)
		if 'tween' + num in own:
			cond1 = own['tween' + num]['function'] == function
			cond2 = own['tween' + num]['element'] == element
			if cond1 and cond2:
				
				# function a ejecutar cuando termina, si se corta antes
				if own['tween' + num]['own_prop_on_end'] != None:
					print('lo hace?¿¡')
					prop = own['tween' + num]['own_prop_on_end']
					value = own['tween' + num]['own_prop_on_end_value']
					own[prop] = value

				del(own['tween' + num])
				number = i
				break
	
	# Si no encontro para reemplazar, de nuevo,
	# Escanea si existe own['tween1 -> 16']
	if number == -1:
		for i in range(16):
			
			num = str(i)
			if 'tween' + num in own:
				# Sigue contando
				continue
			
			# Encontro uno libre
			number = i
			break
	
	number = str(number)

	own['tween' + number]                        = {}
	own['tween' + number]['number']              = number
	own['tween' + number]['function']            = function
	own['tween' + number]['element']             = element
	
	own['tween' + number]['prop_value_begin']    = prop_value_begin
	own['tween' + number]['prop_value']          = prop_value
	
	own['tween' + number]['enforce_begin']       = enforce_begin
	own['tween' + number]['enforce']             = enforce

	own['tween' + number]['color_begin']         = color_begin
	own['tween' + number]['color']               = color
	
	own['tween' + number]['loc_begin']           = loc_begin
	own['tween' + number]['loc_obj_target']      = loc_obj_target
	own['tween' + number]['loc_target']          = loc_target

	own['tween' + number]['rot_begin']           = rot_begin
	own['tween' + number]['rot_obj_target']      = rot_obj_target
	own['tween' + number]['rot_target']          = rot_target

	own['tween' + number]['scl_begin']           = scl_begin
	own['tween' + number]['scl_obj_target']      = scl_obj_target
	own['tween' + number]['scl_target']          = scl_target

	own['tween' + number]['enforce']             = enforce
	own['tween' + number]['enforce_begin']       = enforce_begin

	own['tween' + number]['duration']            = duration
	own['tween' + number]['delay']               = delay
	own['tween' + number]['ease_type']           = ease_type
	
	own['tween' + number]['own_prop_on_start']       = own_prop_on_start
	own['tween' + number]['own_prop_on_start_value'] = own_prop_on_start_value
	own['tween' + number]['own_prop_on_end']         = own_prop_on_end
	own['tween' + number]['own_prop_on_end_value']   = own_prop_on_end_value
	
	own['tween' + number]['gd_key_on_start']       = gd_key_on_start
	own['tween' + number]['gd_key_on_start_value'] = gd_key_on_start_value
	own['tween' + number]['gd_key_on_end']         = gd_key_on_end
	own['tween' + number]['gd_key_on_end_value']   = gd_key_on_end_value
	
	own['tween' + number]['seg_orden_on_end']    = seg_orden_on_end
	own['tween' + number]['timer'] = time.time()

	if 'print_tween_funciones' in gd and gd['print_tween_funciones']:
		
		texto = ''
		texto += '--TWEEN\n--number: ' + number + ' --' + function + str(element) + '\n'
		texto += '--delay: '+ str(delay) + ' '
		texto += '--duration: ' + str(duration) + ' '
		texto += '--ease_type: ' + ease_type + '\n'
		
		if enforce != None:
			texto += '--enforce: ' + str(enforce)

			if enforce_begin != None:
				texto += ' --enforce_begin: ' + str(enforce_begin)
			
			texto += '\n'

		if color != None:
			texto += '--color: ' + color

			if color_begin != None:
				texto += ' --color_begin: ' + str(color_begin)
			
			texto += '\n'

		if prop_value != None:
			texto += '--prop_value: ' + str(prop_value)

			if prop_value_begin != None:
				texto += ' --prop_value_begin: ' + str(prop_value_begin)
			
			texto += '\n'

		if loc_begin != None and loc_obj_begin != None:
			texto += '--loc_begin: ' + loc_begin + loc_obj_begin + '\n'

		if loc_target != None and loc_obj_target != None:
			texto += '--loc_target: ' + loc_target + loc_obj_target + '\n'

		if rot_begin != None and rot_obj_begin != None:
			texto += '--rot_begin: ' + rot_begin + rot_obj_begin + '\n'

		if rot_target != None and rot_obj_target != None:
			texto += '--rot_target: ' + rot_target + rot_obj_target + '\n'

		if scl_begin != None and scl_obj_begin != None:
			texto += '--scl_begin: ' + scl_begin + scl_obj_begin + '\n'

		if scl_target != None and scl_obj_target != None:
			texto += '--scl_target: ' + scl_target + scl_obj_target + '\n'

		if own_prop_on_start != None:
			texto += '--own_prop_on_start: ' + str(own_prop_on_start) + ':' + str(own_prop_on_start_value) + '\n'

		if own_prop_on_end != None:
			texto += '--own_prop_on_end: ' + str(own_prop_on_end) + ':' + str(own_prop_on_end_value) + '\n'

		if gd_key_on_start != None:
			texto += '--gd_key_on_start: ' + str(gd_key_on_start) + ':' + str(gd_key_on_start_value) + '\n'

		if gd_key_on_end != None:
			texto += '--gd_key_on_end: ' + str(gd_key_on_end) + ':' + str(gd_key_on_end_value) + '\n'

		if seg_orden_on_end != None:
			texto += '--seg_orden_on_end: ' + seg_orden_on_end
		
		print(texto)




# TWEEN - Loop
def tween_loop():
	
	for i in range(16):

		if 'tween' + str(i) in own:
			
			number              = str(i)
			function            = own['tween' + number]['function']
			element             = own['tween' + number]['element']
			
			prop_value_begin    = own['tween' + number]['prop_value_begin']
			prop_value          = own['tween' + number]['prop_value']
			
			enforce_begin       = own['tween' + number]['enforce_begin']
			enforce             = own['tween' + number]['enforce']
			
			color_begin         = own['tween' + number]['color_begin']
			color               = own['tween' + number]['color']
			
			loc_begin           = own['tween' + number]['loc_begin']
			loc_obj_target      = own['tween' + number]['loc_obj_target']
			loc_target          = own['tween' + number]['loc_target']

			rot_begin           = own['tween' + number]['rot_begin']
			rot_obj_target      = own['tween' + number]['rot_obj_target']
			rot_target          = own['tween' + number]['rot_target']

			scl_begin           = own['tween' + number]['scl_begin']
			scl_obj_target      = own['tween' + number]['scl_obj_target']
			scl_target          = own['tween' + number]['scl_target']

			delay               = own['tween' + number]['delay']
			duration            = own['tween' + number]['duration']
			ease_type           = own['tween' + number]['ease_type']
			
			own_prop_on_start       = own['tween' + number]['own_prop_on_start']
			own_prop_on_start_value = own['tween' + number]['own_prop_on_start_value']
			own_prop_on_end         = own['tween' + number]['own_prop_on_end']
			own_prop_on_end_value   = own['tween' + number]['own_prop_on_end_value']
			
			gd_key_on_start       = own['tween' + number]['gd_key_on_start']
			gd_key_on_start_value = own['tween' + number]['gd_key_on_start_value']
			gd_key_on_end         = own['tween' + number]['gd_key_on_end']
			gd_key_on_end_value   = own['tween' + number]['gd_key_on_end_value']
			
			seg_orden_on_end    = own['tween' + number]['seg_orden_on_end']
			
			timer               = time.time() - own['tween' + number]['timer'] - own['tween' + number]['delay']
			
			finish              = None
			
			# Para que funcione delay
			if timer >= 0:
				
				# valor para asignar a propiedad del objeto cuando comienza
				if own_prop_on_start != None:
					own[own_prop_on_start] = own_prop_on_start_value
					own['tween' + number]['own_prop_on_start'] = None
					own['tween' + number]['own_prop_on_start_value'] = None

				# valor para asignar a propiedad de globalDict cuando comienza
				if gd_key_on_start != None:
					gd[gd_key_on_start] = gd_key_on_start_value
					own['tween' + number]['gd_key_on_start'] = None
					own['tween' + number]['gd_key_on_start_value'] = None
				
				# (MD) segunda orden a fijar cuando comienza
				if seg_orden_on_end != None:
					own['seg_orden_tween' + number] = seg_orden_on_end
					own['tween' + number]['seg_orden_on_end'] = None
				
				# si finish es un objeto, setea finish[x,y,z] CADA VEZ
				# Esto es por si el objeto esta en movimiento
				# FUNCION OBJ_MOVE Y BONE_MOVE
				if function == 'obj_move' or function == 'bone_move':
					# move
					if loc_obj_target != None:
						finish = list(scene.objects[loc_obj_target].worldPosition)
					else:
						finish = loc_target
					
					change = ['','','']
					for i in range(3):
						if finish[i] != '':
							change[i] = finish[i] - loc_begin[i]
						
					xyz = ['','','']
					for i in range(3):
						if change[i] != '':
							xyz[i] = tween_eq(ease_type, timer, loc_begin[i], change[i], duration)
						#~ print(xyz)
					
					# termina el tiempo de duracion
					if timer > duration:
						xyz = finish
						#~ print('borra', number)
						del(own['tween' + number])
					
						# function a ejecutar cuando termina
						if own_prop_on_end != None:
							own[own_prop_on_end] = own_prop_on_end_value
					
						# function a ejecutar cuando termina
						if gd_key_on_end != None:
							gd[gd_key_on_end] = gd_key_on_end_value
					
					if function == 'obj_move':
						#~ print(function + '("' + element[0] + '", ' + str(xyz) + ')')
						eval('tween_' + function + '("' + element[0] + '", ' + str(xyz) + ')')
					elif function == 'bone_move':
						#~ print(function + '("' + element[0] + '", ' + str(xyz) + ')')
						eval('tween_' + function + '("' + element[0] + ':' + element[1] + '", ' + str(xyz) + ')')
				
				# OBJ_ROTATE
				elif function == 'obj_rotate':
					if rot_obj_target != None:
						finish = list(scene.objects[rot_obj_target].worldOrientation.to_euler())
					else:
						finish = rot_target
				
					change = ['','','']
					for i in range(3):
						if finish[i] != '':
							change[i] = finish[i] - rot_begin[i]
						
					xyz = ['','','']
					for i in range(3):
						if change[i] != '':
							xyz[i] = tween_eq(ease_type, timer, rot_begin[i], change[i], duration)
						#~ print(xyz)
					
					# termina el tiempo de duracion
					if timer > duration:
						xyz = finish
						#~ print('borra', number)
						del(own['tween' + number])
					
						# function a ejecutar cuando termina
						if own_prop_on_end != None:
							own[own_prop_on_end] = own_prop_on_end_value
					
						# function a ejecutar cuando termina
						if gd_key_on_end != None:
							gd[gd_key_on_end] = gd_key_on_end_value
					
					#~ print(function + '("' + element[0] + '", ' + str(xyz) + ')')
					eval('tween_' + function + '("' + element[0] + '", ' + str(xyz) + ')')
				
				# OBJ_SCALE
				elif function == 'obj_scale':
					if scl_obj_target != None:
						finish = list(scene.objects[scl_obj_target].worldScale)
					else:
						finish = scl_target
				
					change = ['','','']
					for i in range(3):
						if finish[i] != '':
							change[i] = finish[i] - scl_begin[i]
						
					xyz = ['','','']
					for i in range(3):
						if change[i] != '':
							xyz[i] = tween_eq(ease_type, timer, scl_begin[i], change[i], duration)
						#~ print(xyz)
					
					# termina el tiempo de duracion
					if timer > duration:
						xyz = finish
						#~ print('borra', number)
						del(own['tween' + number])
					
						# function a ejecutar cuando termina
						if own_prop_on_end != None:
							own[own_prop_on_end] = own_prop_on_end_value
					
						# function a ejecutar cuando termina
						if gd_key_on_end != None:
							gd[prop_own_prop_on_end] = gd_key_on_end_value
					
					#~ print(function + '("' + element[0] + '", ' + str(xyz) + ')')
					eval('tween_' + function + '("' + element[0] + '", ' + str(xyz) + ')')
				
				# FUNCION OBJ_COLOR
				elif function == 'obj_color':
					finish = color
				
					change = ['','','','']
					for i in range(4):
						if finish[i] != '':
							change[i] = finish[i] - color_begin[i]
						
					rgba = ['','','', '']
					for i in range(4):
						if change[i] != '':
							rgba[i] = tween_eq(ease_type, timer, color_begin[i], change[i], duration)
					
					# termina el tiempo de duracion
					if timer > duration:
						rgba = finish
						#~ print('borra', number)
						del(own['tween' + number])
					
						# function a ejecutar cuando termina
						if own_prop_on_end != None:
							own[own_prop_on_end] = own_prop_on_end_value
					
						# function a ejecutar cuando termina
						if gd_key_on_end != None:
							gd[gd_key_on_end] = gd_key_on_end_value
					
					#~ print('tween_obj_color("' + element + '", ' + str(rgba) + ')')
					eval('tween_obj_color("' + element[0] + '", ' + str(rgba) + ')')
				
				# FUNCION CONSTRAINT ENFORCE
				elif function == 'constraint_enforce':
				
					change = enforce - enforce_begin
					x = tween_eq(ease_type, timer, enforce_begin, change, duration)
					
					# termina el tiempo de duracion
					if timer > duration:
						x = enforce
						#~ print('borra', number)
						del(own['tween' + number])
						
						# Funcion a ejecutar cuando termina
						if own_prop_on_end != None:
							own[own_prop_on_end] = own_prop_on_end_value
					
						# Funcion a ejecutar cuando termina
						if gd_key_on_end != None:
							gd[gd_key_on_end] = gd_key_on_end_value
					
					#~ print('tween_constraint_enforce("' + element + '", ' + str(x) + ')')
					eval('tween_constraint_enforce("' + element[0] + ':' + element[1] + ':' + element[2] + '", ' + str(x) + ')')

				# FUNCION PROPERTY
				elif function == 'property':
				
					change = prop_value - prop_value_begin
					x = tween_eq(ease_type, timer, prop_value_begin, change, duration)
					
					# termina el tiempo de duracion
					if timer > duration:
						x = prop_value
						#~ print('borra', number)
						del(own['tween' + number])
						
						# Funcion a ejecutar cuando termina
						if own_prop_on_end != None:
							own[own_prop_on_end] = own_prop_on_end_value
					
						# Funcion a ejecutar cuando termina
						if gd_key_on_end != None:
							gd[gd_key_on_end] = gd_key_on_end_value
					
					#~ print('tween_constraint_enforce("' + element + '", ' + str(x) + ')')
					eval('tween_obj_property("' + element[0] + ':' + element[1] + '", ' + str(x) + ')')

# TWEEN - Ecuaciones
def tween_eq(ease_type, t, b, c, d):
	#~ if t >= 0:
	if ease_type == 'linear':
		return c * t / d + b
	elif ease_type == 'inQuad':
		t/=d
		return c * t * t + b
	elif ease_type == 'outQuad':
		t/=d
		return - c * t * (t - 2) + b
	elif ease_type == 'inOutQuad':
		t/=d/2
		if (t < 1):
			return c / 2 * t * t + b
		t -= 1
		return -c / 2 * ((t) * (t - 2) - 1) + b

# recibe objeto y valor en lista[x,y,z]
def tween_obj_move(element, xyz):
	for i in range(3):
		if xyz[i] != '': scene.objects[element].worldPosition[i] = xyz[i]

# recibe objeto y valor euler en lista[x,y,z]
def tween_obj_rotate(element, xyz):
	new_euler = scene.objects[element].worldOrientation.to_euler()

	for i in range(3):
		if xyz[i] != '': new_euler[i] = xyz[i]
			
	scene.objects[element].worldOrientation = new_euler.to_matrix()

# recibe objeto y valor en lista[x,y,z]
def tween_obj_scale(element, xyz):
	for i in range(3):
		if xyz[i] != '': scene.objects[element].localScale[i] = xyz[i]

# recibe objeto y valor en lista[r,g,b,a]
def tween_obj_color(element, rgba):
	for i in range(4):
		if rgba[i] != '': scene.objects[element].color[i] = rgba[i]

# recibe objeto:bone y valor en lista[x,y,z]
def tween_bone_move(element, xyz):
	element = element.split(':')
	new_vector = scene.objects[element[0]].channels[element[1]].location
	
	for i in range(3):
		if xyz[i] != '': new_vector[i] = xyz[i]
	
	scene.objects[element[0]].channels[element[1]].location = new_vector

# recibe objeto:bone:constraint y el valor de enforce
def tween_constraint_enforce(element, x):
	element = element.split(':')
	scene.objects[element[0]].constraints[element[1] + ':' + element[2]].enforce = x

# recibe objeto:property y el valor de property
def tween_obj_property(element, x):
	element = element.split(':')
	scene.objects[element[0]][element[1]] = x


'''
tween for BGE, v0.2


For moving or rotating (euler) or scale object from:
-actual position or 
-[x,y,z] or 
-an object position/rotation/scale.
to:
-[x,y,z] or
-['',y,''] (just Y axis, for example) or
-an object position/rotation/scale.

E.G:
tween.tween(element='Torus', loc_obj_target='Empty.003', duration=3.5, ease_type='linear')
tween.tween(loc_target=['',4,''], own_prop_on_end='fx', own_prop_on_end_value=False)
tween.tween(rot_obj_target='Empty.000')
tween.tween(scl_obj=[1,1.5,''])


In Local, for moving bones from:
-actual position or
-[x,y,z] (in local)
to:
-[x,y,z] (in local)
-['',y,''] (just Y axis, for example)

EG: tween.tween(element='Armature:Bone.001', loc_target=[-2,1,2], duration=4)


For changing object color from:
-actual color or
-[r,g,b,a]
to:
-[r,g,b,a] or
-['',g,'',a] (just green and alpha, for example)

EG: tween.tween(element='Suzanne', color=['','','',1], ease_type='inOutQuad')


For changing bone constraint influence from:
-actual influence value
-Float number (0-1)
to:
-Float number (0-1)

EG: tween.tween(element='Armature.001:Bone.001:damp', enforce=1)


---------Defaults---------

function = ''
element = own.name            ; Name of the object as 'object'
                              ; Name of the bone as 'object:bone'
							  ; Name of the constraint as 'object:bone:constraint'

prop_value_begin = None       ; Start value of the transition of a object property value (optional)
prop_value = None             ; Final value of the transition of a object property value

enforce_begin = None          ; Start value of the transition of a constraint influence (optional)
enforce = None                ; Final value of the transition of a constraint influence

color_begin = None            ; Start value of the transition of an object color as [r,g,b,a] (optional)
color = None                  ; Final value of the transition of an object color as [r,g,b,a]

loc_obj_begin = None          ; Object (name) to get the starting position for the move transition
loc_begin = None              ; [x,y,z] or ['',5,0.5] of the starting position for the move transition
loc_obj_target = None         ; Object (name) to get the final position for the move transition
loc_target = None             ; [x,y,z] or ['',5,0.5] of the final position for the move transition

rot_obj_begin = None          ; Object (name) to get the starting rotation for the move transition
rot_begin = None              ; [x,y,z] or ['',5,0.5] of the starting rotation for the move transition
rot_obj_target = None         ; Object (name) to get the final rotation for the move transition
rot_target = None             ; [x,y,z] or ['',5,0.5] of the final rotation for the move transition

scl_obj_begin = None          ; Object (name) to get the starting scale for the move transition
scl_begin = None              ; [x,y,z] or ['',5,0.5] of the starting scale for the move transition
scl_obj_target = None         ; Object (name) to get the final scale for the move transition
scl_target = None             ; [x,y,z] or ['',5,0.5] of the final scale for the move transition

delay = 0                     ; Delay before tweening (in seconds)
duration = 1.0                ; Duration of the tweening (in seconds)
ease_type = 'outQuad'         ; Ease type: 'linear', 'outQuad', 'inQuad', 'inOutQuad' (Robbert Penner)

own_prop_on_start = None          ; Own object property (key of object dictionary) to change on tween start
own_prop_on_start_value = None    ; New value of the property

own_prop_on_end = None            ; Own object property (key of object dictionary) to change on tween finish
own_prop_on_end_value = None      ; New value of the property

gd_key_on_start = None          ; globalDict key to change on tween start
gd_key_on_start_value = None    ; New value of the property

gd_key_on_end = None            ; globalDict key to change on tween finish
gd_key_on_end_value = None      ; New value of the property

seg_orden_on_end = None       ; Second order (to do when end)

Based in Tweener, for ActionScript 2 and 3.
https://code.google.com/p/tweener/

Using Robert Penner's Easing Functions
http://www.robertpenner.com/easing/

Mario Mey
http://www.mariomey.com.ar

--------------
Changelog:
--------------


v0.5 - 2/4/2015:
- prop_on_start, prop_on_start_value, prop_on_end, prop_on_end_value
  are now own_prop_on_start, own_prop_on_start_value,
  own_prop_on_end and own_prop_on_end_value
  
- gd_key_on_start, gd_key_on_start_value, 
  gd_key_on_end, gd_key_on_end_value
  It works the same as with own_prop_on_start, etc, but using globalDict

v0.4 - 26/11/2014:
- prop_value, prop_value_begin:
  It works the same as with Enforce, using object's property
  'element' must be 'object:property' or just 'property' (own object)
  Funciona igual que con Enforce, usando una property del objeto
  'element' puede ser 'object:property' o solo 'property' (objecto own)

v0.3 - 23/10/2014:
- scl_obj_begin, scl_begin, scl_obj_target, scl_target:
  It works the same as with Position
  Funciona igual que con Position

v0.2 - 22/10/2014:
- own_prop_on_start, own_prop_on_start_value:
  Value assing to an object property on tween start
  Asignacion de un valor a una propiedad de un objeto cuando comienza el tween.

- seg_orden_on_end:
  Second Order, Tween version (MD component)
  Segunda Orden, version Tween (componente de las MD)

- delay:
  Delay before tween starting.
  Delay antes de comenzar el tween.

- rot_obj_begin, rot_begin, rot_obj_target, rot_target:
  It works the same as with Position
  Funciona igual que con Position


v0.1 – 1/10/2014:
- Only 1 or 2 axis bone movement fixed.
- Solucionado el movimiento de bones en 1 o 2 ejes solamente.

vSinNumero – 20/8/2014
- Lanzamiento inicial
- Initial launch

'''
