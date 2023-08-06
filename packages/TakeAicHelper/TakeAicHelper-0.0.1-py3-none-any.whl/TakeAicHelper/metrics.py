import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

class Metrics:

    def __init__(self, path, encoding = 'utf-8', sep = ';', minimunScore = 0.6):
        self.path = path
        self.sep = sep
        self.encoding = encoding
        self.minimunScore = minimunScore
        self.data = pd.read_csv(self.path, encoding = self.encoding, sep = self.sep)

    def overview(self):
        trueIntentions = self.data[self.data['Score'].astype(float) >= self.minimunScore]
        falseIntentions = self.data[self.data['Score'].astype(float) < self.minimunScore]
  
        return(print(f"\nTamanho da base: {len(self.data)}" + 
                     f"\nQuantidade de intenções no modelo: {len(self.data['Intention'].value_counts().index)}" +
                     f"\nTaxa de Compreensão Geral: {format(len(self.data[self.data['Score'].astype(float) >= self.minimunScore]) / len(self.data) * 100, '.1f')}%" +
                     f"\nIntenções reconhecidas acima de {self.minimunScore*100}%: {len(trueIntentions)}" +
                     f"\nIntenções reconhecidas abaixo de {self.minimunScore*100}%: {len(falseIntentions)}"))    
    def tcg(self):
       tcgValue = format(len(self.data[self.data['Score'].astype(float) >= self.minimunScore]) / len(self.data) * 100, '.1f')
       return(tcgValue)
    
    def intentDetails(self, intentName):
        intentDataFrame = self.data[self.data['Intention'] == intentName][['Text','Intention','Score', 'Entities']]
        return(intentDataFrame)

    def intentions(self,n):
        
        intlist = []                        
        frame = { 
                'Intenção': pd.Series(self.data['Intention'].value_counts().index.tolist()), 
                'Frequência de reconhecimento': pd.Series(self.data['Intention'].value_counts().values.tolist()) 
                }
                        
        result = pd.DataFrame(frame)
                        
        if n > 0:
            result = result.nlargest(n,'Frequência de reconhecimento')
        elif n < 0:
            result = result.nsmallest(abs(n),'Frequência de reconhecimento')
        else:
            result
        
        intlist.append(result['Intenção'])                        
        
        return(print(result))

    def entities(self,n=0,intentName=None):
                    
        entitiesList = []
        entitiesValues = []
                    
        if intentName!=None:
          targetSeries = self.data[self.data['Intention'] == intentName].Entities
        else:
            targetSeries = self.data['Entities']                     
                        
        for el in targetSeries:
            if el != '[]':
             entitiesValues.append(el)
        
        for values in entitiesValues:
                entities = re.search(r'(?!"value":")(\w{1,100}\s?\w{1,100})(?="}])', values)
                entitiesList.append(entities.group(0))

        frame = { 
                'Entidade': pd.Series(entitiesList).value_counts().index.tolist(), 
                'Frequência de reconhecimento': pd.Series(entitiesList).value_counts().values.tolist()
                } 
                        
        entitiesList = pd.DataFrame(frame)                    
        
                        
        if n > 0:
            entitiesList = entitiesList.nlargest(n,'Frequência de reconhecimento')
        elif n < 0:
            entitiesList = entitiesList.nsmallest(abs(n),'Frequência de reconhecimento')
        else:
            entitiesList
                    
        return(print(entitiesList))

    def tr(self, figure=None):

        TR = self.data['Intention'].value_counts() / len(self.data) * 100
        formatvalue = []
                    
        for value in TR.values:
              formatvalue.append(format(value,'.2f'))
                   
        if figure=='table':
            fig = go.Figure(data=[go.Table(header=dict(values=['Intenções', 'Reconhecimento (%)'], fill_color='green', font_color='white'),
                                           cells=dict(values=[self.data['Intention'].value_counts().index.tolist(),formatvalue], line_color='green',
                                           fill_color='white', font_color='black'))])
            fig.update_layout(
                height=1000)

            showMode = fig.show()              
        elif figure=='chart':
            
            index_value = self.data['Intention'].value_counts().tolist()
            index_name = self.data['Intention'].value_counts().index.tolist()

            fig = px.bar(x=index_name, y=index_value, text=index_value, color=index_value, color_continuous_scale=px.colors.sequential.Greens)
            fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig.update_layout(
                uniformtext_minsize=3, 
                uniformtext_mode='hide',
                 yaxis_title="Frequência de reconhecimento",
                 xaxis_title="Nome das intenções")
            showMode = fig.show()
        else:                    

            frame = { 
                'Intenção': self.data['Intention'].value_counts().index.tolist(),
                'Reconhecimento (%)': formatvalue
                 } 

            trDf = pd.DataFrame(frame)  
            showMode = trDf

        return(showMode)

    def tci(self, figure=None, minimunScore=0.6):
        
        true_intentions = self.data[self.data['Score'].astype(float) >= self.minimunScore]
        intent_name = self.data['Intention'].value_counts().index.to_list()                      
        values = []
        
        for name in intent_name:
            values.append(len(true_intentions[(true_intentions['Intention'] == name)]) / len(self.data[(self.data['Intention'] == name)]) * 100)
            formatvalue2 = []
        for value in values:
            formatvalue2.append(format(value,'.2f'))
                        
        if figure=='table':     
            
            fig = go.Figure(data=[go.Table(header=dict(values=['Intenções', 'Compreensão Interna (%)'], fill_color='green', font_color='white'),
            cells=dict(values=[self.data['Intention'].value_counts().index.tolist(),formatvalue2], line_color='green',
            fill_color='white', font_color='black'))])
            fig.update_layout(
                height=1000)

            showMode = fig.show()

        elif figure=='chart':
            fig = px.bar(x=self.data['Intention'].value_counts().index.tolist(), y=values,text=values, color=values, color_continuous_scale=px.colors.sequential.Greens)
            fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig.update_layout(uniformtext_minsize=8,
                            uniformtext_mode='hide',
                            yaxis_title="Taxa de Compreensão Interna (%)",
                            xaxis_title="Nome das intenções",
                            title="")
            
            showMode = fig.show()

        else:                    

            frame = { 
                     'Intenção': self.data['Intention'].value_counts().index.tolist(),
                     'Compreensão Interna (%)': values
                    } 

            tciDf = pd.DataFrame(frame)  
            showMode = tciDf
       
        return(showMode)
        
    def csvByIntentions(self, output, sep):
        
        intentName = self.data['Intention'].value_counts().index.to_list()
        for intention in intentName:
            self.data[self.data['Intention'] == intention][['Text','Intention','Score', 'Entities']].to_csv(f'{output}/{intention}.csv', sep=sep)

def main():
		overview()
		tcg()
		tci()
		tr()
		intentions()
		entities()
		csvByIntentions()
		intentDetails
		