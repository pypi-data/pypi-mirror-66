##############################################################|----------====----------|##############################################################
##############################################################|+---#----~-~~-~----#---+|##############################################################
##############################################################|*-------WebWrite-------*|##############################################################
##############################################################|+---#----~-~~-~----#---+|##############################################################
##############################################################|----------BETA----------|##############################################################


#Creating file and html code
import os
def startuse(name, header, css=0, way=0):
	global handle
	file_name = f'{name}.html'
	if way != 0:
		os.system(f'cd {way}')
		os.system(f'{file_name}')
	if css == 0:
		global code
		code = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>""" + header + """</title>
</head>
<body>
<!-- File made by WebWrite -->\n"""
		return handle
	else:
		global css_name
		css_name = css + ".css"
		handle = open(file_name, "w")
		code = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<link rel="stylesheet" href='""" + css_name + """'>
	<title>""" + header + """</title>
</head>
<body>
<!-- File made by WebWrite -->\n"""
	return handle


#Creating b block
def writeb(text):
	tex = f'<b>{text}</b>'
	return tex

#Creating br block
def writebr(text1, text2):
	tex = f'{text1}<br>{text2}'
	return tex

#Creating button
def writebut(text, clss=0, change=True):
	if change == False:
		if clss == 0:
			global usikBut
			usikBut = f"<button>{text}</button>"
			return usikBut
		else:
			usikBut = f'<button class = "{clss}"> {text} </button>'
			return usikBut
	else:
		if clss == 0:
			global code

			code += f"<button>{text}</button>"

		else:
			code += f'<button class = "{clss}">{text}</button>'

#Creating code block
def writecode(text, clss=0, change=True):
	if change == False:
		if clss == 0:
			global usikCode
			usikCode = f"<code>{text}</code>"
			return usikCode
		else:
			usikCode = f'<code class = "{clss}"> {text} </code>'
			return usikCode
	else:
		if clss == 0:
			global code

			code += f"<code>{text}</code>"

		else:
			code += f'<code class = "{clss}">{text}</code>'

#Creating del block
def writedel(text):
	led = f'<del>{text}</del>'
	return led

#Creating hr
def writehr(text):
	hr = f'<hr>{text}</hr>'
	return hr

#Creating i block
def writei(text):
	i = f'<i>{text}</i>'
	return i

#Creating mark
def writemark(text):
	mark = f'<mark>{text}</mark>'
	return mark

def writeruby(text):
	ruby = f'<ruby>{text}</ruby>'


#Creating list-text
def listel(text):
	li = f'<li>{text}</li>'
	return li

#Creating list
def writelist(kind, text, clss=0, change=True):
	if kind == "mark":
		kind = "ul"
	elif kind == "numb":
		kind = "ol"
	if change == False:
		if clss == 0:
			global usikList
			usikList = f"<{kind}>{text}</{kind}>"
			return usikList
		else:
			usikList = f'<{kind} class = "{clss}">{text}</{kind}>'
			return usikList
	else:
		if clss == 0:
			global code
			code += f"<{kind}>{text}</{kind}>"
		else:
			code += f'<{kind} class = "{clss}">{text}</{kind}>'

"""List of types (kind) for writeinp()"""
# 1. button
# 2. checkbox
# 3. file
# 4. hidden
# 5. image
# 6. password
# 7. radio
# 8. reset
# 9. submit
# 10. text
# 11. color
# 12. date
# 13. datetime
# 14. datetime-local
# 15. email
# 16. number
# 17. range
# 18. search
# 19. tel
# 20. time
# 21. url
# 22. month
# 23. week

#Creating input
def writeinp(valu, kind, name, clss=0, change=True):
	if change == False:
		if clss == 0:
			global usikInp
			usikInp = f"<input value = '{valu}' type = '{kind}' name = '{name}'>"
			return usikInp
		else:
			usikInp = f"<input value = '{valu}' class = '{clss}' type = '{kind}' name = '{name}'>"
			return usikInp
	else:
		if clss == 0:
			global code
			code += f"<input value = '{valu}' type = '{kind}' name = '{name}'>"
		else:
			code += f"<input value = '{valu}' class = '{clss}' type = '{kind}' name = '{name}'>"

#Creating form
def writeform(text, action, name, clss=0, change=True):
	if change == False:
		if clss == 0:
			global usikForm
			usikForm = f"<form action = '{action}' name = '{name}'>{text}</form>"
			return usikForm
		else:
			usikForm = f"<form class = '{clss}' action = '{action}' name = '{name}'>{text}</form>"
			return usikForm
	else:
		if clss == 0:
			global code
			code += f"<form action = '{action}' name = '{name}'>{text}</form>"
		else:
			code += f"<form class = '{clss}' action = '{action}' name = '{name}'>{text}</form>"
	

#Creating p block
def writep(text, clss=0, change=True):
	if change == False:
		if clss == 0:
			global usikP
			usikP = f"<p>{text}</p>"
			return usikP
		else:
			usikP = f'<p class = "{clss}"> {text} </p>'
			return usikP
	else:
		if clss == 0:
			global code

			code += f'<p>{text}</p>'

		else:
			code += f'<p class = "{clss}">{text}</p>'

#Creating h block
def writeh(respect, text, clss=0, change=True):
	if change == False:
		if clss == 0:
			global usikH
			usikH = f'<h{respect}>{text}</h{respect}>'
			return usikH
		else:
			usikH = f'<h{respect} class = "{clss}">{text}</h{respect}>'
			return usikH
	else:
		if clss == 0:
			global code
			code += f'<h{respect}>{text}</h{respect}>'
		else:
			code += f'<h{respect} class = "{clss}">{text}</h{respect}>'

#Creating link
def writea(text, href, clss=0, change=True):
	if change == False:
		if clss == 0:
			global usikA
			usikA = f'<a href = "{href}">{text}</a>'
			return usikA
		else:
			usikA = f'<a href = "{href}" class = "{clss}">{text}</a>'
			return usikA
	else:
		if clss == 0:
			global code
			code += f'<a href = "{href}">{text}</a>'
		else:
			code += f'<a href = "{href}" class = "{clss}">{text}</a>'


#Creating image
def writeimg(src, alt, clss=0, change=True):
	if change == False:
		if clss == 0:
			global usikImg
			usikImg = f'<img  src = "{src}"  alt = "{alt}">'
			return usikImg
		else:
			usikImg = f'<img  src = "{src}"  alt = "{alt}" class = "{clss}">'
			return usikImg
	else:
		if clss == 0:
			global code
			code += f'<img  src = "{src}"  alt = "{alt}">'
		else:
			code += f'<img  src = "{src}"  alt = "{alt}" class = "{clss}">'


#Creating div
def writediv(text, clss=0, change=True):
	if change == False:
		if clss == 0:
			global usikDiv
			usikDiv = f'<div>{text}</div>'
			return usikDiv
		else:
			usikDiv = f'<div class="{clss}">{text}</div>'
			return usikDiv
	else:
		if clss == 0:
			global code
			code += f'<div>{text}</div>'
		else:
			code += f'<div class="{clss}">{text}</div>'

#Connecting CSS
def stylestart():
	global csscode
	csscode = """/* File made by WebWrite */ \n"""
	global stylecss
	stylecss = open(css_name, "w")

#Start connecting to class
def startclass(clss, pseudo=0):
	if pseudo == 0:
		global csscode
		csscode += f'.{clss} ' + "{ \n"
	else:
		csscode += f'.{clss}:{pseudo} ' + "{ \n"

#Start connecting to object
def startObject(obj, pseudo=0):
	if pseudo == 0:
		global csscode
		csscode += f'{obj} ' + "{ \n"
	else:
		csscode += f'{obj}:{pseudo} ' + "{ \n"

#Creating img
def setimg(name):
	call = f'url({name})'
	return call

#You can also use usestyle() to create some virtual variables
def usevar(varname):
	var = f'var(--{varname});'
	return var

"""~Functions which usestyle() supports~"""

# 1. margin (top, right, bottom, left)
# 2. padding (top, right, bottom, left)
# 3. display
# 4. position
# 5. align-items
# 6. backgraund-color
# 7. background-image (with using setimg())
# 8. font-family
# 9. left
# 10. right
# 11. bottom
# 12. top
# and other things the same type

#Connecting styles
def usestyle(kind, mean, fin=False):
	if fin == False:
		global csscode
		csscode += f"\t{kind}: {mean};\n"
	else:
		csscode += f"\t{kind}: {mean};\n" + "}\n\n"


#Unactivating CSS
def stylefin():
	stylecss.write(csscode)
	stylecss.close()


#Finish use
def finuse():
	global code
	code += "\n</body>"
	code += "\n</html>"
	handle.write(code)
	handle.close()
