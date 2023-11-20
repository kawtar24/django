from django.http import HttpResponse
from django.shortcuts import  render
from django.shortcuts import render
from .forms import FileUploadForm, ChooseColumnsForm
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

from io import BytesIO
import base64
from .forms import FileUploadForm, ChooseColumnsForm


# Create your views here.
def index(request):
    
        
        return render(request, 'app1/index.html')
       
def visualiser(request):

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['file']
            # Traitement pour les fichiers Excel
            if fichier.name.endswith(('.xls', '.xlsx')):
                try:
                    data = pd.read_excel(fichier)
                    df = pd.DataFrame(data)
                    return render(request, 'app1/visualiser.html', {'df': df.to_html(classes='table table-bordered')})
                except pd.errors.ParserError:
                    return HttpResponse("Erreur lors de la lecture du fichier Excel. Veuillez vérifier le format du fichier.")

            # Traitement pour les fichiers CSV
            elif fichier.name.endswith('.csv'):
                try:
                    data = pd.read_csv(fichier)
                    df = pd.DataFrame(data)
                    return render(request, 'app1/visualiser.html', {'df': df.to_html(classes='table table-bordered')})
                except pd.errors.ParserError:
                    return HttpResponse("Erreur lors de la lecture du fichier CSV. Veuillez vérifier le format du fichier.")

            else:
                # Fichier non pris en charge
                return HttpResponse("Seuls les fichiers Excel (.xls, .xlsx) ou CSV (.csv) sont autorisés. Veuillez télécharger un fichier valide.")
    else:
        form = FileUploadForm()
    
    return render(request, 'app1/visualiser.html', {'form': form})



def Graphe(request):
    form = FileUploadForm()  # Define form outside the if block

    if request.method == 'POST':
        # File upload form handling
        if 'fileupload' in request.POST:
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                fichier = request.FILES['file']
                try:
                    data = pd.read_excel(fichier) if fichier.name.endswith(('.xls', '.xlsx')) else pd.read_csv(fichier)
                    df = pd.DataFrame(data)
                    
                    # Once the file is processed, show the column selection form
                    columns_form = ChooseColumnsForm(df.columns)
                    return render(request, 'app1/Graph.html', {'columns_form': columns_form})

                except pd.errors.ParserError:
                    return HttpResponse("Erreur lors de la lecture du fichier. Veuillez vérifier le format du fichier.")

        # Column selection form handling
        elif 'choose_columns' in request.POST:
            columns_form = ChooseColumnsForm(request.POST)
            if columns_form.is_valid():
                # Retrieve selected columns
                x_column = columns_form.cleaned_data['x_column']
                y_column = columns_form.cleaned_data['y_column']

                # Generate the graph using Matplotlib
                plt.figure(figsize=(10, 6))
                plt.scatter(df[x_column], df[y_column])
                plt.title(f'{y_column} vs {x_column}')
                plt.xlabel(x_column)
                plt.ylabel(y_column)

                # Save the plot to a BytesIO object
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)

                # Convert the BytesIO object to a base64-encoded string
                img_str = base64.b64encode(img_data.getvalue()).decode()

                # For example, you can render a simple HTML page with an image tag for the graph
                return render(request, 'app1/Graphe.html', {'img_str': img_str})

    return render(request, 'app1/Graphe.html', {'form': form})
def Parcoure_donnes(request):

  return render(request, 'app1/Parcoure_donnes.html')
