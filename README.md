# Kapacity_Challenge

Hello. Here is brief instruction of how to run my code.

I used Python and Flask to solve this challenge. So you would require to install python and the following packages:

Python (my version is 3.6)
Pandas
Flask
requests

If you have all the packages just run:
python3 solution.py

Otherwise, follow the next steps.

I highly recommend to use conda environment to do it:
Link to the miniconda, which is minimal installer for conda:
https://docs.conda.io/en/latest/miniconda.html


Just run the next code in the directory with the code

(you can change "myenv" to whatever name you want)

conda create -n myenv python=3.6 pandas flask requests
conda activate myenv
python3 solution.py

Now, the server will be active and you can send the API calls to http://192.168.0.141:5000/ or localhost:5000/

The endpoint for this challenge is:

localhost:5000/timestamps/<filename>/<function>/<minutes>
  
Examples:
  localhost:5000/timestamps/small1/mean/5
  localhost:5000/timestamps/small2/mean/5
  localhost:5000/timestamps/large/mean/5
  localhost:5000/timestamps/large/mean/10 (for 10 minutes mean in the case if you are interested)
  
Right now only mean function works and allowed filenames are (small1, small2, small3, large)
  
Please reach by email if there were any problems along the way. Have a nice day!
