import gradio as gr

# gradio是个很棒的工具，可以用来做一些机器学习模型的可视化，这里我们用它来做一个简单的文本分类器。

def greet(name):
    return "Hello " + name + "!"
iface = gr.Interface(fn=greet, inputs="text", outputs="text")
iface.launch()

