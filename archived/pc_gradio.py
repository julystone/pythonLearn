import gradio as gr

# gradio�Ǹ��ܰ��Ĺ��ߣ�����������һЩ����ѧϰģ�͵Ŀ��ӻ�������������������һ���򵥵��ı���������

def greet(name):
    return "Hello " + name + "!"
iface = gr.Interface(fn=greet, inputs="text", outputs="text")
iface.launch()

