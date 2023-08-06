#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append(__file__.replace("paneltime\\functions.py",'build\\lib.win-amd64-3.5'))
sys.path.append(__file__.replace("paneltime\\functions.py",'build\\lib.linux-x86_64-3.5'))
import cfunctions as c
import numpy as np
import sys
import os
import csv
import re

def currentdir():
	path=os.path.dirname(__file__)
	return path

def timer(tic, a):
	if a is None:
		a=[]
		tic=time.perf_counter()
	tac=time.perf_counter()
	a.append(tic-tac)
	return tac,a


def join(path,iterative):
	for i in iterative:
		path=os.path.join(path,i)
	return path


def clean(string,split='',cleanchrs=['\n','\t',' ']):
	"""Cleans the text for linfeed etc., and splits the text wiht split if split is not None. \n
	If return_string a string is returned when the lenght of the split string is 1"""
	if split is None or split=='':
		s=clean_str(string,cleanchrs)
		return s		
	if any([i in split for i in cleanchrs]):
		s=string.split(split)
		for i in range(len(s)):
			s[i]=clean_str(s[i],cleanchrs)
	else:	
		s=clean_str(string,cleanchrs,split)

	ret=[]
	for i in s:
		if i!='':
			ret.append(i)
	return ret

def split_input(input_str):
	
	if input_str is None:
		return None
	
	illegal=['§','£','¤']
	input_str=input_str.replace('\n','').replace(' ','').replace('\r','').replace('\t','')
	p = re.compile('\([^()]+\)')
	if np.any([i in input_str for i in illegal]):
		raise RuntimeError(f"The characters {','.join(illegal)} are not allowed in model string")
	while 1:
		matches=tuple(p.finditer(input_str))
		if len(matches)==0:
			break
		for m in matches:
			k,n=m.start(),m.end()
			s =input_str[:k]+'¤'
			s+=input_str[k+1:n-1].replace('+','§') + '£'
			s+=input_str[n:]
			input_str=s

		

	for s in [',','\n','+',' ']:
		lst=input_str.split(s)
		if len(lst)>1:
			break
	x=[]
	for i in lst:
		m=clean(i)
		if m!='':
			m=m.replace('¤','(')
			m=m.replace('§','+')
			m=m.replace('£',')')
			x.append(m)
	return x	


def clean_str(s,cleanchrs,split=''):
	for j in cleanchrs:
		s=s.replace(j,'')
	if split!='':
		s=s.split(split)
	return s

def clean_section(string):
	for i in ['\n\n','\n\r','\r\n']:
		while i in string:
			string=string.replace(i,'\n')
	if string[0]=='\n':
		string=string[1:]
	return string


def formatarray(array,linelen,sep):
	s=sep.join([str(i) for i in array])
	s='\n'.join(s[n:n + linelen] for n in range(0, len(s), linelen))	
	return s

def replace_many(string,oldtext_list,newtext):
	for i in oldtext_list:
		string=string.replace(i,newtext)


def savevar(variable,name='tmp'):
	"""takes variable and name and saves variable with filname <name>.csv """	
	fname=obtain_fname('./output/'+name)
	print ( 'saves to '+ fname)
	if type(variable)==np.ndarray:
		if not variable.dtype=='float64':
			savelist(variable, fname)	
		else:
			np.savetxt(fname,variable,delimiter=";")
	else:
		savelist(variable, fname)


def savelist(variable,name):
	file = open(name,'w',newline='')
	writer = csv.writer(file,delimiter=';')
	writer.writerows(variable)
	file.close()	

def savevars(varlist):
	"""takes a tuple of (var,name) pairs and saves numpy array var 
	with <name>.csv. Use double brackets for single variable."""	

	for var,name in varlist:
		savevar(var,name)

def obtain_fname(name):

	path=os.path.abspath(name)
	path_dir=os.path.dirname(path)
	if not os.path.exists(path_dir):
		os.makedirs(path_dir)	

	return path

def copy_array_dict(d):
	r=dict()
	for i in d:
		r[i]=np.array(d[i])
	return r


def append(arr,values):
	for i in range(len(arr)):
		arr[i].append(values[i])
		

		