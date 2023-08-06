#file containing instructions for reporting release notes
import pyfiglet as pfg

def release_note_report(fname, program, version, fdir=''):
    file_namedir=fdir+'/'+fname
    fil=open(file_namedir, 'r')
    text=fil.read()
    fil.close()
    fig=pfg.Figlet()
    print(fig.renderText(program))
    print(fig.renderText(version))
    print(text)