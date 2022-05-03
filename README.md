# EXPERT SYSTEM DESIGN FOR DIAGNOSIS OF DENTAL DISEASES USING THE K-NEAREST NEIGHBOR AND CERTAINTY FACTOR METHODS

I build an expert system design that applies a combination of Certainty Factor and K-Nearest Neighbor methods in solving problems of diagnosing dental diseases (especially for teledentistry). The expert system is website-based (using Jinja 3.0 and Bootstrap AdminLTE.io) and uses MySQL. 
The application provides an accuracy of 80% in the Certainty factor-only method using result validation and the combined accuracy of the Certainty Factor - K Nearest Neighbor method of 90% using Cross Validation (to see the calculation of 90% accuracy: https://github.com/fanimasturina/CF-KNN-Accuracy-Using-Jupyter-Notebook). The dataset is used on combination methods to serves the neighbor classification, the detail of dataset is consist of 100 patients medical records (name, certainty value of symptomps, and diagnosis).  

How to run the app on local:
1.	Download XAMPP, make sure the mySQL setting is on the way. (Turn on mysql and apache)
<img width="331" alt="image" src="https://user-images.githubusercontent.com/71430949/166093351-1057c6c6-cbb5-4365-a5a1-638f44c2f0f9.png">


2.	import database on mySQL. Its name is "essks" (it is in this folder, in unzip first). The quickest way to open a database is to click "Admin" on the mysql section of XAMPP.
<img width="399" alt="image" src="https://user-images.githubusercontent.com/71430949/166093420-fcd531e4-bf9c-475d-b933-0e1273562087.png">
<img width="438" alt="image" src="https://user-images.githubusercontent.com/71430949/166093297-fa30ec3b-751f-4166-8710-e7218cf96f98.png">


3.	open Visual Studio Code, then import this folder by "open folder" (not open file). 
<img width="165" alt="image" src="https://user-images.githubusercontent.com/71430949/166093301-dbbf8ead-5542-410c-b16a-2af112f1e1d7.png">


4.	Then later appears the entire file in the left side corner (all assets will appear).
 <img width="385" alt="image" src="https://user-images.githubusercontent.com/71430949/166093306-d7914cf0-7cf3-4b69-bf47-1134c084bd45.png">

5.	In VSC, shift + ctrl + p, then type "Powershell Integrated Console". Make sure the Integrated Console, if not yet can be downloaded in the extension Visual Studio Code.
 <img width="372" alt="image" src="https://user-images.githubusercontent.com/71430949/166093311-3b0c75c3-6aba-4f9a-92da-06bd2c69b885.png">

6.	Download virtual environment on terminal 
 <img width="468" alt="image" src="https://user-images.githubusercontent.com/71430949/166093315-5dff8811-9d35-493a-861a-e61d113c6825.png">

7.	Enter "python -m virtualenv venv" to create a virtual environment named venv
 <img width="468" alt="image" src="https://user-images.githubusercontent.com/71430949/166093317-495c343d-2a6b-4853-91f7-8aaf4f69d86a.png">

8.	Go to its virtual environment by typing "venv\Scripts\activate"
 <img width="468" alt="image" src="https://user-images.githubusercontent.com/71430949/166093321-fbab89d2-38aa-4d9a-af28-7f31825b255b.png">

9.	After entering venv, install all requirements by typing "pip install -r requirements.txt"
 <img width="468" alt="image" src="https://user-images.githubusercontent.com/71430949/166093329-3e1a1cb9-74e3-470e-b14c-e56eef6f7920.png">

10.	then click "python web.py" on the terminal to run its server. 
11.	If you are connected, open it in the web browser (Chrome) and click localhost or its IP name.
