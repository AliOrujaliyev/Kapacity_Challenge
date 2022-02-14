import pandas as pd
import requests
from flask import Flask, Response
import json
from datetime import datetime


app = Flask(__name__)

# Just for testing purposes
@app.route('/')
def index():
    return "Hello World!"

# --------------------------------------------
# So, considering that this function can possibly be deployed, and rather than having simple function that does one job
# I believe it would be nice to have more flexible function, so I add some modifications to this endpoint, so that we can extend it in the future.
# --------------------------------------------
# filename should be string
# aggregation function should be string 
# minutes (interval) can be both float and int, as it is possible to have 0.5 minute intervals
# --------------------------------------------
@app.route("/timestamps/<string:filename>/<string:aggr>/<minutes>", methods=['GET'])
def timestamps_aggregated(filename, aggr,minutes):

    # check if filename is in the list of the allowed files
    whitelist_filenames = ["small1", "small2", "small3", "large"]

    if filename not in whitelist_filenames:
        return Response(
        "The filename " + filename + " does not exist or not supported for this endpoint",
        status=400,
    )


    # check if minutes is numeric type
    try:
        minutes = float(minutes)
    except ValueError:
        return Response("Can't convert " + minutes + " to number. Please provide numeric input.", status = 400)



    # in the future, if we want to support other aggregation types for this endpoint, we can add them to the following array
    whitelist_aggr = ['mean']

    # check if aggregation function is in the list of the allowed functions
    if aggr not in whitelist_aggr:
        return Response(
        "The aggregation function " + aggr + " does not exist or not supported for this endpoint",
        status=400,
    )


    # interval can't be negative or 0, as we can't take mean of 0 minute interval
    if minutes <= 0:
        return Response(
        "Number of minutes (interval) should have positive value",
        status=400,
    )

    try:
        # get the data from Kapacity API and store it to pandas dataframe
        response = requests.get("http://tech-challenge.kapacity.io/json?filename=" + filename)
        data = response.json()
        df = pd.DataFrame.from_dict(data)
    except:
        return Response("Can't read the data from external API", status = 400)

    try:
        # Convert time_stamp column to timestamp with (YY/MM/DD HH:MM:SS) format (removing milliseconds from the timestamp)
        df['time_stamp'] = df['time_stamp'].astype('datetime64[s]')

        # select only numeric and datetime types
        df = df.select_dtypes(include = ['int64', 'float64', 'datetime64[ns]'])

        # time interval by which data would be aggregated ("5T", "3T" and etc..)
        time_interval = str(minutes) + 'T'

        # number of rows of raw data received from Kapacity API
        raw_rows_count = df.shape[0]

        # aggregate data with provided method and time.
        # this assignment asked me to do only mean of values, but in the case if we would need other aggregation function like sum or median
        # i will put simple switch or if/else statement here
        # also, adding time_stamp index back as string column for later (when writing it in the file to preserve the shape)
        if aggr == 'mean':
            aggr_df = df.resample(time_interval, on='time_stamp').mean()
            aggr_df['time_stamp'] = aggr_df.index.astype('str')

        # number of rows of aggregared data
        aggr_rows_count = aggr_df.shape[0]

        # in the challenge it was mentioned to show how many raw rows was in the file, while in the image it says "number of rows aggregated"
        # so I decided to return both
        output_message = {
            'message': 'success',
            'status': 200,
            'nr_of_rows_raw': raw_rows_count,
            'nr_of_rows_aggr': aggr_rows_count
        }

        # save locally as json and csv file
        # technically we can't overwrite the same file everytime, so it would been nice to keep track of the different files
        # and when they were created. So, the simple method would be to add datetime to the filename.
        now = datetime.now()
        now = str(now.strftime("%d-%m-%Y%H:%M:%S"))

        json_file = aggr_df.to_json(orient="records")
        json_file = json.loads(json_file)
        with open((filename + "_" + now + '.json'), 'w') as f:
            json.dump(json_file, f, indent=4)

        aggr_df.to_csv(filename + "_" + now + ".csv",index=False)

        return output_message

    except Exception as e:
        # for debugging purposes
        print(e)
        output_message = {
            'message': "Error with the received data. Can't aggregate it",
            'status': 400,
        }
        return output_message

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')