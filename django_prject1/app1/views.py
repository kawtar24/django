import io
import os
from urllib import request
from flask import redirect
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Utilisez le backend 'Agg' (non interactif) au lieu du backend par défaut
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import bernoulli ,binom ,expon, norm, poisson,uniform
from io import BytesIO, StringIO
import base64
import seaborn as sns
from django.http import HttpResponse, JsonResponse
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

def file_loi_view(request):
                 
                selected_graph = request.POST.get('graph')
                val1 = request.POST.get('val1')
                val2 =request.POST.get('val2')
                            
           
                if selected_graph == '1' :
                          data_bern = bernoulli.rvs(size=1000,p= float (val1))
                          plot = sns.histplot(data_bern, kde=True, stat='probability')
                          plot.set(xlabel='Bernoulli', ylabel='Probabilité')

                if selected_graph == '2' :
                         
                          data_binom = binom.rvs(n=int (val2),p=float (val1),loc=0,size=1000)
                          plot = sns.histplot(data_binom, kde=True, stat='probability')
                          plot.set(xlabel='Binomial', ylabel='Probabilité')

                if selected_graph == '3' :
                          
                          data_unif = uniform.rvs(loc=int (val1), scale=int (val2), size=1000)
                          plt.figure(figsize=(6,4))
                          plot = sns.histplot(data_unif, kde=True, stat='probability')
                          
                if selected_graph == '4' :
                          data_binom = poisson.rvs(mu=int (val1), size=10000)
                          plot = sns.histplot(data_binom, kde=True, stat='probability')
                          plot.set(xlabel='Poisson', ylabel='Probabilité')
                if selected_graph == '5' :
                          data = norm.rvs(loc=int (val1), scale=int (val2), size=1000)
                          plot = sns.kdeplot(data, fill=True)

                if selected_graph == '6' :
                          data = expon.rvs(scale=float (val1), size=1000)
                          plot=sns.kdeplot(data, fill=True)

               # Save the plot as an image  
               
               # Save the plot as an image (you can save it to a file or encode it as base64)
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                # Close all     Matplotlib figuliste to clear the state
                plt.close()
                # Encode the plot to base64
                plot_url = base64.b64encode(image_png).decode('utf-8')

                return render(request, 'app1/loi.html', {'plot_url': plot_url})


def stats(request):
    liste = None
    tab = None
    name=None
    ligne=None
    lignes=None
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)      
        if form.is_valid():
            file_name = request.FILES['file'].name  
            uploaded_file = form.cleaned_data['file']
            file_extension = os.path.splitext(file_name)[1]

            if  file_extension == '.csv':
                df = pd.read_csv(uploaded_file)
                stats_values = request.POST.get('stats_values')
                ligne_a_afficher = request.POST.get('stats')
                ligne_f_afficher = request.POST.get('statsd')
                ligne_l_afficher = request.POST.get('statsf')
                
                if stats_values:
                    if stats_values == "1":
                        tab=df.head()
                        name="Les 5 premier lignes du fichier"
                    if stats_values == "2":
                        tab =df.tail()
                        name="Les 5 dernier lignes du fichier"
                    if stats_values == "3":
                        liste = df.columns.tolist()
                if ligne_a_afficher:
                        ligne=df.loc[int(ligne_a_afficher)]
                if ligne_f_afficher:
                        lignes=df.loc[int(ligne_f_afficher):int(ligne_l_afficher)]      
    else:  # For GET requests or initial render
        form = FileUploadForm()               
    
    
    return render(request, 'app1/statistiques.html',{'form':form,'tab':tab, 'name':name,'liste':liste,'ligne':ligne, 'lignes':lignes})

def test_traitement(request):

    if request.method == 'GET':
        test_type = request.GET.get('testType')
        if test_type:
            # Récupérer les paramètres communs à tous les tests
            significance = float(request.GET.get('significance', 0.05))

            if test_type == 'tTest':
                # Récupérer les paramètres spécifiques au t-test
                field1 = request.GET.get('tTestField1')
                field2 = request.GET.get('tTestField2')
                s1 = request.GET.get('tTestS1')
                s2 = request.GET.get('tTestS2')
                n1 = request.GET.get('tTestN1')
                n2 = request.GET.get('tTestN2')

                t_stat, p_value, hypothesis_result = calculate_t_test (field1, field2, s1, s2, n1, n2, significance)

                # Construire la réponse JSON avec chaque résultat dans des phrases distinctes
                result_json = {
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'hypothesis_result': hypothesis_result,
                    'formula': f"t = (X̄1 - X̄2) / sqrt(s1^2/n1 + s2^2/n2)"
                }

                return JsonResponse(result_json)
                
            elif test_type == 'zTest':
                # Récupérer les paramètres spécifiques au z-test
                field = request.GET.get('zTestField')
                sigma = request.GET.get('zTestSigma')
                n = request.GET.get('zTestN')
                zTestmi =request.GET.get('zTestmi')
                z_test_results = calculate_z_test(field,  zTestmi,sigma, n, significance)

                # Extraire chaque résultat pour l'affichage
                z_statistic_result = z_test_results['z_statistic']
                p_value_two_sided_result = z_test_results['p_value_two_sided']
                p_value_left_result = z_test_results['p_value_left']
                p_value_right_result = z_test_results['p_value_right']
                hypothesis_result_two_sided = z_test_results['hypothesis_result_two_sided']
                hypothesis_result_left = z_test_results['hypothesis_result_left']
                hypothesis_result_right = z_test_results['hypothesis_result_right']

                # Construire la réponse JSON avec chaque résultat dans des phrases distinctes
                result_json = {
                    'z_statistic': z_statistic_result,
                    'p_value_two_sided': p_value_two_sided_result,
                    'p_value_left': p_value_left_result,
                    'p_value_right': p_value_right_result,
                    'hypothesis_result_two_sided': hypothesis_result_two_sided,
                    'hypothesis_result_left': hypothesis_result_left,
                    'hypothesis_result_right': hypothesis_result_right,
                    'formula': f"Z = (X̄ - μ) / (σ/ √n)"
                }

                return JsonResponse(result_json)
            
            elif test_type == 'tTest2':
                # Récupérer les paramètres spécifiques au t-test
                field = request.GET.get('tTestField2')
                sigma = request.GET.get('tTestSigma2')
                n = request.GET.get('testTestN2')
                tTestmi = request.GET.get('tTestmi2')
                t_test_results = calculate_t_test2(field, tTestmi, sigma, n, significance)

                # Extraire chaque résultat pour l'affichage
                t_statistic_result = t_test_results['t_statistic']
                p_value_two_sided_result = t_test_results['p_value_two_sided']
                hypothesis_result_two_sided = t_test_results['hypothesis_result_two_sided']

                # Construire la réponse JSON avec chaque résultat dans des phrases distinctes
                result_json = {
                    't_statistic': t_statistic_result,
                    'p_value_two_sided': p_value_two_sided_result,
                    'hypothesis_result_two_sided': hypothesis_result_two_sided,
                    'formula': f"t = (X̄ - μ) / (σ/ √n)"
                }

                return JsonResponse(result_json)

            elif test_type == 'linearRegression':
                x_values_str = request.GET.get('linearRegressionX', '')
                y_values_str = request.GET.get('linearRegressionY', '')

                x_values = [float(value) for value in x_values_str.split()]
                y_values = [float(value) for value in y_values_str.split()]

                # Appeler la fonction calculate_linear_regression
                slope, intercept = calculate_linear_regression(x_values, y_values)

                # Créer un graphique de dispersion avec la ligne de régression
                plt.scatter(x_values, y_values, label='Data points')
                plt.plot(x_values, slope * np.array(x_values) + intercept, color='red', label='Regression line')
                plt.xlabel('Variable indépendante (X)')
                plt.ylabel('Variable dépendante (Y)')
                plt.legend()

                # Convertir le graphique en image
                image_stream = io.BytesIO()
                plt.savefig(image_stream, format='png')
                image_stream.seek(0)

                # Encoder l'image en base64 pour l'inclure dans la réponse JSON
                image_data = base64.b64encode(image_stream.read()).decode('utf-8')

                # Fermer le graphique
                plt.close()

                # Retourner l'image en réponse JSON, ainsi que la pente et l'ordonnée à l'origine
                return JsonResponse({'image_path': image_data, 'slope': slope, 'intercept': intercept})

            else:
                return JsonResponse({'error': 'Invalid test type'})

        else:
            return JsonResponse({'error': 'Invalid test type'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
      
