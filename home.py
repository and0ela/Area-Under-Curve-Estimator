import math
import streamlit as st
import numpy as numpy
import plotly.express as px
import plotly.graph_objects as go


def f(x):
  return ((4*x) - (x**3))

def ff(func,x):
  try:
    return eval(func)
  except:
    st.warning("Please enter a valid function.")


def L(func,lb, rb, nr):
  sum = 0
  x = lb
  for i in range((nr)):
    sum = sum + ff(func,x)
    x = x + ((rb - lb) / nr)
    #print(i)
    #print(sum)
  return ((rb - lb) / nr) * (sum)


def R(func,lb, rb, nr):
  sum = 0
  x = lb + ((rb - lb) / nr)
  for i in range((nr)):
    sum = sum + ff(func,x)
    x = x + ((rb - lb) / nr)
    #print(i)
    #print(sum)
  return ((rb - lb) / nr) * (sum)


def M(func,lb, rb, nr):
  sum = 0
  x = lb + (0.5 * ((rb - lb) / nr))
  for i in range((nr)):
    sum = sum + ff(func,x)
    x = x + ((rb - lb) / nr)
    #print(i)
    #print(sum)
  return ((rb - lb) / nr) * (sum)


def T(func,lb, rb, nr):
  sum = 0
  x = lb
  inter = (rb - lb) / nr
  for i in range(nr):
    #print(f(x))
    sum = sum + (inter*(ff(func,x) + ff(func,x + inter)))
    x = x + inter
  return ( 0.5) * (sum)


#num_rec = 4
#left_bound = 0
#right_bound = 2



def populate(f,lb,rb,nr):
  try:
    Ln = L(f,lb, rb, nr)
    Rn = R(f,lb, rb, nr)
    Mn = M(f,lb, rb, nr)
    Tn = T(f,lb, rb, nr)
    return Ln,Rn,Mn,Tn
  except:
    return None

def main_page():
  st.title("Area-Under-The-Curve Calculator")
  
  col1,col2 = st.columns(2)
  with col1:
    func = st.text_input("Please input your function!",value='x' )
    
    st.caption("Please format your equation using * for multiplication, / for division, and ** for exponents, and use parentheses when necessary!!")
    left_bound = st.number_input("Left Bound")
    right_bound = st.number_input("Right Bound")
    if right_bound < left_bound:
      st.warning("Please ensure that your left bound is less than your right bound!")
    num_rec = st.number_input("Rectangles",0,None,4,1)
    st.write(func)
    populated = populate(func,left_bound,right_bound,num_rec)
    #st.write(populated)
    #st.write(type(populated))
    if populated is not None:
      print_vals(round(populated[0],4),round(populated[1],4),round(populated[2],4),round(populated[3],4))

      with col2:
        x1 = []
        y1 = []
        data = [x1,y1]

        
        #for i in range(round(left_bound),round(right_bound)+1):
        if left_bound != right_bound:
          i = round(left_bound)
          while i < round(right_bound):
            x1.append(i)
            y1.append(ff(func,i))
            i = i+0.1
            
          fig = px.line(x=x1,y=y1, line_shape="spline")
          fig.add_hline(y=0, line_color='white',line_width = 0.5) 
          fig.add_vline(x=0, line_color='white',line_width = 0.5)
          fig.update_xaxes(showline=True, linewidth=2, linecolor='white')
          fig.update_yaxes(showline=True, linewidth=2, linecolor='white')
          plot_spot = st.empty()

          interval = ((right_bound - left_bound) / num_rec)
        #px.histogram(x=x1,y=y1)
          if st.button("Show Right Endpoints"):
            
            leftx = left_bound
            rightx = left_bound + interval
            lefty = 0
            righty = ff(func,rightx)
            for i in range(num_rec):
              fig.add_shape(type="rect",
                x0=leftx,y0=lefty,x1=rightx,y1=righty,
                line=dict(
                  color="RoyalBlue",
                  width=2,
                ),
                
                )
              leftx = rightx
              rightx = leftx + interval
              lefty = 0
              righty = ff(func,rightx)

          if st.button("Show Left Endpoints"):
            #interval = ((right_bound - left_bound) / num_rec)
            leftx = left_bound
            rightx = left_bound + interval
            lefty = 0
            righty = ff(func,leftx)
            for i in range(num_rec):
              fig.add_shape(type="rect",
                x0=leftx,y0=lefty,x1=rightx,y1=righty,
                line=dict(
                  color="RoyalBlue",
                  width=2,
                ),
                
                )
              leftx = rightx
              rightx = leftx + interval
              lefty = 0
              righty = ff(func,leftx)


          if st.button("Show Midpoints"):
            #interval = ((right_bound - left_bound) / num_rec)
            leftx = left_bound
            rightx = left_bound + interval
            lefty = 0
            righty = ff(func,(leftx+rightx)/2)
            for i in range(num_rec):
              fig.add_shape(type="rect",
                x0=leftx,y0=lefty,x1=rightx,y1=righty,
                line=dict(
                  color="RoyalBlue",
                  width=2,
                ),
                
                )
              leftx = rightx
              rightx = leftx + interval
              lefty = 0
              righty = ff(func,(leftx+rightx)/2)

          if st.button("Show trapezoids"):
            trapx = []
            trapy = []
            leftx = left_bound
            rightx = left_bound + interval
            lefty = ff(func,leftx)
            righty = ff(func,rightx)
            trapx.extend((leftx,leftx,rightx,rightx,leftx))
            trapy.extend((0,lefty,righty,0,0))
            for i in range(num_rec-1):
              trapx.append("None")
              trapy.append("None")
              leftx = rightx
              rightx = leftx + interval
              lefty = ff(func,leftx)
              righty = ff(func,rightx)
              trapx.extend((leftx,leftx,rightx,rightx,leftx))
              trapy.extend((0,lefty,righty,0,0))
            fig.add_trace(go.Scatter(x=trapx,y=trapy,showlegend=False))

            '''''
            trapx = []
            trapy = []
            leftx = left_bound
            rightx = left_bound + interval
            lefty = ff(func,leftx)
            righty = ff(func,rightx)
            trapx.extend((leftx,leftx,rightx,rightx))
            trapy.extend((0,lefty,righty,0))
            for i in range(num_rec*2):
              fig.add_trace(go.Scatter(x=trapx,y=trapy))
              trapx.extend("None")
              leftx = rightx
              rightx = leftx + interval
              lefty = ff(func,leftx)
              righty = ff(func,rightx)
              trapx.extend((leftx,leftx,rightx,rightx))
              trapy.extend((0,lefty,righty,0))
              '''''
            

          with plot_spot:
            st.plotly_chart(fig,use_container_width=True)
          #st.write(x1)
          #st.write(y1)




def print_vals (Ln,Rn,Mn,Tn):

  st.write("L: ", Ln)
  st.write("R: ", Rn)
  st.write("M: ", Mn)
  st.write("T: ", Tn)


main_page()

