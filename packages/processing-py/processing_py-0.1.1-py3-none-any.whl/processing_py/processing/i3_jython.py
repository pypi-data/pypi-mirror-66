from java.io import InputStreamReader, BufferedReader
from java.lang import System

def setup():
    #if not (sys.argv is None):
    #    for i in range(len(sys.argv)):
    #       println(sys.argv[i])
    #else:
    #    println("sys.argv == null")
    
    size(800,600)
    println('[Jython] Created!')

def draw():
    refresh_global_variables()
    listen()        

def refresh_global_variables():
	list_ = [str(millis()),str(mouseX),str(mouseY),str(key)]
	saveStrings("global_variables.txt", list_)

def listen():
    while(True):
        try:
            reader = BufferedReader(InputStreamReader(System.in))
            input = str(reader.readLine())
            println(input)
            if input == 'redraw()':
                break
            exec(input)
            
        except BaseException as e :
            println('error: '+str(e))
            saveStrings("error.txt", [str(e)])
  

