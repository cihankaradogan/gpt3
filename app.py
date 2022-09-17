import gradio as gr
import openai
import os
import subprocess
from threading import Thread
from zipfile import ZipFile
import time

openai.api_key = "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"
import os
os.environ['OPENAI_API_KEY'] = "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"

def run(user_topic, model, finetuned_model):
  if not finetuned_model:
    response = openai.Completion.create(
        model=model,
        prompt=user_topic,
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
  else:
    response = openai.Completion.create(
        model=finetuned_model,
        prompt=user_topic,
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
  return response.choices[0].text

def runfin():
  os.system('openai api fine_tunes.create -t "/content/dataset/dataset_prepared.jsonl" -m davinci')

def finetune(dataset):
  with ZipFile("tmp.zip", "w") as zipObj:
        zipObj.write(dataset.name, "dataset.csv")
  with ZipFile("tmp.zip", 'r') as zip_ref:
    zip_ref.extractall("dataset")
  os.system('yes|openai tools fine_tunes.prepare_data -f "/content/dataset/dataset.csv"')

  Thread(target = runfin).start()

  time.sleep(7)

  out = subprocess.getoutput("openai api fine_tunes.list")
  out = out.replace(r'\n', '\n')
  print(out)

  #os.system('rm -r "/content/dataset/dataset_prepared.jsonl"')
  #os.system('rm -r "/content/dataset/dataset.csv"')
  return out

demo = gr.Blocks()

with demo:
  gr.Markdown("<h3><center>OpenAI Playground</center></h3>")
  
  user_topic = gr.Textbox(label="Write your input", value="Correct this to standard English:\n\nShe no went to the market.")

  model = gr.Dropdown(label="Select a model", choices = ["text-davinci-002","text-curie-001","text-babbage-001","text-ada-001"])

  finetuned_model = gr.Textbox(label="If you will use a finetuned model, write id here")
  
  with gr.Row():
    written_essay = gr.inputs.Textbox(lines=10, label="Output")
  
  b1 = gr.Button("Run")
  b1.click(run, inputs = [user_topic, model, finetuned_model], outputs = written_essay) 

  gr.Markdown("<h3><center>OpenAI Finetune</center></h3>")

  dataset = gr.File(label="Upload your dataset")

  with gr.Row():
    outputfin = gr.inputs.Textbox(lines=10, label="Finetune status will be shown here (Don't lose id for future use)")
  b2 = gr.Button("Finetune")
  b2.click(finetune, inputs = dataset, outputs = outputfin) 
  
demo.launch(enable_queue=False, debug=True)