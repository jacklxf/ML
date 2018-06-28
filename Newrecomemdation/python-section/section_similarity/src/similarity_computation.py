import pygrs
import pandas as pd
import math
import numpy as np
from pyspark.mllib.linalg.distributed import *
from pyspark.mllib.linalg import Vectors

def read_hdfs_data(data_source, path, key):
    return data_source.read_data(path, key)

def calculated_score(count, avg_score):
    return (math.log2(count) +1) * avg_score

def table_processing(data_source, df):
    users = df['playerID'].unique().tolist()
    sections = df['sectionID'].unique().tolist()
    user_dictionary = data_source.bimap(users)
    section_dictionary = data_source.bimap(sections)
    df['playerID'] = df['playerID'].apply(lambda p: user_dictionary[p])
    df['sectionID'] = df['sectionID'].apply(lambda s: section_dictionary[s])
    new_df = df.groupby(['playerID', 'sectionID']).agg({'action_date':'size', 'score':'mean'}).rename(columns={'action_date':'count','score':'avg_score'}).reset_index()
    new_df['final_score'] = new_df.apply(lambda row: calculated_score(row[2], row[3]), axis =1)
    new_df = new_df.drop(['count', 'avg_score'], axis = 1)
    overall_ranking = new_df.groupby(["sectionID"]).agg({'final_score':'mean'}).sort_values('final_score', ascending=False)
    print(overall_ranking.head(10))
    overall_sections = list(overall_ranking.index.values)
    return new_df, user_dictionary, section_dictionary, overall_sections

def similarity_computation(df, spark):
    spark_df = spark.createDataFrame(df).groupBy("sectionID").pivot("playerID").sum("final_score").na.fill(0)
    vectorDF = spark_df.rdd.repartition(1).map(lambda row: IndexedRow(row[0], Vectors.dense(row[1: len(row)])))
    mat = IndexedRowMatrix(vectorDF).toBlockMatrix().transpose().toIndexedRowMatrix()
    exact = mat.columnSimilarities()
    exactEntities = exact.entries.map(lambda m : (m.i, (m.j, m.value))).groupBy(lambda x: x[0]).map(lambda g : (g[0], sorted(list(x[1] for x in g[1])[0: 10], key=lambda tup: tup[1], reverse = True)))
    model = dict(exactEntities.collect())
    print(model)
    return model

def return_records(df):
    print(df.head(40))
    records = {}
    df = df.groupby("playerID").aggregate(lambda x: list(x))
    print(df.head(20))
    for index, row in df.iterrows():
        items = [x for _,x in sorted(zip(row["final_score"], row["sectionID"]),reverse=True)]
        records[index] = items
    print(records)
    return records

def create_limit_dict(df):
    limit_dict = {}
    for index, row in df.iterrows():
        limit_dict[row['sectionID']] = True if int(row['limit']) > 1 else False
    return limit_dict

def store_models(model_store, dict, path):
    for key, value in dict.items():
        print(path+key)
        model_store.store_models_local(path + key, value)


if __name__ == "__main__":
    data_source = pygrs.data_source()
    df = read_hdfs_data(data_source, 'grs_section.h5', 'section_scores')
    limit_df = read_hdfs_data(data_source, 'grs_section.h5', 'section_limit')
    new_df, user_dictionary, section_dictionary, overall_sections = table_processing(data_source, df)
    model = pygrs.model_store()
    similarity_model = similarity_computation(new_df, model.spark)
    player_records = return_records(new_df)
    section_limit = create_limit_dict(limit_df)
    models = {}
    models["similarity_model.pickle"] = similarity_model
    models["player_records.pickle"] = player_records
    models["user_dictionary.pickle"] = user_dictionary
    models["section_dictionary.pickle"] = section_dictionary
    models["section_limit.pickle"] = section_limit
    models["overall_sections.pickle"] = overall_sections
    store_models(model, models, "./../models/")