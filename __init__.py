'''
copyright @avour: mahartstudio

is a Mixin behaviour that can be mixed with a Scrollview
to give the user a reloading effect on the view
then you get an on_reload event to do whatever you want to

Ex
from kivy.garden.reloadbehavior import ReloadBehavior

class Reloader(ReloadBehavior, ScrollView):
    
    def on_reload(self):
        # do anythin
        print('Reloading........')
    

'''

import os


from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.base import runTouchApp as app
from kivy.clock import Clock
from kivy.core.window import Window

from kivy.garden.iconfonts import iconfonts
font_file = os.path.join(os.path.dirname(__file__), 'font-awesome.fontd')
iconfonts.register('awesome_font', 'font-awesome.ttf',
     font_file)


class Rotater(Label):

    angle = NumericProperty(0)

    anim = Animation(angle=360, duration=0.45) + Animation(angle=0, duration=0)

    is_reloading = False

    def reload_anim(self):
        self.anim.repeat = True
        self.anim.start(self)
        self.is_reloading = True
        Clock.schedule_once(self.stop_anim, 2.5)

    def stop_anim(self, *a):
        self.is_reloading = False
        self.anim.cancel(self)
        self.parent.remove_widget(self)


class ReloadBehavior(object):

    minimum_drag_height = NumericProperty(110)
    ''' minimum height the rotater widget should be draged
        NumericProperty and defualts to 110'''

    _rotater = ObjectProperty(None)
    ''' widget that rows down when user drags down to reload
    '''

    __events__ = ('on_reload',)

    def __init__(self, **k):
        super(ReloadBehavior, self).__init__(**k)
        self.effect_cls = 'ScrollEffect'
        self.calc_steps()
        self._rotater = Rotater()

    def on_reload(self):
        'default handler'

    def on_touch_move(self,touch):
        if self.collide_point(*touch.pos):
            if self._rotater.is_reloading:
                return False

            if int(self.scroll_y) >= 1:
                if self._rotater not in Window.children:

                    self.parent.add_widget(self._rotater)

                    self._rotater.center_x=self.center[0]
                    self._rotater.y = self.height
                    self._rotater.angle = 0

                if touch.dy < 0:
                    self.drag_down()
                else:
                    self.drag_up()
                    return super(ReloadBehavior,self).on_touch_move(touch)
                
                return True

        return super(ReloadBehavior, self).on_touch_move(touch)

    def on_touch_up(self,touch):
        if self._rotater in Window.children:
            if self._rotater.is_reloading:
                return False

            if self._rotater.angle > 180:
                self.reload()
            else:
                Window.remove_widget(self._rotater)

        super(ReloadBehavior, self).on_touch_up(touch)


    def on_minimum_drag_height(self, *a):
        self.calc_steps()

    def calc_steps(self):
        self._dis_step = 2.5
        self._angle_step = 360.0/float(self.minimum_drag_height/self._dis_step)


    def drag_down(self):
        if not(self._rotater.angle >= 360):
            self._rotater.y -= self._dis_step
            self._rotater.angle += self._angle_step

    def drag_up(self):
        if not(self._rotater.angle <= 0):
            self._rotater.y += self._dis_step
            self._rotater.angle -= self._angle_step

    def reload(self):
        self.dispatch('on_reload')
        self._rotater.center_y = self.height-50
        self._rotater.reload_anim()



Builder.load_string('''
#: import icon kivy.garden.iconfonts.icon

<Rotater>:
    size_hint: None,None
    text: '%s'% (icon('fa-rotate-left'))
    markup: True
    on_text: print(self.text)
    size: '32dp','32dp'
    canvas.before:
        Clear
        Color:
            rgba: 1,1,1,1
        Ellipse:
            size: self.size
            pos: self.pos
    canvas.after:
        Color:
            rgba: .4,.4,.4,1
        Line:
            ellipse: [self.x,self.y,self.width,self.height]
            width: 1.0

        PushMatrix:
        Rotate:
            angle: 45
            origin: self.center_x,self.center_y
        Rotate:
            angle: root.angle
            origin: self.center_x,self.center_y
        Color:
            rgba: 0,0,0,1
        Rectangle:
            texture: self.texture
            size: self.texture_size
            pos: self.center_x-self.texture_size[0]/2, self.center_y-self.texture_size[1]/2
        PopMatrix:


''')

if __name__ == '__main__':
    grid = Builder.load_string('''
GridLayout:
    size_hint_y: None
    height: self.minimum_height
    cols: 1
    ''')

    class Reloader(ReloadBehavior, ScrollView):
        
        def on_reload(self):
            # do anythin
            print('Reloading........')
    
    reloader = Reloader()
    reloader.add_widget(grid)
    for i in range(20):
        grid.add_widget(Button(size_hint_y=None,
        text=str(i+1), height='46dp'))

    app(reloader)
