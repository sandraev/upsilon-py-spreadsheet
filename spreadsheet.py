# Spreadsheet V1 (beta)
# Made by Sandraev
# --- A spreadsheet template for Upsilon in Python

from math import *
from kandinsky import *
from ion import *
from time import sleep

BGCOLOR = [0,0,0]
CELL_W = 18*3
CELL_H = 18
CELL_COLORS = [[(0,0,20),(160,160,255)],[(0,0,20),(120,120,215)]]
SHEET_W = 5
SHEET_H = 8

active_cell = [0,0,1,1]
key_match = {"shift":"=","exp":"A","ln":"B","log":"C","imaginary":"D","comma":"E","power":"F","sin":"G","cos":"H","tan":"I","pi":"J","sqrt":"K","square":"L","7":"M","8":"N","9":"O","(":"P",")":"Q","4":"R","5":"S","6":"T","*":"U","/":"V","1":"W","2":"X","3":"Y","+":"Z"}
math_keys = ["(",")","*","/","+","-","."]
numbers = ["0","1","2","3","4","5","6","7","8","9"]

def render(value,app):
  new_value = ""
  if len(value) > 0:
    if value[0] == "=":
      list_value = []
      for i in value:
        list_value.append(i)
      print(list_value)
      cellx = 0
      celly = 0
      skip = False
      for v in list_value:
        if skip:
          skip = False
          continue
        if v in letters:
          cellx = letters.index(v)
          if list_value[list_value.index(v)+1] in numbers:
            celly = list_value[list_value.index(v)+1]
            skip = True
            new_value += str(app.sheet[int(cellx)][int(celly)].value)
        if v in math_keys:
          new_value += v
        if v in numbers:
          new_value += v
    else:
      new_value = value
  print(new_value)
  return new_value

class Button():
  def __init__(self,x,y,w,h,color,bgcolor):
    self.x,self.y,self.w,self.h = x,y,w,h
    self.color,self.bgcolor = color,bgcolor
    self.is_active = False

class MainButton(Button):
  def draw(self):
    if self.is_active:
      fill_rect(self.x,self.x,self.w,self.h,self.color)
      fill_rect(self.x+2,self.y+3,14,2,self.bgcolor)
      fill_rect(self.x+2,self.y+8,14,2,self.bgcolor)
      fill_rect(self.x+2,self.y+13,14,2,self.bgcolor)
    else:
      fill_rect(self.x,self.x,self.w,self.h,self.bgcolor)
      fill_rect(self.x+2,self.y+3,14,2,self.color)
      fill_rect(self.x+2,self.y+8,14,2,self.color)
      fill_rect(self.x+2,self.y+13,14,2,self.color)

class Menu():
  def __init__(self,x,y,w,h,txtcolor,bgcolor):
    self.x,self.y,self.w,self.h = x,y,w,h
    self.txtcolor,self.bgcolor = txtcolor,bgcolor
    self.is_active = False
    self.entry_active = 0
    self.entries = []
  def draw(self):
    for kword,entry in self.entries:
      if self.entry_active == self.entries.index((kword,entry)):
        fill_rect(self.x,self.y+(self.entries.index((kword,entry))*self.h),self.w,self.h,self.txtcolor)
        draw_string(entry,self.x+4,self.y+3+(self.entries.index((kword,entry))*self.h),self.bgcolor,self.txtcolor,1)
      else:
        fill_rect(self.x,self.y+(self.entries.index((kword,entry))*self.h),self.w,self.h,self.bgcolor)
        draw_string(entry,self.x+4,self.y+3+(self.entries.index((kword,entry))*self.h),self.txtcolor,self.bgcolor,1)
  def erase(self):
    fill_rect(self.x,self.y,self.w,self.h*len(self.entries),BGCOLOR)

class MainMenu(Menu):
  def __init__(self,*arg):
    super().__init__(*arg)
    self.entries = [("save","Save sheet"),("about","About"),("quit","Quit [MENU]")]

class Popup():
  def __init__(self,title,txt,color,bgcolor):
    self.title,self.txt = title,txt
    self.color,self.bgcolor = color,bgcolor
    self.w = 180
    self.h = 4+10+5+10*5+4
    self.x = 160-int(self.w/2)
    self.y = 111-int(self.h/2)
    self.line_size = int((self.w-10)/7)
    self.line_nb = int(len(self.txt)/self.line_size)
    self.is_active = False
  def draw(self):
    fill_rect(self.x,self.y,self.w,self.h,self.bgcolor)
    draw_line(self.x+1,self.y+1,self.x-2+self.w,self.y+1,BGCOLOR)
    draw_line(self.x-2+self.w,self.y+1,self.x-2+self.w,self.y-1+self.h,BGCOLOR)
    draw_line(self.x-2+self.w,self.y-2+self.h,self.x+1,self.y-2+self.h,BGCOLOR)
    draw_line(self.x+1,self.y-2+self.h,self.x+1,self.y+1,BGCOLOR)
    draw_string(self.title,self.x+(160-self.x)-int(len(self.title)*7/2),self.y+4,self.color,self.bgcolor,1)
    x,y=0,0
    for letter in self.txt:
      draw_string(letter,self.x+4+x*7,self.y+19+y,self.color,self.bgcolor,1)
      x+=1
      if x == self.line_size:
        x=0
        y+=13
  def erase(self):
    fill_rect(self.x,self.y,self.w,self.h,BGCOLOR)

class Bar():
  def __init__(self,txt,color,bgcolor):
    self.txt = txt
    self.color,self.bgcolor = color,bgcolor

class Header(Bar):
  def __init__(self,*arg):
    super().__init__(*arg)
    self.alpha = 0
  def draw(self):
    fill_rect(0,0,320,18,self.bgcolor)
    draw_string(self.txt,160-int(len(self.txt)*7/2),3,self.color,self.bgcolor,1)
    if self.alpha:
      if self.alpha == 1:
        draw_string("alpha",320-7*6,3,self.color,self.bgcolor,1)
      else:
        draw_string("[alpha]",320-7*7,3,self.color,self.bgcolor,1)

class Footer(Bar):
  def draw(self,app):
    txt = str(letters[active_cell[0]])+str(active_cell[1])+": "+str(app.sheet[active_cell[0]][active_cell[1]].value)
    fill_rect(0,222-18,320,18,self.bgcolor)
    draw_string(txt+" ",3,222-18+3,self.color,self.bgcolor,1)
  def edit(self,app,header):
    self.alpha_once = False
    self.alpha_toogle = False
    self.txt = app.sheet[active_cell[0]][active_cell[1]].value
    draw_string(" "+self.txt+"_",3+7*3,222-18+3,self.color,self.bgcolor,1)
    sleep(0.1)
    while True:
      if get_keys() != set():
        cin = get_keys()
        if len(cin) == 1:
          cin = cin.pop()
          if not self.alpha_once and not self.alpha_toogle:
            try:
              cin = int(cin)
              self.txt += str(cin)
            except:
              if cin in math_keys:
                self.txt += cin
              if cin == "backspace":
                txt = ""
                for l in range(len(self.txt)-1):
                  txt += self.txt[l]
                self.txt = txt
              elif cin == "alpha":
                self.alpha_once = True
                header.alpha = 1
                draw_header()
              elif cin == "EXE":
                return self.txt
          else:
            if cin == "alpha":
              if self.alpha_toogle:
                self.alpha_toogle = False
                header.alpha = 0
                draw_header()
              if self.alpha_once:
                self.alpha_toogle = True
                header.alpha = 2
                draw_header()
            else:
              try:
                self.txt += key_match[cin]
              except:
                self.txt += '"'
            self.alpha_once = False
            if not self.alpha_toogle:
              header.alpha = 0
              draw_header()
          draw_string(" "+self.txt+"_"+" ",3+7*3,222-18+3,self.color,self.bgcolor,1)
          while get_keys() != set(): pass

class App():
  def __init__(self,x,y,w,h,bgcolor,brd_Grid,cl_Grid):
    self.x,self.y,self.w,self.h = x,y,w,h
    self.bgcolor = bgcolor
    self.content = []
    self.sheet = []
    self.brd_Grid = brd_Grid
    self.cl_Grid = cl_Grid
  def add_content(self,content):
    self.content.append(content)
  def add_sheet(self,sheet):
    self.sheet.append(sheet)
  def draw(self):
    fill_rect(self.x,self.y,self.w,self.h,self.bgcolor)
    for c in self.content:
      c.draw(self.brd_Grid,self)
    for c in self.sheet:
      for d in c:
#        try:
        d.draw(self.cl_Grid,self,1)
#        except:
#          for e in d:
#            e.draw(self.cl_Grid,self,1)
  def refresh_cnt_cell(self,cell_id):
    try:
      self.sheet[cell_id[0]].draw(self.cl_Grid,self,1)
    except:
      self.sheet[cell_id[0]][cell_id[1]].draw(self.cl_Grid,self,1)

class Grid():
  def __init__(self,origin_x=0,origin_y=18,case_w=CELL_W,case_h=CELL_H):
    self.origin_x = origin_x
    self.origin_y = origin_y
    self.case_w = case_w
    self.case_h = case_h
    self.w_separator = 2
  def get_pos(self,grid_place,xlag=0):
    x = self.origin_x+2+grid_place[0]*(self.case_w+self.w_separator)-xlag
    y = self.origin_y+2+grid_place[1]*(self.case_h+self.w_separator)
    return x,y,int(self.case_w*grid_place[2]),int(self.case_h*grid_place[3])

class Cell():
  def __init__(self,grid_place,color=0,value=0,xlag=0):
    self.grid_place = grid_place
    self.value = value
    self.color = color
    self.xlag = xlag
  def draw(self,Grid,app,rendering=False):
    x,y,w,h = Grid.get_pos(self.grid_place,self.xlag)
    if rendering: 
      value = render(self.value,app)
      txt = str(value)
    else: txt = str(self.value)
    if len(txt) > 7:
      txt = ""
      for i in range(7):
        txt += str(self.value)[i]
    if active_cell == self.grid_place:
      fill_rect(x,y,w,h,CELL_COLORS[self.color][0])
      draw_string(txt,x+3,y+3,CELL_COLORS[self.color][1],CELL_COLORS[self.color][0],1)
    else:
      fill_rect(x,y,w,h,CELL_COLORS[self.color][1])
      draw_string(txt,x+3,y+3,CELL_COLORS[self.color][0],CELL_COLORS[self.color][1],1)

header = Header("SPREADSHEET",[220,220,255],[50,50,100])
footer = Footer("[None]",[220,220,255],[100,100,160])
mb = MainButton(0,0,18,18,[220,220,255],[50,50,100])
mm = MainMenu(0,18,18*8,18,[220,220,255],[100,100,160])
about = Popup("ABOUT:","Spreadsheet is a model of app for Upsilon, written in Python",[220,220,255],[100,100,160])
border_grid = Grid()
cell_grid = Grid(origin_x=38,origin_y=38)
app = App(0,18,320,222-18*2,BGCOLOR,border_grid,cell_grid)

letters = "ABCDEFGHIJKMNOPQRSTUVWXYZ"
top_cells = []
for i in range(SHEET_W):
  top_cells.append(Cell([i+1,0,1,1],1,letters[i],xlag=18))
  app.add_content(top_cells[i])
left_cells = []
for i in range(SHEET_H):
  left_cells.append(Cell([0,i+1,3**(-1)*2,1],1,str(i)))
  app.add_content(left_cells[i])

center_cells = []
for w in range(SHEET_W):
  line = []
  for h in range(SHEET_H):
    line.append(Cell([w,h,1,1],0,"0"))
  center_cells.append(line)
  app.add_sheet(line)

def draw_header():
  header.draw()
  mb.draw()

def draw_all():
  app.draw()
  draw_header()
  footer.draw(app)

draw_all()

while True:
  if keydown(KEY_HOME) and not about.is_active:
    mb.is_active = not mb.is_active
    mb.draw()
    if mb.is_active:
      mm.entry_active = 0
      mm.draw()
    else:
      mm.erase()
      draw_all()
    while keydown(KEY_HOME): pass
  if mb.is_active:
    if keydown(KEY_DOWN) and mm.entry_active != len(mm.entries)-1:
      mm.entry_active += 1
      mm.draw()
      while keydown(KEY_DOWN): pass
    if keydown(KEY_UP) and mm.entry_active:
      mm.entry_active -= 1
      mm.draw()
      while keydown(KEY_UP): pass
    if keydown(KEY_OK):
      if mm.entries[mm.entry_active][0] == "quit":
        mm.erase()
        mb.is_active = False
        mb.draw()
        fill_rect(0,0,320,222,BGCOLOR)
        raise SystemExit
      elif mm.entries[mm.entry_active][0] == "about":
        mm.erase()
        mb.is_active = False
        mb.draw()
        draw_all()
        about.draw()
        about.is_active = True
        while keydown(KEY_OK): pass
  if about.is_active:
    if keydown(KEY_OK):
      about.erase()
      about.is_active = False
      draw_all()
      while keydown(KEY_OK): pass
  if not about.is_active and not mb.is_active:
    if keydown(KEY_LEFT) and active_cell[0] != 0:
      active_cell[0] -= 1
      app.refresh_cnt_cell([active_cell[0]+1,active_cell[1]])
      app.refresh_cnt_cell([active_cell[0],active_cell[1]])
      footer.draw(app)
      while keydown(KEY_LEFT): pass
    if keydown(KEY_RIGHT) and active_cell[0]+1 < SHEET_W:
      active_cell[0] += 1
      app.refresh_cnt_cell([active_cell[0],active_cell[1]])
      app.refresh_cnt_cell([active_cell[0]-1,active_cell[1]])
      footer.draw(app)
      while keydown(KEY_RIGHT): pass
    if keydown(KEY_UP) and active_cell[1] != 0:
      active_cell[1] -= 1
      app.refresh_cnt_cell([active_cell[0],active_cell[1]+1])
      app.refresh_cnt_cell([active_cell[0],active_cell[1]])
      footer.draw(app)
      while keydown(KEY_UP): pass
    if keydown(KEY_DOWN) and active_cell[1]+1 < SHEET_H:
      active_cell[1] += 1
      app.refresh_cnt_cell([active_cell[0],active_cell[1]])
      app.refresh_cnt_cell([active_cell[0],active_cell[1]-1])
      footer.draw(app)
      while keydown(KEY_DOWN): pass
    if keydown(KEY_OK):
      app.sheet[active_cell[0]][active_cell[1]].value = footer.edit(app,header)
      footer.draw(app)
      app.draw()
