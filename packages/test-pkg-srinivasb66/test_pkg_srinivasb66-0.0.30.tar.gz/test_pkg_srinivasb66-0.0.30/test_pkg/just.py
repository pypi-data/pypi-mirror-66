from pyspark.sql import SparkSession
import os
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from boxsdk import Client
from boxsdk import JWTAuth
import requests
import logging
from boxsdk import LoggingClient
from boxsdk.object.collaboration import CollaborationRole
from datetime import date
from pyspark import SparkFiles

def SayHello(name):
    print("Hello " + name)
    return

def findFolder(client, folder_name,parent_folderID):
    items = client.folder(parent_folderID).get_items()
    for item in items:
        if (folder_name == item.name):
            print('Folder already exists, returning id: "{0}"'.format(item.id))
            return item.id
    return 'false'           

def findOrCreatedFolder(client, folder_name,parent_folderID,collaborators):
    folderID = findFolder(client, folder_name,parent_folderID)
    print('Folder ID:"{0}" '.format(folderID))
    if(folderID == 'false' ):
        subfolder = client.folder(parent_folderID).create_subfolder(folder_name)
        print('Created folder:"{0}"'.format(folder_name))
        if(parent_folderID == '0'):
            addCollaborators(client,collaborators,subfolder)
        return subfolder.id
    else:
        return folderID

def addCollaborators(client,collaborators,subfolder):
    collaborators_list = collaborators.split(',')
    for collaborator in collaborators_list:
        client.folder(subfolder.id).collaborate_with_login(collaborator, CollaborationRole.EDITOR)
    print('Successfully added collaborators')

def search_files(client, file_name, folder_id):
    print('searching for : '+file_name)
    items = client.folder(folder_id).get_items(sort='date',direction='DESC')
    for item in items:
        if (file_name == item.name):
            print('file found:'+item.name)
            return item.id
    return 'false'

def uploadOrUpdateHistoryFile(client,file,history_folderID,history_filename,local_filename):
    history_folder = client.folder(history_folderID)
    fileID = search_files(client,history_filename,history_folderID)
    if(fileID == 'false' ):
        history_file = file.copy(history_folder,name=history_filename)
        print('File is copied to history folder')
        return history_file
    else:
        print('History File already exists, updating')
        hdfs_file = open(SparkFiles.get(local_filename),'rb')
        updated_historyfile = client.file(fileID).update_contents_with_stream(hdfs_file)
        hdfs_file.close() 
        return updated_historyfile

def mergeFiles(file_path,box_file_name,tmp_hdfs_filepath,file_format,fs,spark,hadoop):
    df=spark.read.format(file_format).load(file_path)
    df.coalesce(1).write.format(file_format).mode("overwrite").save(tmp_hdfs_filepath)
    for f in fs.listStatus(hadoop.fs.Path(tmp_hdfs_filepath)):
        temp=str(f.getPath()).split('/')
        if(file_format in temp[len(temp)-1]):
            isRenamed = fs.rename(f.getPath(), hadoop.fs.Path(tmp_hdfs_filepath+box_file_name))
            print(isRenamed)

def createBoxClient():
    auth = JWTAuth.from_settings_file(os.getenv('PLATFORM_SECRETS_PATH')+"/amp-analytics-app-dev-config.json")
    auth.authenticate_instance()
    client = LoggingClient(auth)
    print('Client sucessfully created')
    return client

def createTempFile(df,box_file_name,tmp_hdfs_filepath,file_format,hadoop):
    df.coalesce(1).write.format(file_format).mode("overwrite").save(tmp_hdfs_filepath)
    print(hadoop.fs.listStatus(hadoop.fs.Path(tmp_hdfs_filepath)))
    for f in hadoop.fs.listStatus(hadoop.fs.Path(tmp_hdfs_filepath)):
        temp=str(f.getPath()).split('/')
        if(file_format in temp[len(temp)-1]):
            isRenamed = hadoop.fs.rename(f.getPath(), hadoop.fs.Path(tmp_hdfs_filepath+box_file_name))
            print(isRenamed)

def UploadFile(file_path,file_format,box_file_name,box_foldername,box_history_foldername,collaborators,sc,spark):
    hadoop = sc._jvm.org.apache.hadoop
    hconf = hadoop.conf.Configuration()
    fs = hadoop.fs.FileSystem.get(hconf)

    today = date.today()
    d1 = today.strftime("%m%d%Y")
    box_history_filename = d1+"_"+box_file_name
    tmp_hdfs_filepath = "/tmp/"+os.getenv('PLATFORM_JOB_INSTANCE_ID')+"/"
    client = createBoxClient()
    print(fs.getFileStatus(hadoop.fs.Path(file_path)).isDirectory())
    print(fs.listStatus(hadoop.fs.Path(file_path)))
    if fs.getFileStatus(hadoop.fs.Path(file_path)).isDirectory():
        mergeFiles(file_path,box_file_name,tmp_hdfs_filepath,file_format,fs,spark,hadoop)
        spark.addFile('hdfs:///'+tmp_hdfs_filepath+box_file_name)
        fs.delete(hadoop.fs.Path(tmp_hdfs_filepath), True) 
        hdfs_file = open(SparkFiles.get(box_file_name),'rb')
        local_filename = box_file_name
    else:
        spark.addFile('hdfs:///'+file_path)
        x = file_path.split('/')
        file_name = x[len(x)-1]
        hdfs_file = open(SparkFiles.get(file_name),'rb')
        local_filename = file_name
    
    folderID = findOrCreatedFolder(client, box_foldername,'0',collaborators)
    history_folderID = findOrCreatedFolder(client, box_history_foldername,folderID,collaborators)
    fileID = search_files(client,box_file_name,folderID)

    if(fileID == 'false' ):
        new_file = client.folder(folderID).upload_stream(hdfs_file,box_file_name)
        print('File "{0}" uploaded to Box with file ID {1}'.format(new_file.name, new_file.id))
        hdfs_file.close()
        history_file = uploadOrUpdateHistoryFile(client,new_file,history_folderID,box_history_filename,local_filename)
    else:
        print('File already exists, updating')
        updated_file = client.file(fileID).update_contents_with_stream(hdfs_file)
        hdfs_file.close()
        history_file = uploadOrUpdateHistoryFile(client,updated_file,history_folderID,box_history_filename,local_filename)
    return
'''
def UploadDF(df,file_format,box_file_name,box_foldername,box_history_foldername,collaborators,sc,spark):
    hadoop = sc._jvm.org.apache.hadoop
    hconf = hadoop.conf.Configuration()
    fs = hadoop.fs.FileSystem.get(hconf)
    today = date.today()
    d1 = today.strftime("%m%d%Y")
    box_history_filename = d1+"_"+box_file_name
    tmp_hdfs_filepath = "/tmp/"+os.getenv('PLATFORM_JOB_INSTANCE_ID')+"/"
    client = createBoxClient()
    
    createTempFile(df,box_file_name,tmp_hdfs_filepath,file_format,hadoop)
    sc.addFile('hdfs:///'+tmp_hdfs_filepath+box_file_name)
    fs.delete(hadoop.fs.Path(tmp_hdfs_filepath), True) 
    hdfs_file = open(SparkFiles.get(box_file_name),'rb')
    local_filename = box_file_name
    
    folderID = findOrCreatedFolder(client, box_foldername,'0',collaborators)
    history_folderID = findOrCreatedFolder(client, box_history_foldername,folderID,collaborators)
    fileID = search_files(client,box_file_name,folderID)

    if(fileID == 'false' ):
        new_file = client.folder(folderID).upload_stream(hdfs_file,box_file_name)
        print('File "{0}" uploaded to Box with file ID {1}'.format(new_file.name, new_file.id))
        hdfs_file.close()
        history_file = uploadOrUpdateHistoryFile(client,new_file,history_folderID,box_history_filename,local_filename)
    else:
        print('File already exists, updating')
        updated_file = client.file(fileID).update_contents_with_stream(hdfs_file)
        hdfs_file.close()
        history_file = uploadOrUpdateHistoryFile(client,updated_file,history_folderID,box_history_filename,local_filename)
    return
'''