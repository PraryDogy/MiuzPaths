def display(root, text):
    '''
    Insert text in text widget
    '''
    # root > frame with text widget for showing text(top pack), frame with buttons: open, convert(bottom pack)
    # get label with text from root
    f1 = root.winfo_children()[0]
    textbox = f1.winfo_children()[0]

    # unlock textwidget
    textbox.configure(state='normal')
    
    # remove prev and paste new text
    textbox.delete('1.0', 'end')
    textbox.insert('1.0', text)

    # lock textwidget
    textbox.configure(state='disabled')
    