
from sys import platform
import tkinter as tk
from tkinter import ttk
from tkcalendar.calendar_ import Calendar



MAPS = {'winnative': {'focusfill': [('readonly', 'focus', 'SystemHighlight')],
                      'foreground': [('disabled', 'SystemGrayText'),
                                     ('readonly', 'focus', 'SystemHighlightText')],
                      'selectforeground': [('!focus', 'SystemWindowText')],
                      'fieldbackground': [('readonly', 'SystemButtonFace'),
                                          ('disabled', 'SystemButtonFace')],
                      'selectbackground': [('!focus', 'SystemWindow')]},
        'clam': {'foreground': [('readonly', 'focus', '#ffffff')],
                 'fieldbackground': [('readonly', 'focus', '#4a6984'), ('readonly', '#dcdad5')],
                 'background': [('active', '#eeebe7'), ('pressed', '#eeebe7')],
                 'arrowcolor': [('disabled', '#999999')]},
        'alt': {'fieldbackground': [('readonly', '#d9d9d9'),
                                    ('disabled', '#d9d9d9')],
                'arrowcolor': [('disabled', '#a3a3a3')]},
        'default': {'fieldbackground': [('readonly', '#d9d9d9'), ('disabled', '#d9d9d9')],
                    'arrowcolor': [('disabled', '#a3a3a3')]},
        'classic': {'fieldbackground': [('readonly', '#d9d9d9'), ('disabled', '#d9d9d9')]},
        'vista': {'focusfill': [('readonly', 'focus', 'SystemHighlight')],
                  'foreground': [('disabled', 'SystemGrayText'),
                                 ('readonly', 'focus', 'SystemHighlightText')],
                  'selectforeground': [('!focus', 'SystemWindowText')],
                  'selectbackground': [('!focus', 'SystemWindow')]},
        'xpnative': {'focusfill': [('readonly', 'focus', 'SystemHighlight')],
                     'foreground': [('disabled', 'SystemGrayText'),
                                    ('readonly', 'focus', 'SystemHighlightText')],
                     'selectforeground': [('!focus', 'SystemWindowText')],
                     'selectbackground': [('!focus', 'SystemWindow')]}}


class DateEntry(ttk.Entry):
    entry_kw = {'exportselection': 1,
                'invalidcommand': '',
                'justify': 'left',
                'show': '',
                'cursor': 'xterm',
                'style': '',
                'state': 'normal',
                'takefocus': 'ttk::takefocus',
                'textvariable': '',
                'validate': 'none',
                'validatecommand': '',
                'width': 12,
                'xscrollcommand': ''}

    def __init__(self, master=None, **kw):
        kw['selectmode'] = 'day'
        entry_kw = {}

        style = kw.pop('style', 'DateEntry')

        for key in self.entry_kw:
            entry_kw[key] = kw.pop(key, self.entry_kw[key])
        entry_kw['font'] = kw.get('font', None)
        self._cursor = entry_kw['cursor']  # entry cursor
        kw['cursor'] = kw.pop('calendar_cursor', None)

        ttk.Entry.__init__(self, master, **entry_kw)

        self._determine_downarrow_name_after_id = ''


        self._top_cal = tk.Toplevel(self)
        self._top_cal.withdraw()
        if platform == "linux":
            self._top_cal.attributes('-type', 'DROPDOWN_MENU')
        self._top_cal.overrideredirect(True)
        self._calendar = Calendar(self._top_cal, **kw)
        self._calendar.pack()

   
        self.format_date = self._calendar.format_date
        self.parse_date = self._calendar.parse_date

        self._theme_name = ''   
        self.style = ttk.Style(self)
        self._setup_style()
        self.configure(style=style)

        validatecmd = self.register(self._validate_date)
        self.configure(validate='focusout',
                       validatecommand=validatecmd)

        self._date = self._calendar.selection_get()
        if self._date is None:
            today = self._calendar.date.today()
            year = kw.get('year', today.year)
            month = kw.get('month', today.month)
            day = kw.get('day', today.day)
            try:
                self._date = self._calendar.date(year, month, day)
            except ValueError:
                self._date = today
        self._set_text(self.format_date(self._date))

        self.bind('<<ThemeChanged>>',
                  lambda e: self.after(10, self._on_theme_change))
      
        self.bind('<Configure>', self._determine_downarrow_name)
        self.bind('<Map>', self._determine_downarrow_name)
      
        self.bind('<Leave>', lambda e: self.state(['!active']))
        self.bind('<Motion>', self._on_motion)
        self.bind('<ButtonPress-1>', self._on_b1_press)
        
        self._calendar.bind('<<CalendarSelected>>', self._select)
      
        self._calendar.bind('<FocusOut>', self._on_focus_out_cal)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def _setup_style(self, event=None):
        self.style.layout('DateEntry', self.style.layout('TCombobox'))
        self.update_idletasks()
        conf = self.style.configure('TCombobox')
        if conf:
            self.style.configure('DateEntry', **conf)
        maps = self.style.map('TCombobox')
        if maps:
            try:
                self.style.map('DateEntry', **maps)
            except tk.TclError:
                # temporary fix for issue #61 and https://bugs.python.org/issue38661
                maps = MAPS.get(self.style.theme_use(), MAPS['default'])
                self.style.map('DateEntry', **maps)
        try:
            self.after_cancel(self._determine_downarrow_name_after_id)
        except ValueError:
            pass
        self._determine_downarrow_name_after_id = self.after(10, self._determine_downarrow_name)

    def _determine_downarrow_name(self, event=None):
        try:
            self.after_cancel(self._determine_downarrow_name_after_id)
        except ValueError:
            pass
        if self.winfo_ismapped():
            self.update_idletasks()
            y = self.winfo_height() // 2
            x = self.winfo_width() - 10
            name = self.identify(x, y)
            if name:
                self._downarrow_name = name
            else:
                self._determine_downarrow_name_after_id = self.after(10, self._determine_downarrow_name)

    def _on_motion(self, event):
        x, y = event.x, event.y
        if 'disabled' not in self.state():
            if self.identify(x, y) == self._downarrow_name:
                self.state(['active'])
                ttk.Entry.configure(self, cursor='arrow')
            else:
                self.state(['!active'])
                ttk.Entry.configure(self, cursor=self._cursor)

    def _on_theme_change(self):
        theme = self.style.theme_use()
        if self._theme_name != theme:
            self._theme_name = theme
            self._setup_style()

    def _on_b1_press(self, event):
        x, y = event.x, event.y
        if (('disabled' not in self.state()) and self.identify(x, y) == self._downarrow_name):
            self.state(['pressed'])
            self.drop_down()

    def _on_focus_out_cal(self, event):
        if self.focus_get() is not None:
            if self.focus_get() == self:
                x, y = event.x, event.y
                if (type(x) != int or type(y) != int or self.identify(x, y) != self._downarrow_name):
                    self._top_cal.withdraw()
                    self.state(['!pressed'])
            else:
                self._top_cal.withdraw()
                self.state(['!pressed'])
        elif self.grab_current():
            x, y = self._top_cal.winfo_pointerxy()
            xc = self._top_cal.winfo_rootx()
            yc = self._top_cal.winfo_rooty()
            w = self._top_cal.winfo_width()
            h = self._top_cal.winfo_height()
            if xc <= x <= xc + w and yc <= y <= yc + h:
                self._calendar.focus_force()
            else:
                self._top_cal.withdraw()
                self.state(['!pressed'])
        else:
            if 'active' in self.state():
                self._calendar.focus_force()
            else:
                self._top_cal.withdraw()
                self.state(['!pressed'])

    def _validate_date(self):
        try:
            date = self.parse_date(self.get())
            self._date = self._calendar.check_date_range(date)
            if self._date != date:
                self._set_text(self.format_date(self._date))
                return False
            else:
                return True
        except (ValueError, IndexError):
            self._set_text(self.format_date(self._date))
            return False

    def _select(self, event=None):
        date = self._calendar.selection_get()
        if date is not None:
            self._set_text(self.format_date(date))
            self._date = date
            self.event_generate('<<DateEntrySelected>>')
        self._top_cal.withdraw()
        if 'readonly' not in self.state():
            self.focus_set()

    def _set_text(self, txt):
        if 'readonly' in self.state():
            readonly = True
            self.state(('!readonly',))
        else:
            readonly = False
        self.delete(0, 'end')
        self.insert(0, txt)
        if readonly:
            self.state(('readonly',))

    def destroy(self):
        try:
            self.after_cancel(self._determine_downarrow_name_after_id)
        except ValueError:
            pass
        ttk.Entry.destroy(self)

    def drop_down(self):
        if self._calendar.winfo_ismapped():
            self._top_cal.withdraw()
        else:
            self._validate_date()
            date = self.parse_date(self.get())
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            if self.winfo_toplevel().attributes('-topmost'):
                self._top_cal.attributes('-topmost', True)
            else:
                self._top_cal.attributes('-topmost', False)
            self._top_cal.geometry('+%i+%i' % (x, y))
            self._top_cal.deiconify()
            self._calendar.focus_set()
            self._calendar.selection_set(date)

    def state(self, *args):
        if args:
            # change cursor depending on state to mimic Combobox behavior
            states = args[0]
            if 'disabled' in states or 'readonly' in states:
                self.configure(cursor='arrow')
            elif '!disabled' in states or '!readonly' in states:
                self.configure(cursor='xterm')
        return ttk.Entry.state(self, *args)

    def keys(self):
        keys = list(self.entry_kw)
        keys.extend(self._calendar.keys())
        keys.append('calendar_cursor')
        return list(set(keys))

    def cget(self, key):
        if key in self.entry_kw:
            return ttk.Entry.cget(self, key)
        elif key == 'calendar_cursor':
            return self._calendar.cget('cursor')
        else:
            return self._calendar.cget(key)

    def configure(self, cnf={}, **kw):

        if not isinstance(cnf, dict):
            raise TypeError("Expected a dictionary or keyword arguments.")
        kwargs = cnf.copy()
        kwargs.update(kw)

        entry_kw = {}
        keys = list(kwargs.keys())
        for key in keys:
            if key in self.entry_kw:
                entry_kw[key] = kwargs.pop(key)
        font = kwargs.get('font', None)
        if font is not None:
            entry_kw['font'] = font
        self._cursor = str(entry_kw.get('cursor', self._cursor))
        if entry_kw.get('state') == 'readonly' and self._cursor == 'xterm' and 'cursor' not in entry_kw:
            entry_kw['cursor'] = 'arrow'
            self._cursor  = 'arrow'
        ttk.Entry.configure(self, entry_kw)

        kwargs['cursor'] = kwargs.pop('calendar_cursor', None)
        self._calendar.configure(kwargs)
        if 'date_pattern' in kwargs or 'locale' in kwargs:
            self._set_text(self.format_date(self._date))

    config = configure

    def set_date(self, date):
        try:
            txt = self.format_date(date)
        except AssertionError:
            txt = str(date)
            try:
                self.parse_date(txt)
            except Exception:
                raise ValueError("%r is not a valid date." % date)
        self._set_text(txt)
        self._validate_date()

    def get_date(self):
        self._validate_date()
        return self.parse_date(self.get())
