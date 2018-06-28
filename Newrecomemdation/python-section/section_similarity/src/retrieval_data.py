import pygrs
import json
import pandas as pd
import argparse
from datetime import datetime, date, timedelta
import time
from pandas import HDFStore

def indexKey(type, action):
    if 'opengame' in type:
        return type
    if action[-1].isdigit():
        return type+action[:-1]
    else:
        return type+action

def build_score_rules():
    action_dict = {}
    action_dict['sectionchangeall']='b'
    action_dict['sectionchangegames'] = 'b'
    action_dict['multiplaychangegames'] = 'b'
    action_dict['sectionviewall'] = 'v'
    action_dict['sectionleft'] = 'b'
    action_dict['sectionright'] = 'b'
    action_dict['myfavoritefavorite'] = 'b'
    action_dict['gametypefilterlivedealer'] = 'b'
    action_dict['gametypefilterslots'] = 'b'
    action_dict['gametypefilteregames'] = 'b'
    action_dict['gametypefiltersports'] = 'b'
    action_dict['sectiongameprovidericon'] = 'v'
    action_dict['sectiontheme'] = 'v'
    action_dict['opengame'] = 'o'
    return action_dict

def give_score(actionsJson, action_dict):
    sections_details = {}
    sections_score = {}
    for jobject in actionsJson:
        section = jobject['sectioncode'].lower()
        section_actions = {}
        if section in sections_details:
            section_actions = sections_details[section]
        # get action type e.g. 'o', 'b'
        action_index = indexKey(jobject['type'], jobject['action'])
        if action_index in action_dict:
            action_type = action_dict[action_index]
            # update section's action
            if action_type in section_actions:
                section_actions[action_type] += 1
            else:
                section_actions[action_type] = 1
        sections_details[section] = section_actions
    # calculate score for every section
    for section, actions in sections_details.items():
        browsing_count = actions['b'] if 'b' in actions else 0
        browsing_score = 0
        if browsing_count > 0 and browsing_count < 4:
            browsing_score = 1
        elif browsing_count >=4 and browsing_count < 11:
            browsing_score = 2
        elif browsing_score >= 11:
            browsing_score = 3
        viewing_score = 2 if 'v' in actions else 0
        opening_score = 2 if 'o' in actions else 0
        additional_score = 0
        if len(actions.keys()) <= 2 and len(actions.keys()) > 1:
            additional_score = 1
        elif len(actions.keys()) >= 3:
            additional_score = 2
        final_score = browsing_score + viewing_score + opening_score + additional_score
        sections_score[section] = final_score

    return sections_score

def format_data(records):
    totalSectionList = []
    print("start to format data")
    for row in records:
        player_id = row[0]
        actionJson = json.loads(row[1])['sequence']
        action_time = row[2]
        action_date = row[3]
        scores = give_score(actionJson, build_score_rules())
        for section, score in scores.items():
            data_row = [player_id, section, score, action_time, action_date]
            totalSectionList.append(data_row)
    df = pd.DataFrame(totalSectionList, columns = ['playerID', 'sectionID', 'score', 'action_time', 'action_date'])
    print(df.head(10))
    return df

def actions_prepare_query(args):
    currentDate = date.fromtimestamp(time.mktime(time.localtime()))
    correctDate = currentDate-timedelta(1)
    endDate = correctDate.strftime('%Y%m%d')
    startDate = (correctDate - timedelta(int(args.days_before))).strftime('%Y%m%d')
    print("Setting date: ")
    print(startDate, endDate)
    sql_query = """
    select 
    lower(pb.PlayerId) as PlayerId,
    lower(pb.Actions) as Actions,   
    case when pb.ClosedOn is null then AVG(datediff(s, pb.CreatedOn, pb.ClosedOn)) over () else datediff(s, pb.CreatedOn, pb.ClosedOn) end as actionTime,
    CONVERT(nvarchar(20), pb.CreatedOn, 120) actionDate
    from [dbo].[PlayerBehaviors] pb
    where 
    pb.CreatedOn > '{}'
    and pb.ClosedOn <= '{}'
    and pb.Actions LIKE '%templateintelligence%'
    """.format(startDate, endDate)
    print(sql_query)
    return sql_query

def section_limit_query():
    return """
    select distinct(Lower(Code)), Limit from [dbo].[LobbyTemplateSections]
    """

def get_section_limit_df(sections):
    section_limit_rows = []
    for row in sections:
        section_limit_rows.append([row[0], int(row[1])])
    df = pd.DataFrame(section_limit_rows, columns = ['sectionID', 'limit'])
    return df

def store_data(etl, data_dict, path):
    etl.write_hdfs(data_dict,path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--days_before', help="days before", default=30)
    parser.add_argument('-d', '--driver', default='{ODBC Driver 17 for SQL Server}')
    parser.add_argument('-s', '--server', default='10.25.41.117')
    parser.add_argument('-l', '--loginName', help="sql loginName", default="AIprojSG")
    parser.add_argument('-p', '--password', help="sql password", default="rsuaF6-DVeU8")
    args = parser.parse_args()
    actions_sql_query = actions_prepare_query(args)
    section_query = section_limit_query()
    etl = pygrs.etl()
    records = etl.read_sql_data(args, actions_sql_query, "UgsAI-Staging")
    sections_limit = etl.read_sql_data(args, section_query, "Ugs-staging")
    df = format_data(records)
    limit_df = get_section_limit_df(sections_limit)
    data_dict = {"section_scores": df, "section_limit": limit_df}
    store_data(etl, data_dict, "grs_section.h5")






