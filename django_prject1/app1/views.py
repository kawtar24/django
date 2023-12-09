import io
import os
from urllib import request
from flask import redirect
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

from io import BytesIO, StringIO
import base64
import seaborn as sns
from django.http import HttpResponse
from django.shortcuts import render
from .forms import FileUploadForm,ChooseColumnsForm



#  Create your views here.
def index(request): 
        return render(request, 'app1/index.html')
       
def visualiser(request):

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['file']
            #  Traitement pour les fichiers Excel
            if fichier.name.endswith(('.xls', '.xlsx')):
                try:
                    data = pd.read_excel(fichier)
                    df = pd.DataFrame(data)
                    return render(request, 'app1/visualiser.html', {'df': df.to_html(classes='table table-bordered')})
                except pd.errors.ParserError:
                    return HttpResponse("Erreur lors de la lecture du fichier Excel. Veuillez vérifier le format du fichier.")

            #  Traitement pour les fichiers CSV
            elif fichier.name.endswith('.csv'):
                try:
                    data = pd.read_csv(fichier)
                    df = pd.DataFrame(data)
                    return render(request, 'app1/visualiser.html', {'df': df.to_html(classes='table table-bordered')})
                except pd.errors.ParserError:
                    return HttpResponse("Erreur lors de la lecture du fichier CSV. Veuillez vérifier le format du fichier.")

            else:
                #  Fichier non pris en charge
                return HttpResponse("Seuls les fichiers Excel (.xls, .xlsx) ou CSV (.csv) sont autorisés. Veuillez télécharger un fichier valide.")
    else:
        form = FileUploadForm()
    
    return render(request, 'app1/visualiser.html', {'form': form})


def Graphe(request):
    
    file_name = None  # Initialize with a default value
    plot_url = None 
    plot = None 
    df_head = pd.DataFrame()
    df=None
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
           
            file_name = request.FILES['file'].name  
            selected_graph = request.POST.get('graph')
            val1 = request.POST.get('val1')
            val2 = request.POST.get('val2')
            
            plt.figure()

            file_extension = os.path.splitext(file_name)[1]

            uploaded_file = form.cleaned_data['file']
            if  file_extension == '.csv':
                
                df = pd.read_csv(uploaded_file)
                df_head = df.head()
                sns.set(style="whitegrid")
                if selected_graph == '1' : 
                          with sns.axes_style("darkgrid"):
                           # Define a color palette for better distinction
                            palette = sns.color_palette("husl", 3)  # You can adjust the number of colors
                            
                            # Create a line plot with enhanced styling
                            plot = sns.lineplot(x=val1, y=val2, data=df, marker='o', color=palette[0], linestyle='-', linewidth=2, label='Line Plot')

                            plot.set_xlabel=val1
                            plot.set_ylabel=val2
                            # Customize the grid
                            plot.grid(axis='both', linestyle='--', alpha=0.7)

                            # Customize tick parameters
                            plot.tick_params(axis='both', which='major', labelsize=10)
                if selected_graph == '2' : 
                          plot = sns.scatterplot(x=val1, y=val2,data=df, marker='o', s=50,color='red')                          
                          plot.set_xlabel=val1
                          plot.set_ylabel=val2

                          
                if selected_graph == '3' :
                          palette = sns.color_palette("Paired")  
                          plot= sns.boxplot(x=val1,y=val2,data=df, palette=palette, width=0.5)
                          plot.set_xlabel=val1
                          plot.set_ylabel=val2
                          plot.set_title('Box Plot', fontsize=14)
                           # Customize the grid
                          plot.grid(axis='y', linestyle='--', alpha=0.7)

                            # Customize tick parameters
                          plot.tick_params(axis='both', which='major', labelsize=10)
                          plt.tight_layout()
                if selected_graph == '4' : 
                          plot= sns.histplot(x=val1,data=df)  
                          plot.set_xlabel=val1
                if selected_graph == '5' : 
                          plot= sns.kdeplot(x=val1,data=df)     
                          plot.set_xlabel=val1  
                if selected_graph == '6' : 
                          plot= sns.violinplot(x=val1,data=df)   
                          plot.set_xlabel=val1  

                if selected_graph == '7' : 
                          plot= sns.barplot(x=val1,y=val2,data=df)  
                          plot.set_xlabel=val1
                          plot.set_ylabel=val2    
                if selected_graph == '8' : 
                          dff = df.select_dtypes(include=['number'])
                          correlation_matrix = dff.corr()
                          plot=sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
                          plt.title('Heatmap')
                if selected_graph == '9' : 
                          category_counts = df[val1].value_counts()
                          plot=plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)

    # Save the plot as an image  
               
               # Save the plot as an image (you can save it to a file or encode it as base64)
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                # Close all     Matplotlib figures to clear the state
                plt.close()
                # Encode the plot to base64
                plot_url = base64.b64encode(image_png).decode('utf-8')


            if  file_extension in ('.xlsx', '.xls'): 
                
                uploaded_file = form.cleaned_data['file']
                df = pd.read_excel(uploaded_file)
                # Process the DataFrame
                sns.set(style="whitegrid")
                plot = sns.relplot(data=df)
                # Save the plot as an image (you can save it to a file or encode it as base64)
                buffer = io.BytesIO()
                plot.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                 # Get the first five rows of the DataFrame
                print(df_head)
                # Encode the plot to base64
                plot_url = base64.b64encode(image_png).decode('utf-8')
    else:
        form = FileUploadForm()
    return render(request, 'app1/Graphe.html', {'form': form, 'file_name': file_name, 'plot_url': plot_url, 'df_head': df_head})
    

  



    
def Parcoure_donnes(request):
  return render(request, 'app1/Parcoure_donnes.html')
