
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import functions as fu

class re_obj:
	def __init__(self,panel,group,T_i,T_i_count,fixed_random_eff):
		"""Following Greene(2012) p. 413-414"""
		self.panel=panel
		self.sigma_u=0
		self.group=group
		self.avg_Tinv=np.mean(1/T_i_count) #T_i_count is the total number of observations for each group (N,1)
		self.T_i=T_i*panel.included#self.T_i is T_i_count at each observation (N,T,1)
		self.FE_RE=fixed_random_eff
	
	def RE(self,x,recalc=True):
		panel=self.panel
		if self.FE_RE==0:
			return 0*panel.included
		if self.FE_RE==1:
			self.xFE=self.FRE(x)
			return self.xFE
		if recalc:
			N,T,k=x.shape
			
			self.xFE=(x+self.FRE(x))*panel.included
			self.e_var=self.panel.mean(self.xFE**2)/(1-self.avg_Tinv)
			self.v_var=self.panel.mean((panel.included*x)**2)-self.e_var
			if self.v_var<0:
				#print("Warning, negative group random effect variance. 0 is assumed")
				self.v_var=0
				self.theta=panel.zeros
				return panel.zeros
				
			#self.e_var=0.01693374924097458
			#self.v_var=0.0005709978136967248
			self.theta=(1-np.sqrt(self.e_var/(self.e_var+self.v_var*self.T_i)))*self.panel.included
			self.theta*=(self.T_i>1)
			if np.any(self.theta>1) or np.any(self.theta<0):
				raise RuntimeError("WTF")
		#x=panel.Y
		eRE=self.FRE(x,self.theta)
		return eRE
	
	def dRE(self,dx,x,vname):
		"""Returns the first and second derivative of RE"""
		panel=self.panel
		if not hasattr(self,'dxFE'):
			self.dxFE=dict()
			self.dFE_var=dict()
			self.dtheta=dict()
			self.de_var=dict()
			self.dv_var=dict()
		
		if dx is None:
			return None
		if self.FE_RE==0:
			return 0*panel.included
		elif self.FE_RE==1:
			return self.FRE(dx)	
		if self.v_var==0:
			return panel.zeros
		(N,T,k)=dx.shape	

		self.dxFE[vname]=(dx+self.FRE(dx))*panel.included
		self.de_var[vname]=2*np.sum(np.sum(self.xFE*self.dxFE[vname],0),0)/(self.panel.NT*(1-self.avg_Tinv))
		self.dv_var[vname]=(2*np.sum(np.sum(x*dx*panel.included,0),0)/self.panel.NT)-self.de_var[vname]
		

		

		self.dtheta_de_var=(-0.5*(1/self.e_var)*(1-self.theta)*self.theta*(2-self.theta))
		self.dtheta_dv_var=(0.5*(self.T_i/self.e_var)*(1-self.theta)**3)
		self.dtheta[vname]=(self.dtheta_de_var*self.de_var[vname]+self.dtheta_dv_var*self.dv_var[vname])
		self.dtheta[vname]*=(self.T_i>1)
		dRE0=self.FRE(dx,self.theta)
		dRE1=self.FRE(x,self.dtheta[vname])
		return (dRE0+dRE1)*self.panel.included
	
	def ddRE(self,ddx,dx1,dx2,x,vname1,vname2):
		"""Returns the first and second derivative of RE"""
		panel=self.panel
		if dx1 is None or dx2 is None:
			return None
		(N,T,k)=dx1.shape
		(N,T,m)=dx2.shape			
		if self.FE_RE==0 or self.sigma_u<0:
			return 0*panel.included.reshape((N,T,1,1))
		elif self.FE_RE==1:
			return self.FRE(ddx)	
		if self.v_var==0:
			return panel.zeros.reshape((N,T,1,1))

		if ddx is None:
			ddxFE=0
			ddx=0
			hasdd=False
		else:
			ddxFE=(ddx+self.FRE(ddx))*panel.included.reshape(N,T,1,1)
			hasdd=True
			
		dxFE1=self.dxFE[vname1].reshape(N,T,k,1)
		dxFE2=self.dxFE[vname2].reshape(N,T,1,m)
		dx1=dx1.reshape(N,T,k,1)
		dx2=dx2.reshape(N,T,1,m)
		de_var1=self.de_var[vname1].reshape(k,1)
		de_var2=self.de_var[vname2].reshape(1,m)
		dv_var1=self.dv_var[vname1].reshape(k,1)
		dv_var2=self.dv_var[vname2].reshape(1,m)		
		dtheta_de_var=self.dtheta_de_var.reshape(N,T,1,1)
		dtheta_dv_var=self.dtheta_dv_var.reshape(N,T,1,1)
		theta=self.theta.reshape(N,T,1,1)
		T_i=self.T_i.reshape(N,T,1,1)
		x=x.reshape(N,T,1,1)
		incl=panel.included.reshape(N,T,1,1)
		

	
		
		d2e_var=2*np.sum(np.sum(dxFE1*dxFE2+self.xFE.reshape(N,T,1,1)*ddxFE,0),0)/(self.panel.NT*(1-self.avg_Tinv))
		d2v_var=(2*np.sum(np.sum((dx1*dx2+x*ddx)*incl,0),0)/self.panel.NT)-d2e_var	
		
		d2theta_d_e_v_var=-0.5*dtheta_dv_var*(1/self.e_var)*(3*(theta-2)*theta+2)
		d2theta_d_v_var =-0.75*(T_i/self.e_var)**2*(1-theta)**5
		d2theta_d_e_var =-0.5*dtheta_de_var*(1/self.e_var)*(4-3*(2-theta)*theta)	
		
		ddtheta  =d2theta_d_e_var  * de_var1* de_var2 
		ddtheta +=d2theta_d_e_v_var * (de_var1* dv_var2+dv_var1* de_var2)
		ddtheta +=d2theta_d_v_var * dv_var1* dv_var2  
		ddtheta +=dtheta_de_var*d2e_var+dtheta_dv_var*d2v_var
		ddtheta*=(T_i>1)
	
		if hasdd:
			dRE00=self.FRE(ddx,self.theta.reshape(N,T,1,1))
		else:
			dRE00=0
		dRE01=self.FRE(dx1,self.dtheta[vname2].reshape(N,T,1,m),True)
		dRE10=self.FRE(dx2,self.dtheta[vname1].reshape(N,T,k,1),True)
		dRE11=self.FRE(x,ddtheta,True)
		return (dRE00+dRE01+dRE10+dRE11)*panel.included.reshape(N,T,1,1)
	
	def FRE(self,x,w=1,d=False):
		if self.group:
			return self.FRE_group(x,w,d)
		else:
			return self.FRE_time(x,w,d)
	
	def FRE_group(self,x,w,d):
		"""returns x after fixed effects, and set lost observations to zero"""
		#assumes x is a "N x T x k" matrix
		if x is None:
			return None
		T_i,s=get_subshapes(self.panel,x,True)
		incl=self.panel.included.reshape(s[1])
		
		sum_x=np.sum(x*incl,1).reshape(s[0])
		mean_x=sum_x/T_i
		mean_x_all=np.sum(sum_x,0)/self.panel.NT
		
		dFE=w*(mean_x_all-mean_x)*incl#last product expands the T vector to a TxN matrix
		return dFE
	
	def FRE_time(self,x,w,d):
		#assumes x is a "N x T x k" matrix
		
		
		if x is None:
			return None
		mean_x,mean_x_all,incl=mean_time(self.panel, x)
		dFE=(w*(mean_x_all-mean_x))*incl#last product expands the T vector to a TxN matrix
		return dFE
	
def mean_time(panel,x,mean_dates=False):
	n_dates=panel.n_dates
	dmap=panel.date_map
	date_count,s=get_subshapes(panel,x,False)
	incl=panel.included.reshape(s[1])
	x=x*incl
	sum_x_dates=np.zeros(s[0])
	for i in range(n_dates):
		sum_x_dates[i]=np.sum(x[dmap[i]],0)		
	mean_x_dates=sum_x_dates/date_count
	if mean_dates:
		return mean_x_dates
	mean_x=np.zeros(x.shape)
	for i in range(n_dates):
		mean_x[dmap[i]]=mean_x_dates[i]	
	mean_x_all=np.sum(sum_x_dates,0)/panel.NT
	return mean_x,mean_x_all,incl
	


def get_subshapes(panel,x,group):
	if group:
		if len(x.shape)==3:
			N,T,k=x.shape
			s=((N,1,k),(N,T,1))
			T_i=panel.T_i
		elif len(x.shape)==4:
			N,T,k,m=x.shape
			s=((N,1,k,m),(N,T,1,1))
			T_i=panel.T_i.reshape((N,1,1,1))	
		return T_i,s
	else:
		date_count=panel.date_count
		n_dates=panel.n_dates
		if len(x.shape)==3:
			N,T,k=x.shape
			s=((n_dates,1,k),(N,T,1))
			
		elif len(x.shape)==4:
			N,T,k,m=x.shape
			s=((n_dates,1,k,m),(N,T,1,1))
			date_count=date_count.reshape((n_dates,1,1,1))	
		return date_count,s			