import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.interpolate import make_interp_spline
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

def graph(ret):
    dict = ret
    appreciation_curr = np.array(dict["appreciation_curr"])
    appreciation_infl = np.array(dict["appreciation_infl"])
    depreciation = np.array(dict["depreciation"])
    mortgage = np.array(dict["mortgage"])
    total = np.array(dict["total"])
    domain = [2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034]

    with PdfPages('Real_Estate_Report.pdf') as pdf:
        # logo
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.imshow(plt.imread(os.path.join(dir_path, 'logo.png')))
        plt.axis('off')
        pdf.savefig()
        # Plot and save the first graph
        
        fig, ax = plt.subplots(figsize=(8, 4))
        Spline = make_interp_spline(domain,appreciation_curr)

        x=np.linspace(min(domain), max(domain), 500)
        y=Spline(x)
        ax.plot(x,y)
        ax.set_title("Appreciation (adj)")
        ax.set_ylabel("Price")
        ax.set_xlabel("Year")
        plt.scatter(domain, appreciation_curr, color='blue')
        for i, (xi, yi) in enumerate(zip(domain, appreciation_curr)):
            plt.text(xi, yi, "$" + str(int(yi)), ha='right', va='bottom', fontsize=6)
        pdf.savefig()  
        plt.close(fig) 
        
        fig, ax = plt.subplots(figsize=(8, 4))
        Spline = make_interp_spline(domain,appreciation_infl)

        x =np.linspace(min(domain), max(domain), 500)
        y=Spline(x)
        ax.plot(x,y)
        ax.set_title("Appreciation")
        ax.set_ylabel("Price")
        ax.set_xlabel("Year")
        plt.scatter(domain, appreciation_infl, color='blue')
        for i, (xi, yi) in enumerate(zip(domain, appreciation_infl)):
            plt.text(xi, yi, "$" + str(int(yi)), ha='right', va='bottom', fontsize=6)
        pdf.savefig()  
        plt.close(fig) 
        
        fig, ax = plt.subplots(figsize=(8, 4))
        Spline = make_interp_spline(domain,mortgage)

        x = np.linspace(min(domain), max(domain), 500)
        y= Spline(x)
        ax.plot(x,y)
        ax.set_title("Mortgage Costs")
        ax.set_ylabel("Price")
        ax.set_xlabel("Year")
        plt.scatter(domain, mortgage, color='blue')
        for i, (xi, yi) in enumerate(zip(domain, mortgage)):
            plt.text(xi, yi, "$" + str(int(yi)), ha='right', va='bottom', fontsize=6)
        pdf.savefig()   
        plt.close(fig) 

        
        fig, ax = plt.subplots(figsize=(8, 4))
        Spline = make_interp_spline(domain,depreciation)
        x =np.linspace(min(domain), max(domain), 500)
        y=Spline(x)
        ax.plot(x,y)
        ax.set_title("depreciation")
        ax.set_ylabel("Price")
        ax.set_xlabel("Year")
        plt.scatter(domain, depreciation, color='blue')
        for i, (xi, yi) in enumerate(zip(domain, depreciation)):
            plt.text(xi, yi, "$" + str(int(yi)), ha='right', va='bottom', fontsize=6)
        pdf.savefig()  
        plt.close(fig) 
        
        fig, ax = plt.subplots(figsize=(8, 4))
        Spline = make_interp_spline(domain,total-2*total[0])
        x = np.linspace(min(domain), max(domain), 500)
        y = Spline(x)
        ax.plot(x,y)
        ax.set_title("Total Change in Asset")
        ax.set_ylabel("Price")
        ax.set_xlabel("Year")
        plt.scatter(domain, total-2*total[0], color='blue')
        for i, (xi, yi) in enumerate(zip(domain, total-2*total[0])):
            plt.text(xi, yi, "$" + str(int(yi)), ha='right', va='bottom', fontsize=6)
        print(total-2*total[0])
        
        pdf.savefig()  
        plt.close(fig)

    return