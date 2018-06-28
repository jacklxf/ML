import pygrs
import pandas as pd
import math
import numpy as np
from pyspark.mllib.linalg.distributed import *
from pyspark.mllib.linalg import Vectors
import json
from itertools import cycle
import argparse

def read_models(model_store, model_list, path):
    models = {}
    for key in model_list:
        models[key] = model_store.read_models_local(path + key+".pickle")
    return models

class section_recommendation_model(pygrs.model_deploy):
    def __init__(self, similarity_model, player_records, user_dictionary, section_dictionay, section_limit, overall_sections):
        self.similarity_model = similarity_model
        self.player_records = player_records
        self.user_dictionay = user_dictionary
        self.section_dictionay = section_dictionay
        self.section_limit = section_limit
        self.overall_sections = overall_sections

    def add_section(self, section_code, sections_exist, section_limit, rank, personalized_results):
        if section_code in sections_exist and sections_exist[section_code]:
            section = {
                "section_code": section_code,
                "rank": rank
            }
            rank +=1
            personalized_results.append(section)
            return personalized_results, sections_exist, rank
        if section_code not in sections_exist:
            section = {
                "section_code": section_code,
                "rank": rank
            }
            rank += 1
            sections_exist[section_code] = section_limit[section_code]
            personalized_results.append(section)
            return personalized_results, sections_exist, rank
        return personalized_results, sections_exist, rank

    def get_sections(self, user_id, recommendation_number, reversed_section_dict):
        sections_exist = {}
        personalized_results = []
        rank = 1
        past_records = self.player_records[user_id]
        first_choice = past_records[0]
        second_choice = past_records[1] if len(past_records) > 1 else self.overall_sections[0]
        first_list = [sections[0] for sections in self.similarity_model[first_choice]] if first_choice in self.similarity_model else self.overall_sections
        second_list = [sections[0] for sections in self.similarity_model[second_choice]] if second_choice in self.similarity_model else self.overall_sections
        first_list.insert(0, first_choice)
        second_list.insert(0, second_choice)
        for f, s in zip(first_list, second_list):
            f_code = reversed_section_dict[f]
            s_code = reversed_section_dict[s]
            personalized_results, sections_exist, rank = self.add_section(f_code, sections_exist, self.section_limit, rank, personalized_results)
            if rank > recommendation_number:
                break
            personalized_results, sections_exist, rank = self.add_section(s_code, sections_exist, self.section_limit, rank, personalized_results)
            if rank > recommendation_number:
                break
        if(len(first_list) != len(second_list)):
            for l in second_list[len(first_list):] if len(first_list) < len(second_list) else first_list[len(second_list):]:
                l_code = reversed_section_dict[l]
                personalized_results, sections_exist, rank = self.add_section(l_code, sections_exist, self.section_limit, rank, personalized_results)
                if rank > recommendation_number:
                    break
        # deal with the situation that recommendation number is not fulfilled
        if(len(personalized_results) < recommendation_number):
            for section in self.overall_sections:
                section_code = reversed_section_dict[section]
                personalized_results, sections_exist, rank = self.add_section(section_code, sections_exist, self.section_limit, rank, personalized_results)
                if rank > recommendation_number:
                    break
        return personalized_results

    def give_result(self, request_json):
        request_json = json.loads(json.dumps(request_json))
        if "userID" not in request_json:
            raise pygrs.deploy_error("api error", "No userID has been passed in.")
        if "recommendationNumber" not in request_json:
            raise pygrs.deploy_error("api error", "No recommendationNumber has been passed in.")
        userID = request_json["userID"].lower()
        recommendationNumber = int(request_json["recommendationNumber"])
        reversed_section_dict = pygrs.data_source().reverse(self.section_dictionay)
        rank = 1
        non_personalized_results = []
        personalized_results = []
        for section in self.overall_sections:
            code = reversed_section_dict[section]
            section = {
                "section_code": code,
                "rank": rank
            }
            non_personalized_results.append(section)
            rank += 1
            if rank > recommendationNumber:
                break
        if userID in self.user_dictionay:
            personalized_results = self.get_sections(self.user_dictionay[userID], recommendationNumber, reversed_section_dict)
        result = {
                "userID": userID,
                "recommendationNumber": recommendationNumber,
                "personalized":personalized_results,
                "non_personalized": non_personalized_results[0: recommendationNumber -1]
            }
        return json.dumps(result, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help="api port", default="8068")
    args = parser.parse_args()
    model = pygrs.model_store()
    model_list = ["similarity_model", "player_records", "user_dictionary", "section_dictionary", "section_limit", "overall_sections"]
    models = read_models(model, model_list, "./../models/")
    recommendation_model = section_recommendation_model(models["similarity_model"], models[ "player_records"], models["user_dictionary"], models["section_dictionary"], models["section_limit"], models["overall_sections"])
    section_api = pygrs.rest_api(recommendation_model)
    route = pygrs.api_route()
    route.add_api(section_api, "/section_recommendation")
    route.serve_api("10.25.3.117", args.port)


