#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calculus
import numpy as np
import constraints as cnstr
import loglikelihood as logl
from scipy import stats
import sys


class direction:
	def __init__(self,panel,mp,output_tab):
		self.progress_bar=output_tab.progress_bar.set_progress
		self.progress_bar_obj=output_tab.progress_bar
		self.gradient=calculus.gradient(panel,self.progress_bar)
		self.hessian=calculus.hessian(panel,self.gradient,self.progress_bar)
		self.panel=panel
		self.constr=None
		self.hessian_num=None
		self.do_shocks=True
		self.input_old=None
		self.CI=0
		self.I=np.diag(np.ones(panel.args.n_args))
		self.mp=mp
		self.dx_norm=None
		self.H=None
		self.G=None
		self.g=None
		self.weak_mc_dict=[]


	def get(self,ll,its,newton_failed,msg):
		if ll.LL is None:
			raise RuntimeError("Error in LL calculation: %s" %(ll.err_msg,))
		self.ll=ll
		self.constr_old=self.constr
		self.progress_bar_obj.suffix=msg
		self.constr=cnstr.constraints(self.panel,ll.args_v)
		cnstr.add_static_constraints(self.constr,self.panel,ll,its)			
		self.calc_gradient(ll)
		self.calc_hessian(ll,its)
		
		self.weak_mc_dict=cnstr.add_dynamic_constraints(ll,self,newton_failed)	
		self.CI=self.constr.CI
		
		self.dx=solve(self.constr,self.H, self.g, ll.args_v)
		#dx=solve_delete(self.constr,hessian, g, ll.args_v)	

		
		self.dx_norm=self.normalize(self.dx, ll.args_v)
		try:
			self.dx_unconstr=self.normalize(solve(None,self.H, self.g, ll.args_v),ll.args_v)
		except:
			self.dx_unconstr=self.dx_norm
		self.progress_bar_obj.suffix=''

	
	def include(self,all=False):
		include=np.array(self.panel.args.n_args*[True])
		if all:
			return include
		include[list(self.constr.constraints)]=False
		return include	

	def calc_gradient(self,ll):
		DLL_e=-(ll.e_RE*ll.v_inv)*self.panel.included
		dLL_lnv=-0.5*(self.panel.included-(ll.e_REsq*ll.v_inv)*self.panel.included)	
		dLL_lnv*=ll.dlnv_pos
		self.LL_gradient_tobit(ll, DLL_e, dLL_lnv)
			
		self.g,self.G=self.gradient.get(ll,DLL_e,dLL_lnv,return_G=True)	
	
	def LL_gradient_tobit(self,ll,DLL_e,dLL_lnv):
		g=[1,-1]
		self.f=[None,None]
		self.f_F=[None,None]
		for i in [0,1]:
			if self.panel.input.tobit_active[i]:
				I=self.panel.tobit_I[i]
				self.f[i]=stats.norm.pdf(g[i]*ll.e_st[I])
				self.f_F[i]=(ll.F[i]!=0)*self.f[i]/(ll.F[i]+(ll.F[i]==0))
				self.v_inv05=ll.v_inv**0.5
				DLL_e[I]=g[i]*self.f_F[i]*self.v_inv05[I]
				dLL_lnv[I]=-0.5*DLL_e[I]*ll.e_RE[I]
				a=0
				

	def LL_hessian_tobit(self,ll,d2LL_de2,d2LL_dln_de,d2LL_dln2):
		g=[1,-1]
		if sum(self.panel.input.tobit_active)==0:
			return
		self.f=[None,None]
		e1s1=ll.e_st
		e2s2=ll.e_REsq*ll.v_inv
		e3s3=e2s2*e1s1
		e1s2=e1s1*self.v_inv05
		e1s3=e1s1*ll.v_inv
		e2s3=e2s2*self.v_inv05
		f_F=self.f_F
		for i in [0,1]:
			if self.panel.input.tobit_active[i]:
				I=self.panel.tobit_I[i]
				f_F2=self.f_F[i]**2
				d2LL_de2[I]=      -(g[i]*f_F[i]*e1s3[I] + f_F2*ll.v_inv[I])
				d2LL_dln_de[I] =   0.5*(f_F2*e1s2[I]  +  g[i]*f_F[i]*(e2s3[I]-self.v_inv05[I]))
				d2LL_dln2[I] =     0.25*(f_F2*e2s2[I]  +  g[i]*f_F[i]*(e1s1[I]-e3s3[I]))

	def calc_hessian(self,ll,its):
		I=self.I
		ll=self.ll
		d2LL_de2=-ll.v_inv*self.panel.included
		d2LL_dln_de=ll.e_RE*ll.v_inv*self.panel.included
		d2LL_dln_de*=ll.dlnv_pos
		d2LL_dln2=-0.5*ll.e_REsq*ll.v_inv*self.panel.included	
		d2LL_dln2*=ll.dlnv_pos
		self.LL_hessian_tobit(ll, d2LL_de2, d2LL_dln_de, d2LL_dln2)
		self.H=self.hessian.get(ll,self.mp,d2LL_de2,d2LL_dln_de,d2LL_dln2)
		
		if self.dx_norm is None:
			m=10
		else:
			m=max(self.dx_norm**2)
		self.H=(self.H+m*I*self.H)/(1+m)	

	
	def init_ll(self,args):
		self.constr=cnstr.constraints(self.panel,args)
		cnstr.add_static_constraints(self.constr,self.panel,None,0)	
		ll=logl.LL(args, self.panel, constraints=self.constr,print_err=True)
		if ll.LL is None:
			if self.panel.settings.loadargs.value:
				print("Initial arguments failed, attempting default OLS-arguments ...")
				self.panel.args.set_init_args(True)
				ll=logl.LL(self.panel.args.args_OLS,self.panel,constraints=self.constr,print_err=True)
				if ll.LL is None:
					raise RuntimeError("OLS-arguments failed too, you should check the data")
				else:
					print("default OLS-arguments worked")
			else:
				raise RuntimeError("OLS-arguments failed, you should check the data")
				
		return ll
	
	def normalize(self,dx,args_v):
		dx_norm=(args_v!=0)*dx/(np.abs(args_v)+(args_v==0))
		dx_norm=(args_v<1e-2)*dx+(args_v>=1e-2)*dx_norm	
		return dx_norm	

def hessin(hessian):
	try:
		h=-np.linalg.inv(hessian)
	except:
		return None	
	return h

def nummerical_hessin(g,g_old,hessin,dxi):
	#Not currently in use
	if dxi is None:
		return None
	dg=g-g_old 				#Compute difference of gradients,
	#and difference times current matrix:
	n=len(g)
	hdg=(np.dot(hessin,dg.reshape(n,1))).flatten()
	fac=fae=sumdg=sumxi=0.0 							#Calculate dot products for the denominators. 
	fac = np.sum(dg*dxi) 
	fae = np.sum(dg*hdg)
	sumdg = np.sum(dg*dg) 
	sumxi = np.sum(dxi*dxi) 
	if (fac > (3.0e-16*sumdg*sumxi)**0.5):#Skip update if fac not sufficiently positive.
		fac=1.0/fac
		fad=1.0/fae 
								#The vector that makes BFGS different from DFP:
		dg=fac*dxi-fad*hdg   
		#The BFGS updating formula:
		hessin+=fac*dxi.reshape(n,1)*dxi.reshape(1,n)
		hessin-=fad*hdg.reshape(n,1)*hdg.reshape(1,n)
		hessin+=fae*dg.reshape(n,1)*dg.reshape(1,n)	
	return hessin


def solve(constr,H, g, x):
	"""Solves a second degree taylor expansion for the dc for df/dc=0 if f is quadratic, given gradient
	g, hessian H, inequalty constraints c and equalitiy constraints c_eq and returns the solution and 
	and index constrained indicating the constrained variables"""
	if H is None:
		raise RuntimeError('Hessian is None')
	if constr is None:
		return -np.linalg.solve(H,g).flatten()	
	n=len(H)
	k=len(constr.constraints)
	H=np.concatenate((H,np.zeros((n,k))),1)
	H=np.concatenate((H,np.zeros((k,n+k))),0)
	g=np.append(g,(k)*[0])
	
	for i in range(k):
		H[n+i,n+i]=1
	j=0
	xi=np.zeros(len(g))
	for i in constr.fixed:
		kuhn_tucker(constr.fixed[i],i,j,n, H, g, x,xi, recalc=False)
		j+=1
	xi=-np.linalg.solve(H,g).flatten()	
	OK=False
	w=0
	for r in range(50):
		j2=j
		
		for i in constr.intervals:
			xi=kuhn_tucker(constr.intervals[i],i,j2,n, H, g, x,xi)
			j2+=1
		OK=constr.within(x+xi[:n],False)
		if OK: 
			break
		if r==k+3:
			#print('Unable to set constraints in direction calculation')
			break

	return xi[:n]


def solve_delete(constr,H, g, x):
	"""Solves a second degree taylor expansion for the dc for df/dc=0 if f is quadratic, given gradient
	g, hessian H, inequalty constraints c and equalitiy constraints c_eq and returns the solution and 
	and index constrained indicating the constrained variables"""
	if H is None:
		return None,g*0
	try:
		list(constr.constraints.keys())[0]
	except:
		return -np.linalg.solve(H,g).flatten()	
	
	m=len(H)
	
	idx=np.ones(m,dtype=bool)
	delmap=np.arange(m)
	if len(list(constr.fixed.keys()))>0:#removing fixed constraints from the matrix
		idx[list(constr.fixed.keys())]=False
		H=H[idx][:,idx]
		g=g[idx]
		delmap-=np.cumsum(idx==False)
		delmap[idx==False]=m#if for some odd reason, the deleted variables are referenced later, an out-of-bounds error is thrown
	n=len(H)
	k=len(constr.intervals)
	H=np.concatenate((H,np.zeros((n,k))),1)
	H=np.concatenate((H,np.zeros((k,n+k))),0)
	g=np.append(g,(k)*[0])
	
	for i in range(k):
		H[n+i,n+i]=1
	xi=-np.linalg.solve(H,g).flatten()	
	xi_full=np.zeros(m)
	OK=False
	keys=list(constr.intervals.keys())
	for r in range(50):		
		for j in range(k):
			key=keys[j]
			xi=kuhn_tucker_del(constr,key,j,n, H, g, x,xi,delmap)
		xi_full[idx]=xi[:n]
		OK=constr.within(x+xi_full,False)
		if OK: 
			break
		if r==k+3:
			#print('Unable to set constraints in direction calculation')
			break
	xi_full=np.zeros(m)
	xi_full[idx]=xi[:n]
	return xi_full

def kuhn_tucker_del(constr,key,j,n,H,g,x,xi,delmap,recalc=True):
	q=None
	c=constr.intervals[key]
	i=delmap[key]
	if not c.value is None:
		q=-(c.value-x[i])
	elif x[i]+xi[i]<c.min:
		q=-(c.min-x[i])
	elif x[i]+xi[i]>c.max:
		q=-(c.max-x[i])
	if q!=None:
		H[i,n+j]=1
		H[n+j,i]=1
		H[n+j,n+j]=0
		g[n+j]=q
		if recalc:
			xi=-np.linalg.solve(H,g).flatten()	
	return xi


def kuhn_tucker(c,i,j,n,H,g,x,xi,recalc=True):
	q=None
	if not c.value is None:
		q=-(c.value-x[i])
	elif x[i]+xi[i]<c.min:
		q=-(c.min-x[i])
	elif x[i]+xi[i]>c.max:
		q=-(c.max-x[i])
	if q!=None:
		H[i,n+j]=1
		H[n+j,i]=1
		H[n+j,n+j]=0
		g[n+j]=q
		if recalc:
			xi=-np.linalg.solve(H,g).flatten()	
	return xi


