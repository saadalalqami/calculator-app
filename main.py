from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
import math

class CalculatorLayout(BoxLayout):
    display_text = StringProperty('0')
    history_list = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expression = ''
        self.last_result = None
        
    def on_button_press(self, button):
        """معالجة الضغط على الأزرار"""
        if button == 'C':
            self.expression = ''
            self.display_text = '0'
        elif button == '⌫':
            self.expression = self.expression[:-1]
            self.display_text = self.expression if self.expression else '0'
        elif button == '=':
            try:
                # استبدال الرموز
                expr = self.expression.replace('×', '*').replace('÷', '/')
                # تقييم العملية
                result = eval(expr, {"__builtins__": None}, {
                    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                    'sqrt': math.sqrt, 'log': math.log10, 'ln': math.log
                })
                # حفظ في التاريخ
                self.history_list.insert(0, f"{self.expression} = {result}")
                if len(self.history_list) > 10:
                    self.history_list.pop()
                # عرض النتيجة
                self.display_text = str(result)
                self.expression = str(result)
                self.last_result = result
            except Exception as e:
                self.display_text = 'خطأ'
                Clock.schedule_once(lambda dt: self.clear_error(), 1)
        else:
            self.expression += button
            self.display_text = self.expression
            
    def clear_error(self):
        self.display_text = self.expression if self.expression else '0'
        
    def scientific_function(self, func):
        """معالجة الدوال العلمية"""
        try:
            current = float(self.display_text) if self.display_text != '0' else 0
            if func == 'sin':
                result = math.sin(math.radians(current))
            elif func == 'cos':
                result = math.cos(math.radians(current))
            elif func == 'tan':
                result = math.tan(math.radians(current))
            elif func == '√':
                result = math.sqrt(current)
            elif func == 'log':
                result = math.log10(current)
            
            self.display_text = str(result)
            self.expression = str(result)
            self.history_list.insert(0, f"{func}({current}) = {result}")
        except:
            self.display_text = 'خطأ'
            Clock.schedule_once(lambda dt: self.clear_error(), 1)
            
    def clear_history(self):
        self.history_list.clear()

class CalculatorApp(App):
    def build(self):
        return CalculatorLayout()

if __name__ == '__main__':
    CalculatorApp().run()
