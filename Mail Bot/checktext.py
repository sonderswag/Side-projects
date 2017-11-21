def checkText(txt):
     txt  = str(txt)
     for i in txt:
          
          if i.isalpha():
               return False
               break
     return True 

print checkText('hello')

print checkText('a')

print checkText(123)

print checkText("123abc")
          