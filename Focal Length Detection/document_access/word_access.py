import win32com.client

def run():
    try:
        Application = win32com.client.gencache.EnsureDispatch('Word.Application')
        Word = Application.ActiveDocument
        return Word
    except:
        return -1

def increase_font_size(word, distance, thresh):
    try:
        range1 = word.Range(0)
        if(distance > (thresh + 100)):
            range1.Font.Size = 24
        elif(distance < (thresh - 100)):
            range1.Font.Size = 12
        else:
            range1.Font.Size = 18
        return "Done"
    except:
        return -1
