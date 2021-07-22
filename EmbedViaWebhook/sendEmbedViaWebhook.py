import tkinter as tk
from tkinter import colorchooser, messagebox, font, ttk
import os.path
import json
import discord


# Scrollable frame class from: https://blog.teclado.com/tkinter-scrollable-frames/
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


root = tk.Tk()
root.title('Send Embed to Discord via Webhook')
root.geometry('500x500')


def change_embed_color():
    global color
    c = tk.colorchooser.askcolor()
    btn_color.config(bg=c[1])
    color = discord.Colour.from_rgb(int(c[0][0]), int(c[0][1]), int(c[0][2]))


def send_embed():
    if not len(ent_title.get()) > 0 or not len(txt_desc.get('1.0', 'end-1c')) > 1:
        tk.messagebox.showerror('ERROR', 'Title and Description cannot be empty!')
        return
    if tk.messagebox.askyesno('SEND', 'Do you want to send this embed?'):
        # create webhook
        hook = discord.Webhook.from_url(url, adapter=discord.RequestsWebhookAdapter())
        # compose embed dict
        embed_dict = {
            'title': ent_title.get(),
            'type': 'rich',
            'description': txt_desc.get('1.0', 'end-1c'),
            'color': color.value,
            'fields': []
        }
        # gather content for fields
        for i in range(len(content)-1):
            inline = True if len(content[i]) - 1 > 1 else False
            for j in range(len(content[i])-1):
                elem = content[i][j]
                if len(elem['title'].get()) > 0 or len(elem['text'].get('1.0', 'end-1c')) > 1:
                    embed_dict['fields'].append({
                        'name': elem['title'].get(),
                        'value': elem['text'].get('1.0', 'end-1c'),
                        'inline': inline
                    })
        hook.send(embed=discord.Embed.from_dict(embed_dict))
        tk.messagebox.showinfo('OK', 'Embed sent')


def draw_content():
    for i in range(len(content)):
        for j in range(len(content[i])):
            o = content[i][j]
            if isinstance(o, dict):
                o['frame'].grid(row=i, column=j, sticky=tk.NSEW, padx=2, pady=2)
                o['title'].pack(fill=tk.X)
                o['text'].pack(fill=tk.BOTH)
            else:
                o.grid(row=i, column=j, sticky=tk.NSEW, padx=2, pady=2)


def add_content_item(row):
    # build frame
    frame = tk.Frame(master=frm_content)
    title = tk.Entry(master=frame, font=tk.font.Font(weight=tk.font.BOLD))
    text = tk.Text(master=frame, height=3, width=20)
    # insert package into content list
    row_list = content[row]
    row_list.insert(len(row_list)-1, {'frame': frame,
                                      'title': title,
                                      'text': text
                                      })
    # redraw content
    draw_content()


def add_content_row():
    # build frame
    frame = tk.Frame(master=frm_content)
    title = tk.Entry(master=frame, font=tk.font.Font(weight=tk.font.BOLD))
    text = tk.Text(master=frame, height=3, width=20)
    new_row = len(content)-1
    button = tk.Button(master=frm_content, command=lambda: add_content_item(new_row),
                       text='+', fg='green', font=tk.font.Font(weight=tk.font.BOLD, size=30))
    # insert package into content list
    content.insert(new_row, [{'frame': frame,
                              'title': title,
                              'text': text},
                             button])
    # redraw content
    draw_content()


def option_changed(value):
    global url
    if value == 'add new':
        # open new window to input new webhook
        win_newhook = tk.Toplevel(root)
        lbl_name_newhook = tk.Label(master=win_newhook, text='Name:')
        lbl_name_newhook.grid(row=0, column=0)
        ent_name_newhook = tk.Entry(master=win_newhook)
        ent_name_newhook.grid(row=0, column=1)
        lbl_address_newhook = tk.Label(master=win_newhook, text='Address:')
        lbl_address_newhook.grid(row=1, column=0)
        ent_address_newhook = tk.Entry(master=win_newhook)
        ent_address_newhook.grid(row=1, column=1)

        def add_webhook():
            webhook_options[ent_name_newhook.get()] = ent_address_newhook.get()
            with open('webhooks.json', 'w') as file:
                json.dump(webhook_options, file)
            drop_data.set(ent_name_newhook.get())
            win_newhook.destroy()
            win_newhook.update()

        btn_add_newhook = tk.Button(master=win_newhook, text='Add', bg='lime', command=add_webhook).grid(row=2)

    url = webhook_options[value]


# check for existing webhooks file
if os.path.exists('webhooks.json'):
    with open('webhooks.json', 'r') as file:
        webhook_options = json.load(file)
else:
    with open('webhooks.json', 'w') as file:
        webhook_options = {'add new': ''}
        json.dump(webhook_options, file)

# set default/initial value
drop_data = tk.StringVar()
drop_data.set('choose webhook')
url = ''
# set default/initial color
color = discord.Color.blue()


# Info widgets
frm_info = tk.Frame(master=root)
btn_color = tk.Button(master=frm_info, width=2, height=1, bg='#3498db', command=change_embed_color)
lbl_title = tk.Label(master=frm_info, text='Title:')
ent_title = tk.Entry(master=frm_info, font=tk.font.Font(weight=tk.font.BOLD))
lbl_webhook = tk.Label(master=frm_info, text='Channel:')
ent_webhook = tk.OptionMenu(frm_info, drop_data, *webhook_options.keys(), command=option_changed)

# Description widgets
frm_desc = tk.Frame(master=root)
lbl_desc = tk.Label(master=frm_desc, text='Description:')
txt_desc = tk.Text(master=frm_desc, height=2)

# Content widget
frm_scrollable = ScrollableFrame(root)

frm_content = tk.Frame(master=frm_scrollable.scrollable_frame)
content = [[], []]
frm_init_content = tk.Frame(master=frm_content)
content[0].append({'frame': frm_init_content,
                   'title': tk.Entry(master=frm_init_content, font=tk.font.Font(weight=tk.font.BOLD)),
                   'text': tk.Text(master=frm_init_content, height=3, width=20)
                   })
content[0].append(tk.Button(master=frm_content, command=lambda: add_content_item(0),
                            text='+', fg='green', font=tk.font.Font(weight=tk.font.BOLD, size=25)))
content[1].append(tk.Button(master=frm_content, command=add_content_row,
                            text='+', fg='green', font=tk.font.Font(weight=tk.font.BOLD, size=25)))

# Control widgets
frm_control = tk.Frame(master=root)
btn_send = tk.Button(master=frm_control, text='SEND', bg='lime', command=send_embed)

# Layout
## Info section
frm_info.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5, expand=tk.FALSE)
btn_color.pack(side=tk.LEFT)
lbl_title.pack(side=tk.LEFT)
ent_title.pack(side=tk.LEFT, fill=tk.X)
ent_webhook.pack(side=tk.RIGHT)
lbl_webhook.pack(side=tk.RIGHT)

## Description section
frm_desc.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5, expand=tk.FALSE)
lbl_desc.pack(anchor=tk.NW)
txt_desc.pack(fill=tk.BOTH)

## Content section
frm_scrollable.pack(fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=tk.TRUE)
frm_content.pack(fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5)
draw_content()

## Commit/Control section
frm_control.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5, expand=tk.FALSE)
btn_send.pack()

# start window
root.mainloop()
