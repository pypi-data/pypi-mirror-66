""" This module defines all exergi functions within the AWS.S3 module"""

def exportFileToS3(obj,bucket,key):
    """ This module exports a pandas.DataFrame to specified bucket/key. 

    Keyword Arguments:
        - obj [python obj.]  -  Python object to be exported
        - bucket [str]       -  S3 export bucket,no trailing "/".
                                "stage-data-scientist".
        - key [str]          -  S3 export key, no leading "/". String should 
                                end with the desired file format. 
                                "public/.../example.csv". Currently supported 
                                fileformats is
                                    - .csv
                                        - pandas.DataFrame()
                                    - .xlsx
                                        - pandas.DataFrame()
                                    - .pkl
                                        - pandas.DataFrame()
                                        - sklearn
                                    - .json
                                        - keras (model description)
                                    - .h5
                                        - keras (model weights)
                                    - .npy
                                        - numpy (arrays)
    Returns:
        None
    """

    import boto3
    import io
    import pickle
    import os
    import pandas as pd
    import numpy as np
    import tempfile
    import json
    from sklearn.externals import joblib
    
    # Connect to S3
    s3client = boto3.client("s3")
    s3resource = boto3.resource("s3")   

    # Extra file name, file format and export object type
    _, fileFormat = os.path.splitext(key)
    objClass = obj.__class__.__module__.split(".")[0]
    raiseString = "Object class {} not supported for {} export. - ".format(objClass,fileFormat)

    # Comma separated files 
    if fileFormat == ".csv":
        if objClass == "pandas":
            buffer = io.StringIO()
            obj.to_csv(buffer,index=False)    
            s3resource.Object(bucket, key).put(Body=buffer.getvalue())
        else:
            raise Exception(raiseString)

    # Excel files 
    elif fileFormat == ".xlsx":
        if objClass == "pandas":
            with io.BytesIO() as output:
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    obj.to_excel(writer)
                data = output.getvalue()
                s3resource.Object(bucket, key).put(Body=data)
        else:
            raise Exception(raiseString)

    # Pickle files 
    elif fileFormat == ".pkl":
    
        if objClass == "sklearn":
            with tempfile.TemporaryFile() as fp:
                joblib.dump(obj, fp)
                fp.seek(0)
                s3resource.Object(bucket, key).put(Body=fp.read())
        
        elif objClass == "pandas":
            serializedMyData = pickle.dumps(obj)
            s3resource.Object(bucket, key).put(Body=serializedMyData)
        else:
            raise Exception(raiseString)
    
    # JSON files
    elif fileFormat == ".json":
        if objClass == "keras":
            s3resource.Object(bucket, key).put(Body=json.dumps(obj.to_json()).encode())
        else:
            raise Exception(raiseString)
            
    # HDF5 files 
    elif fileFormat == ".h5":
        if objClass == "keras":
            with tempfile.NamedTemporaryFile(suffix='.h5')  as fp:
                obj.save(fp.name)   
                fp.seek(0)
                s3resource.Object(bucket, key).put(Body=fp.read())
        else:
            raise Exception(raiseString)

    # npy files 
    elif fileFormat == ".npy":
        if objClass == "numpy":
            with tempfile.TemporaryFile()  as fp:
                np.save(fp,obj) 
                fp.seek(0)
                s3resource.Object(bucket, key).put(Body=fp.read())
        else:
            raise Exception(raiseString)

    else:
        raise Exception(raiseString)

def importFileFromS3(bucket, key, objClass="pandas", **kwargs):
    """ This module imports a pandas.DataFrame from specified bucket/key. 

    Arguments:
        - bucket [str]      -   S3 export bucket,no trailing "/".
                                "stage-data-scientist".
        - key [str]         -   S3 export key, no leading "/". String should 
                                end with the desired file format. 
                                "public/.../example.csv". Currently supported 
                                fileformats is
                                    - .csv
                                        - pandas.DataFrame()
                                    - .xlsx
                                        - pandas.DataFrame()
                                    - .pkl
                                        - pandas.DataFrame()
                                        - sklearn
                                    - .json
                                        - keras (model description)
                                    - .h5
                                        - keras (model weights)
                                    - .npy
                                        - numpy (arrays)
        - objClass [str]    -   String explaining what object type file should
                                be loaded as (default = "pandas")
    Keyword Arguments:
        - **kwargs [any]    -   Keyword arguments import function. Import 
                                function varies for each file format: 
                                file format:
                                    .csv  = pd.read_csv()
                                    .xlsx = pd.read_excel()
                                    .pkl  = pd.read_pickle()
    Returns:
        - obj [python obj]  -   Imported 
    """
    import boto3
    import io
    import os
    import pandas as pd
    import numpy as np
    import tempfile
    from sklearn.externals import joblib
    from keras.models import load_model

    # Connect to S3
    s3client = boto3.client("s3")
    s3resource = boto3.resource("s3")   

    # Extra file name, file format and export object type
    _, fileFormat = os.path.splitext(key)
    raiseString = "Object class {} not supported for {} import. - ".format(objClass,fileFormat)

    # Get raw data from S3
    S3obj = s3client.get_object(Bucket=bucket,Key=key)
    S3data = S3obj["Body"].read()

    # CSV files 
    if fileFormat == ".csv":
        if objClass == "pandas":
            obj = pd.read_csv(io.BytesIO(S3data),**kwargs)
        else:
            raise Exception(raiseString)

    # Excel files 
    elif fileFormat == ".xlsx":
        if objClass == "pandas":
            obj = pd.read_excel(io.BytesIO(S3data), **kwargs)
        else:
            raise Exception(raiseString)

    # Pickle files 
    elif fileFormat == ".pkl":
        if objClass == "pandas":
            obj = pd.read_pickle(io.BytesIO(S3data), **kwargs)
        elif objClass == "sklearn":
            with tempfile.TemporaryFile() as fp:
                s3client.download_fileobj(Bucket=bucket, Key=key,Fileobj=fp)
                fp.seek(0)
                obj = joblib.load(fp)          
        else:
            raise Exception(raiseString)

    # JSON files
    elif fileFormat == ".json":
        if objClass == "keras":
            json_file = json.loads(s3resource.Object(bucket, key).get()['Body'].read().decode('utf-8'))
            obj = model_from_json(json_file)
        else:
            raise Exception(raiseString)

    # HDF5 files 
    elif fileFormat == ".h5":
        if objClass == "keras":
            with tempfile.NamedTemporaryFile() as fp:
                s3client.download_fileobj(Bucket=bucket, Key=key,Fileobj=fp)
                fp.seek(0)
                obj = load_model(fp.name)
        else:
            raise Exception(raiseString)

    # npy files 
    elif fileFormat == ".npy":
        if objClass == "numpy":
            with tempfile.NamedTemporaryFile()  as fp:
                s3client.download_fileobj(Bucket=bucket, Key=key,Fileobj=fp)
                fp.seek(0)
                obj = np.load(fp.name)
        else:
            raise Exception(raiseString)

    else:
        raise Exception(raiseString)
        
    return obj

def listFilesInPath(bucket,prefix,suffix=None,removeFileExtension=False):
    """ List all files (sorted) in the specified bucket and prefix
    
    Arguments:
        - bucket [str]      -   S3 bucket where path i located,no trailing "/".
                                "stage-data-scientist"
        - prefix [str]      -   S3 prefix where files should be listed, "/". 
        - suffix [str]      -   File suffix (like '.csv','.xlsx') that list of 
                                file should be filter with 
        - removeFileExtension
    Returns:
        - listOfFiles [lst]  -   List of files in bucket-prefix. 
    """
    import pandas as pd
    import io
    import boto3
    import os

    s3resource = boto3.resource("s3")
    s3bucket = s3resource.Bucket(bucket)
    listOfFiles = []
    
    # List all keys 
    for objectSummary in list(s3bucket.objects.filter(Prefix=prefix))[0:]:
        listOfFiles.append(objectSummary.key)
        
    listOfFiles = [fileName.replace(prefix,"") for fileName in listOfFiles if fileName != prefix]
    listOfFiles = sorted([fileName for fileName in listOfFiles if not "/" in fileName])

    # Subset only files ending with provided suffix 
    if suffix:
        listOfFiles = [fileName for fileName in listOfFiles if suffix in fileName]

    # Remove all file extensions 
    if removeFileExtension:
        listOfFiles = [os.path.splitext(fileName)[0] for fileName in listOfFiles]
    
    return listOfFiles